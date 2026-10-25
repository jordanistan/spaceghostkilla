#!/usr/bin/env python3
"""Offline tests for the SpaceGhostKilla live-review verifier."""

from email.message import Message
import io
from pathlib import Path
import tempfile
import unittest
from urllib.request import Request

from check_live_review import (
    ASSETS,
    CSS_URL,
    ENDPOINTS,
    EXPECTED_CSP,
    FAVICON_URL,
    HERO_URL,
    JS_URL,
    LIMITS,
    PDF_PATH,
    PDF_URL,
    REQUIRED_TEXT,
    SERVICES_URL,
    TYPES,
    ZIP_PATH,
    ZIP_URL,
    ExactRedirectHandler,
    LiveReviewError,
    fetch_url,
    run,
    validate_url,
    verify_file,
    verify_services,
)


def valid_services(extra: str = "", text_extra: str = "") -> bytes:
    markers = " ".join(REQUIRED_TEXT)
    return f"""<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="{EXPECTED_CSP}">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta name="robots" content="noindex,nofollow">
<meta name="description" content="review"><meta property="og:title" content="review"><meta property="og:type" content="website">
<title>Review</title><link rel="icon" href="service-assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="service-assets/site.css">{extra}</head><body>
<a href="https://ill.network/review.html">Reviews</a><a href="index.html">Home</a><a href="#main">Main</a>
<a href="legal.html">Legal</a><a href="https://github.com/jordanistan">GitHub</a>
<a href="https://github.com/jordanistan/spaceghostkilla">Source</a>
<main id="main"><img src="service-assets/hero.svg" alt="">{markers} {text_extra}</main>
<script src="service-assets/site.js" defer></script></body></html>""".encode()


class FakeResponse:
    def __init__(self, body: bytes, *, url: str, content_type: str, status: int = 200, content_length: str | None = None) -> None:
        self.status = status
        self._url = url
        self._stream = io.BytesIO(body)
        self.headers = Message()
        self.headers["Content-Type"] = content_type
        if content_length is not None:
            self.headers["Content-Length"] = content_length

    def getcode(self) -> int:
        return self.status

    def geturl(self) -> str:
        return self._url

    def read(self, size: int = -1) -> bytes:
        return self._stream.read(size)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:  # noqa: ANN001
        return None


class FakeOpener:
    def __init__(self, responses: list[FakeResponse]) -> None:
        self.responses = iter(responses)
        self.requests: list[tuple[Request, int | float | None]] = []

    def open(self, request: Request, timeout=None):  # noqa: ANN001
        self.requests.append((request, timeout))
        return next(self.responses)


class EndpointTests(unittest.TestCase):
    def test_only_exact_endpoints_are_allowed(self) -> None:
        for endpoint in ENDPOINTS:
            validate_url(endpoint)
        invalid = [
            "http://spaceghostkilla.com/services.html",
            "https://evil.example/services.html",
            "https://user@spaceghostkilla.com/services.html",
            "https://spaceghostkilla.com:443/services.html",
            f"{SERVICES_URL}?x=1",
            f"{SERVICES_URL}#main",
            "https://spaceghostkilla.com/%73ervices.html",
            "https://spaceghostkilla.com/../services.html",
        ]
        for endpoint in invalid:
            with self.subTest(endpoint=endpoint), self.assertRaises(LiveReviewError):
                validate_url(endpoint)

    def test_redirects_revalidate_exact_destination(self) -> None:
        handler = ExactRedirectHandler(SERVICES_URL)
        request = Request(SERVICES_URL)
        self.assertEqual(handler.redirect_request(request, None, 302, "Found", {}, SERVICES_URL).full_url, SERVICES_URL)
        with self.assertRaises(LiveReviewError):
            handler.redirect_request(request, None, 302, "Found", {}, PDF_URL)


class FetchTests(unittest.TestCase):
    def test_get_has_bounds_and_no_ambient_credentials(self) -> None:
        opener = FakeOpener([FakeResponse(valid_services(), url=SERVICES_URL, content_type="text/html")])
        self.assertEqual(fetch_url(SERVICES_URL, opener=opener), valid_services())
        request, timeout = opener.requests[0]
        headers = {key.casefold(): value for key, value in request.header_items()}
        self.assertEqual(request.get_method(), "GET")
        self.assertEqual(timeout, 10)
        self.assertEqual(headers["accept-encoding"], "identity")
        for forbidden in ("authorization", "cookie", "referer"):
            self.assertNotIn(forbidden, headers)

    def test_status_type_final_url_and_sizes_are_strict(self) -> None:
        cases = [
            FakeResponse(b"x", url=SERVICES_URL, content_type="text/html", status=503),
            FakeResponse(b"x", url=SERVICES_URL, content_type="application/json"),
            FakeResponse(b"x", url=PDF_URL, content_type="text/html"),
            FakeResponse(b"x", url=SERVICES_URL, content_type="text/html", content_length=str(LIMITS[SERVICES_URL] + 1)),
            FakeResponse(b"x", url=SERVICES_URL, content_type="text/html", content_length="bad"),
        ]
        for response in cases:
            with self.subTest(response=response), self.assertRaises(LiveReviewError):
                fetch_url(SERVICES_URL, opener=FakeOpener([response]))

    def test_streamed_limit_is_enforced(self) -> None:
        previous = LIMITS[SERVICES_URL]
        LIMITS[SERVICES_URL] = 4
        try:
            with self.assertRaises(LiveReviewError):
                fetch_url(SERVICES_URL, opener=FakeOpener([FakeResponse(b"12345", url=SERVICES_URL, content_type="text/html")]))
        finally:
            LIMITS[SERVICES_URL] = previous


