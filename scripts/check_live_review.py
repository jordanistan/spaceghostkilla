#!/usr/bin/env python3
"""Verify the fixed SpaceGhostKilla review surface and released downloads."""

from __future__ import annotations

import argparse
import hashlib
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener


ROOT = Path(__file__).resolve().parents[1]
SERVICES_URL = "https://spaceghostkilla.com/services.html"
PDF_PATH = "assets/downloads/SpaceGhostKilla-Cloud-Security-Quick-Audit-v1.2.pdf"
ZIP_PATH = "assets/downloads/sgk-quick-audit-v1.2.zip"
CSS_PATH = "service-assets/site.css"
JS_PATH = "service-assets/site.js"
HERO_PATH = "service-assets/hero.svg"
FAVICON_PATH = "service-assets/favicon.svg"
PDF_URL = f"https://spaceghostkilla.com/{PDF_PATH}"
ZIP_URL = f"https://spaceghostkilla.com/{ZIP_PATH}"
CSS_URL = f"https://spaceghostkilla.com/{CSS_PATH}"
JS_URL = f"https://spaceghostkilla.com/{JS_PATH}"
HERO_URL = f"https://spaceghostkilla.com/{HERO_PATH}"
FAVICON_URL = f"https://spaceghostkilla.com/{FAVICON_PATH}"
ASSETS = {
    CSS_URL: CSS_PATH,
    JS_URL: JS_PATH,
    HERO_URL: HERO_PATH,
    FAVICON_URL: FAVICON_PATH,
}
ENDPOINTS = {SERVICES_URL, PDF_URL, ZIP_URL, *ASSETS}
LIMITS = {
    SERVICES_URL: 256 * 1024,
    PDF_URL: 2 * 1024 * 1024,
    ZIP_URL: 256 * 1024,
    CSS_URL: 128 * 1024,
    JS_URL: 128 * 1024,
    HERO_URL: 128 * 1024,
    FAVICON_URL: 32 * 1024,
}
TYPES = {
    SERVICES_URL: {"text/html"},
    PDF_URL: {"application/pdf"},
    ZIP_URL: {"application/zip", "application/x-zip-compressed"},
    CSS_URL: {"text/css"},
    JS_URL: {"application/javascript", "text/javascript"},
    HERO_URL: {"image/svg+xml"},
    FAVICON_URL: {"image/svg+xml"},
}
TIMEOUT_SECONDS = 10
EXPECTED_CSP = (
    "default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self'; "
    "font-src 'self'; connect-src 'none'; frame-src 'none'; object-src 'none'; "
    "base-uri 'none'; form-action 'none'"
)
REQUIRED_TEXT = (
    "DESIGN REVIEW",
    "No live booking, payments, or data capture",
    "Design review only",
    "Scoped work · Written authorization · No credentials over email",
    "Draft pricing · final quote by agreement",
    "Field Manual and KubeScan remain unreleased",
    "do not imply accredited assessment status or a certification service",
    "Live inquiries, appointments, purchases, and subscriptions are not enabled in this preview.",
    "No claimed testimonials, certification, sales, or customer counts.",
)
ALLOWED_LINKS = {
    "index.html",
    "legal.html",
    "https://ill.network/review.html",
    "https://github.com/jordanistan/spaceghostkilla",
    "https://github.com/jordanistan",
}
HELD_DOMAINS = {
    "sxswasted.com",
    "austinfcsoccer.com",
    "austinfcsoccer.net",
    "austinfcjerseys.com",
    "atxsoccerjerseys.com",
}
CONTRADICTORY_CLAIMS = {
    "field manual is now available",
    "kubescan is now available",
    "now accepting clients",
    "book a review",
    "booking confirmed",
    "purchase now",
    "buy now",
    "certified compliant",
    "fedramp certified",
    "guaranteed secure",
}


class LiveReviewError(RuntimeError):
    """The live review surface crossed the reviewed boundary."""


def validate_url(url: str) -> None:
    if url not in ENDPOINTS:
        raise LiveReviewError("endpoint changed")
    if "\\" in url or any(ord(char) < 0x21 for char in url) or "%" in url:
        raise LiveReviewError("endpoint contains ambiguous data")
    parsed = urlsplit(url)
    try:
        port = parsed.port
    except ValueError as exc:
        raise LiveReviewError(f"invalid endpoint port: {exc}") from exc
    if parsed.scheme != "https" or parsed.hostname != "spaceghostkilla.com":
        raise LiveReviewError("endpoint origin changed")
    if parsed.username is not None or parsed.password is not None or port is not None:
        raise LiveReviewError("endpoint contains credentials or an explicit port")
    if parsed.query or parsed.fragment or "/../" in parsed.path or "/./" in parsed.path:
        raise LiveReviewError("endpoint contains an unreviewed component")


