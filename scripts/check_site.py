#!/usr/bin/env python3
"""Check local links and the sitemap in the static site without dependencies."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.refs: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if attributes.get("id"):
            self.ids.add(attributes["id"])
        attribute = {"a": "href", "img": "src", "script": "src", "link": "href"}.get(tag)
        if attribute and attributes.get(attribute):
            self.refs.append((tag, attributes[attribute]))


def local_target(page: Path, reference: str) -> tuple[Path, str] | None:
    parsed = urlsplit(reference)
    if parsed.scheme or parsed.netloc or reference.startswith("//"):
        if parsed.scheme == "javascript":
            raise ValueError("javascript: URL")
        return None
    path = unquote(parsed.path)
    if not path:
        return page.resolve(), unquote(parsed.fragment)
    target = (ROOT / path.lstrip("/")) if path.startswith("/") else (page.parent / path)
    if target.is_dir():
        target /= "index.html"
    target = target.resolve()
    if not target.is_relative_to(ROOT):
        raise ValueError("reference leaves the site root")
    return target, unquote(parsed.fragment)


def check() -> list[str]:
    errors: list[str] = []
    pages: dict[Path, Page] = {}
    for path in sorted(ROOT.glob("*.html")):
        parser = Page()
        parser.feed(path.read_text(encoding="utf-8"))
        pages[path] = parser

    for path, parser in list(pages.items()):
        for tag, reference in parser.refs:
            try:
                result = local_target(path, reference)
                if result is None:
                    continue
                target, fragment = result
                if not target.is_file():
                    errors.append(f"{path.name}: {tag} {reference!r} has no local file")
                elif fragment and target.suffix == ".html":
                    if target not in pages:
                        other = Page()
                        other.feed(target.read_text(encoding="utf-8"))
                        pages[target] = other
                    if fragment not in pages[target].ids:
                        errors.append(f"{path.name}: {reference!r} has no target id")
            except ValueError as error:
                errors.append(f"{path.name}: {reference!r}: {error}")

    css = ROOT / "styles.css"
    if css.exists():
        for reference in re.findall(r"url\(\s*['\"]?([^)'\"]+)", css.read_text(encoding="utf-8")):
            if reference.startswith(("#", "%23")):
                continue  # Fragment inside an inline SVG data URL.
            try:
                result = local_target(css, reference)
                if result is not None and not result[0].is_file():
                    errors.append(f"styles.css: {reference!r} has no local file")
            except ValueError as error:
                errors.append(f"styles.css: {reference!r}: {error}")

    try:
        sitemap = ET.parse(ROOT / "sitemap.xml")
        for element in sitemap.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
            url = urlsplit(element.text or "")
            if url.scheme != "https" or url.netloc != "spaceghostkilla.com":
                errors.append(f"sitemap.xml: unexpected URL {element.text!r}")
            elif not (ROOT / (url.path.lstrip("/") or "index.html")).is_file():
                errors.append(f"sitemap.xml: {element.text!r} has no page")
    except (ET.ParseError, FileNotFoundError) as error:
        errors.append(f"sitemap.xml: {error}")

    return errors


if __name__ == "__main__":
    failures = check()
    for failure in failures:
        print(failure, file=sys.stderr)
    print(f"Static site check: {'failed' if failures else 'passed'}")
    sys.exit(bool(failures))
