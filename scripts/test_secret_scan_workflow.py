#!/usr/bin/env python3
"""Offline regression tests for the SpaceGhostKilla secret-scan workflow."""

from pathlib import Path
import re
import unittest


CHECKOUT_SHA = "3d3c42e5aac5ba805825da76410c181273ba90b1"
GITLEAKS_SHA = "e0c47f4f8be36e29cdc102c57e68cb5cbf0e8d1e"
ROOT = Path(__file__).resolve().parents[1]
SECRET_SCAN_WORKFLOW = ROOT / ".github/workflows/secret-scan.yml"
SITE_CHECKS_WORKFLOW = ROOT / ".github/workflows/site-checks.yml"


class SecretScanWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.workflow = SECRET_SCAN_WORKFLOW.read_text()

    def test_trusted_triggers_and_read_only_permissions(self) -> None:
        triggers = self.workflow.split("on:\n", 1)[1].split("permissions:\n", 1)[0]
        self.assertEqual(
            triggers,
            "  pull_request:\n"
            "    branches: [main]\n"
            "  push:\n"
            "    branches: [main]\n"
            "  workflow_dispatch:\n"
            "  schedule:\n"
            "    - cron: '41 1 * * 2'\n",
        )
        self.assertNotIn("pull_request_target", self.workflow)
        self.assertEqual(self.workflow.count("permissions:\n  contents: read"), 1)
        self.assertNotRegex(self.workflow, r"\bwrite(?:-all)?\b")

    def test_actions_are_exactly_pinned(self) -> None:
        self.assertEqual(
            self.workflow.count(f"actions/checkout@{CHECKOUT_SHA}"), 1
        )
        self.assertEqual(
            self.workflow.count(f"gitleaks/gitleaks-action@{GITLEAKS_SHA}"), 1
        )
        uses = re.findall(r"(?m)^\s*-?\s*uses:\s*([^\s#]+)", self.workflow)
        self.assertEqual(len(uses), 2)
        for action in uses:
            with self.subTest(action=action):
                self.assertRegex(action, r"^[^@\s]+@[0-9a-f]{40}$")

    def test_scan_is_bounded_and_cancels_superseded_runs(self) -> None:
        self.assertEqual(self.workflow.count("timeout-minutes: 10"), 1)
        self.assertIn(
            "concurrency:\n"
            "  group: sgk-secret-scan-${{ github.ref }}\n"
            "  cancel-in-progress: true",
            self.workflow,
        )

    def test_checkout_and_gitleaks_keep_output_boundaries(self) -> None:
        self.assertEqual(self.workflow.count("fetch-depth: 0"), 1)
        self.assertEqual(self.workflow.count("persist-credentials: false"), 1)
        self.assertEqual(
            self.workflow.count("GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}"), 1
        )
        self.assertEqual(
            self.workflow.count("GITLEAKS_ENABLE_COMMENTS: 'false'"), 1
        )
        self.assertEqual(
            self.workflow.count("GITLEAKS_ENABLE_UPLOAD_ARTIFACT: 'false'"), 1
        )

    def test_site_checks_run_policy_test(self) -> None:
        site_checks = SITE_CHECKS_WORKFLOW.read_text()
        command = "python3 -m unittest scripts.test_secret_scan_workflow -v"
        self.assertEqual(site_checks.count(command), 1)
        validate = site_checks.split("\n  validate:\n", 1)[1]
        self.assertIn(
            "name: Check secret-scan workflow policy\n"
            f"        run: {command}",
            validate,
        )


if __name__ == "__main__":
    unittest.main()