class ExactRedirectHandler(HTTPRedirectHandler):
    max_redirections = 3
    max_repeats = 1

    def __init__(self, expected: str) -> None:
        super().__init__()
        self.expected = expected

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001
        validate_url(newurl)
        if newurl != self.expected:
            raise LiveReviewError("redirect destination changed")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _read_bounded(response, limit: int) -> bytes:  # noqa: ANN001
    length = response.headers.get("Content-Length")
    if length is not None:
        try:
            declared = int(length)
        except ValueError as exc:
            raise LiveReviewError("invalid Content-Length") from exc
        if declared < 0 or declared > limit:
            raise LiveReviewError("declared response exceeds byte limit")
    chunks: list[bytes] = []
    total = 0
    while True:
        chunk = response.read(min(64 * 1024, limit + 1 - total))
        if not chunk:
            return b"".join(chunks)
        total += len(chunk)
        if total > limit:
            raise LiveReviewError("streamed response exceeds byte limit")
        chunks.append(chunk)


def fetch_url(url: str, *, opener=None) -> bytes:
    validate_url(url)
    if opener is None:
        opener = build_opener(ExactRedirectHandler(url))
    request = Request(
        url,
        method="GET",
        headers={
            "Accept": ", ".join(sorted(TYPES[url])),
            "Accept-Encoding": "identity",
            "User-Agent": "spaceghostkilla-live-review/1.0",
        },
    )
    with opener.open(request, timeout=TIMEOUT_SECONDS) as response:
        status = getattr(response, "status", None) or response.getcode()
        if status != 200:
            raise LiveReviewError(f"unexpected HTTP status {status}")
        if response.geturl() != url:
            raise LiveReviewError("final endpoint changed")
        content_type = response.headers.get_content_type()
        if content_type not in TYPES[url]:
            raise LiveReviewError(f"unexpected content type {content_type}")
        return _read_bounded(response, LIMITS[url])


