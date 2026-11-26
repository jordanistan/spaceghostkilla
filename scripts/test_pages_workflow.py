#!/usr/bin/env python3
"""Fail-closed regression test for the complete Pages workflow contract."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PAGES_WORKFLOW = ROOT / ".github/workflows/pages.yml"
EXPECTED_PAGES_WORKFLOW = """name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - name: Check out without persisted credentials
        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7
        with:
          persist-credentials: false

      - name: Validate before publication
        run: |
          python3 scripts/check_site.py
          node --check script.js
          node --check service-assets/site.js

      - name: Stage site files
        run: bash scripts/stage_site.sh _site

      - name: Setup Pages
        uses: actions/configure-pages@45bfe0192ca1faeb007ade9deae92b16b8254a0d # v6

      - name: Upload artifact
        uses: actions/upload-pages-artifact@fc324d3547104276b827a68afc52ff2a11cc49c9 # v5
        with:
          path: _site

  deploy:
    permissions:
      contents: read
      pages: write
      id-token: write
    needs: build
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@368f82528645a54fb793d4d04e342629a3f51346 # v5
"""


class PagesWorkflowTests(unittest.TestCase):
    def test_complete_pages_workflow_contract_is_exact(self) -> None:
        self.assertEqual(
            PAGES_WORKFLOW.read_bytes(),
            EXPECTED_PAGES_WORKFLOW.encode("utf-8"),
        )


if __name__ == "__main__":
    unittest.main()