class ServicesTests(unittest.TestCase):
    def test_reviewed_services_page_passes(self) -> None:
        self.assertEqual(len(verify_services(valid_services())), 64)

    def test_every_required_boundary_is_required(self) -> None:
        for marker in REQUIRED_TEXT:
            with self.subTest(marker=marker), self.assertRaises(LiveReviewError):
                verify_services(valid_services().replace(marker.encode(), b"removed", 1))

    def test_active_and_external_content_is_rejected(self) -> None:
        extras = [
            '<form action="https://evil.example"></form>',
            '<script src="https://evil.example/x.js" defer></script>',
            '<script>alert(1)</script>',
            '<link rel="stylesheet" href="https://evil.example/x.css">',
            '<img src="https://evil.example/pixel.png">',
            '<meta http-equiv="refresh" content="0;url=https://evil.example">',
            '<base href="https://evil.example/">',
            '<iframe src="https://evil.example"></iframe>',
            '<svg><use href="https://evil.example/icons.svg#x"></use></svg>',
            '<video poster="https://evil.example/pixel.png"></video>',
            '<div data="https://evil.example/x">x</div>',
            '<a href="#main" ping="https://evil.example/collect">x</a>',
            '<div onclick="alert(1)">x</div>',
            '<div style="background:url(https://evil.example)">x</div>',
        ]
        for extra in extras:
            with self.subTest(extra=extra), self.assertRaises(LiveReviewError):
                verify_services(valid_services(extra=extra))

    def test_capture_tracker_and_held_domain_markers_are_rejected(self) -> None:
        markers = [
            "mailto:support@spaceghostkilla.com",
            "tel:+15125550100",
            "formspree",
            "stripe.com",
            "paypal.com",
            "cloudflareinsights",
            "beacon.min.js",
            "localStorage",
            "sessionStorage",
            "XMLHttpRequest",
            "sxswasted.com",
            "austinfcsoccer.com",
            "Field Manual is now available",
            "now accepting clients",
            "FedRAMP certified",
        ]
        for marker in markers:
            with self.subTest(marker=marker), self.assertRaises(LiveReviewError):
                verify_services(valid_services(text_extra=marker))

    def test_invalid_utf8_and_resource_drift_are_rejected(self) -> None:
        with self.assertRaises(LiveReviewError):
            verify_services(b"\xff")
        with self.assertRaises(LiveReviewError):
            verify_services(valid_services().replace(b"service-assets/site.js", b"service-assets/other.js"))


class DownloadAndRunTests(unittest.TestCase):
    def test_download_requires_signature_and_exact_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.pdf"
            path.write_bytes(b"%PDF-reviewed")
            self.assertEqual(len(verify_file(b"%PDF-reviewed", path, b"%PDF-")), 64)
            with self.assertRaises(LiveReviewError):
                verify_file(b"%PDF-changed", path, b"%PDF-")
            with self.assertRaises(LiveReviewError):
                verify_file(b"not-pdf", path, b"%PDF-")

    def test_checked_in_review_and_assets_match_the_verifier(self) -> None:
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(len(verify_services((root / "services.html").read_bytes())), 64)
        for path in ASSETS.values():
            asset = root / path
            self.assertTrue(asset.is_file())
            self.assertEqual(len(verify_file(asset.read_bytes(), asset)), 64)

    def test_full_run_fetches_seven_fixed_endpoints(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / Path(PDF_PATH).parent).mkdir(parents=True)
            for path in ASSETS.values():
                (root / path).parent.mkdir(parents=True, exist_ok=True)
                (root / path).write_bytes(path.encode())
            (root / PDF_PATH).write_bytes(b"%PDF-reviewed")
            (root / ZIP_PATH).write_bytes(b"PK\x03\x04reviewed")
            opener = FakeOpener([
                FakeResponse(valid_services(), url=SERVICES_URL, content_type="text/html"),
                FakeResponse(b"service-assets/site.css", url=CSS_URL, content_type="text/css"),
                FakeResponse(b"service-assets/site.js", url=JS_URL, content_type="application/javascript"),
                FakeResponse(b"service-assets/hero.svg", url=HERO_URL, content_type="image/svg+xml"),
                FakeResponse(b"service-assets/favicon.svg", url=FAVICON_URL, content_type="image/svg+xml"),
                FakeResponse(b"%PDF-reviewed", url=PDF_URL, content_type="application/pdf"),
                FakeResponse(b"PK\x03\x04reviewed", url=ZIP_URL, content_type="application/x-zip-compressed"),
            ])
            evidence = run(opener=opener, root=root)
            self.assertEqual(
                [request.full_url for request, _ in opener.requests],
                [SERVICES_URL, CSS_URL, JS_URL, HERO_URL, FAVICON_URL, PDF_URL, ZIP_URL],
            )
            self.assertEqual(evidence["pdf_bytes"], 13)

    def test_workflow_keeps_live_requests_off_pull_requests(self) -> None:
        workflow = (Path(__file__).resolve().parents[1] / ".github/workflows/live-review.yml").read_text()
        self.assertIn("permissions:\n  contents: read", workflow)
        self.assertIn("persist-credentials: false", workflow)
        self.assertIn("github.event_name == 'schedule'", workflow)
        self.assertIn("github.event_name == 'workflow_dispatch'", workflow)
        self.assertIn("github.ref == 'refs/heads/main'", workflow)
        self.assertIn("python3 scripts/test_live_review.py", workflow)
        self.assertIn("python3 scripts/check_live_review.py", workflow)
        for path in ("services.html", "service-assets/**", PDF_PATH, ZIP_PATH):
            self.assertGreaterEqual(workflow.count(path), 2)


if __name__ == "__main__":
    unittest.main()
    FAVICON_URL,
    HERO_URL,
    JS_URL,