class ReviewDocument(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.errors: list[str] = []
        self.text: list[str] = []
        self.scripts: list[str] = []
        self.script_text: list[str] = []
        self.stylesheets: list[str] = []
        self.icons: list[str] = []
        self.images: list[str] = []
        self.links: list[str] = []
        self.csps: list[str] = []
        self.referrers: list[str] = []
        self.robots: list[str] = []
        self.in_script = False

    def handle_starttag(self, tag: str, attrs) -> None:  # noqa: ANN001
        names = [name.lower() for name, _ in attrs]
        if len(names) != len(set(names)):
            self.errors.append(f"duplicate attribute on {tag}")
            return
        if any(name.startswith("on") or name in {"srcdoc", "srcset"} for name in names):
            self.errors.append(f"active attribute on {tag}")
        values = dict(attrs)
        if {"ping", "formaction"} & set(values):
            self.errors.append(f"unexpected request attribute on {tag}")
        if "style" in values:
            self.errors.append(f"inline style on {tag}")
        if tag in {"form", "input", "textarea", "select", "button", "iframe", "object", "embed", "audio", "video", "source", "track", "picture", "portal", "svg", "use", "base", "style"}:
            self.errors.append(f"unexpected active element: {tag}")
        active_attributes = {"src", "href", "action", "data", "poster"} & set(values)
        if active_attributes and tag not in {"script", "link", "img", "a"}:
            self.errors.append(f"unexpected active resource attribute on {tag}")
        if tag == "script":
            if set(values) != {"src", "defer"} or values.get("defer") is not None:
                self.errors.append("script attributes changed")
            self.scripts.append(values.get("src", ""))
            self.in_script = True
        elif tag == "link":
            if set(values) - {"rel", "href", "type"}:
                self.errors.append("link attributes changed")
            rel = {item.casefold() for item in values.get("rel", "").split()}
            if rel == {"stylesheet"}:
                self.stylesheets.append(values.get("href", ""))
            elif rel == {"icon"}:
                self.icons.append(values.get("href", ""))
            else:
                self.errors.append("unexpected link relation")
        elif tag == "img":
            if set(values) - {"src", "alt", "width", "height", "class"}:
                self.errors.append("image attributes changed")
            self.images.append(values.get("src", ""))
        elif tag == "a":
            if set(values) - {"href", "class"}:
                self.errors.append("anchor attributes changed")
            self.links.append(values.get("href", ""))
        elif tag == "meta":
            http_equiv = values.get("http-equiv", "").casefold()
            name = values.get("name", "").casefold()
            if http_equiv == "content-security-policy":
                self.csps.append(values.get("content", ""))
            elif http_equiv:
                self.errors.append("unexpected http-equiv metadata")
            elif name == "referrer":
                self.referrers.append(values.get("content", ""))
            elif name == "robots":
                self.robots.append(values.get("content", ""))

    def handle_endtag(self, tag: str) -> None:
        if tag == "script":
            self.in_script = False

    def handle_data(self, data: str) -> None:
        if self.in_script and data.strip():
            self.script_text.append(data)
        self.text.append(data)


def verify_services(data: bytes) -> str:
    try:
        html = data.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise LiveReviewError("services page is not strict UTF-8") from exc
    parser = ReviewDocument()
    parser.feed(html)
    parser.close()
    if parser.errors:
        raise LiveReviewError("; ".join(parser.errors))
    if parser.script_text:
        raise LiveReviewError("inline script content is not allowed")
    if parser.scripts != ["service-assets/site.js"]:
        raise LiveReviewError("script inventory changed")
    if parser.stylesheets != ["service-assets/site.css"]:
        raise LiveReviewError("stylesheet inventory changed")
    if parser.icons != ["service-assets/favicon.svg"]:
        raise LiveReviewError("icon inventory changed")
    if parser.images != ["service-assets/hero.svg"]:
        raise LiveReviewError("image inventory changed")
    if parser.csps != [EXPECTED_CSP]:
        raise LiveReviewError("content security policy changed")
    if parser.referrers != ["strict-origin-when-cross-origin"]:
        raise LiveReviewError("referrer policy changed")
    if parser.robots != ["noindex,nofollow"]:
        raise LiveReviewError("review indexing boundary changed")
    for href in parser.links:
        if href.startswith("#"):
            continue
        if href not in ALLOWED_LINKS:
            raise LiveReviewError(f"unexpected link target: {href}")
    public_text = " ".join(" ".join(parser.text).split())
    for marker in REQUIRED_TEXT:
        if marker not in public_text:
            raise LiveReviewError(f"missing review boundary: {marker}")
    lowered = html.casefold()
    for marker in CONTRADICTORY_CLAIMS:
        if marker in lowered:
            raise LiveReviewError(f"contradictory review claim: {marker}")
    for marker in HELD_DOMAINS | {"mailto:", "tel:", "support@spaceghostkilla.com", "formspree", "stripe.com", "paypal.com", "cloudflareinsights", "beacon.min.js", "localstorage", "sessionstorage", "xmlhttprequest"}:
        if marker.casefold() in lowered:
            raise LiveReviewError(f"prohibited review marker: {marker}")
    return hashlib.sha256(data).hexdigest()


def verify_file(data: bytes, local_path: Path, signature: bytes | None = None) -> str:
    if signature is not None and not data.startswith(signature):
        raise LiveReviewError(f"{local_path.name} has the wrong file signature")
    expected = local_path.read_bytes()
    if data != expected:
        raise LiveReviewError(f"{local_path.name} differs from the reviewed file")
    return hashlib.sha256(data).hexdigest()


def run(*, opener=None, root: Path = ROOT) -> dict[str, object]:
    services = fetch_url(SERVICES_URL, opener=opener)
    assets = {url: fetch_url(url, opener=opener) for url in ASSETS}
    pdf = fetch_url(PDF_URL, opener=opener)
    archive = fetch_url(ZIP_URL, opener=opener)
    return {
        "services_bytes": len(services),
        "services_sha256": verify_services(services),
        "asset_sha256": {
            path: verify_file(assets[url], root / path) for url, path in ASSETS.items()
        },
        "pdf_bytes": len(pdf),
        "pdf_sha256": verify_file(pdf, root / PDF_PATH, b"%PDF-"),
        "zip_bytes": len(archive),
        "zip_sha256": verify_file(archive, root / ZIP_PATH, b"PK\x03\x04"),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args(argv)
    evidence = run()
    print("SpaceGhostKilla live review passed: " + "; ".join(f"{key}={value}" for key, value in evidence.items()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
