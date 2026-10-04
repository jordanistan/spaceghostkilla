#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
output="${1:-_production}"
if [[ -e "$output" ]]; then echo 'Use a fresh output directory' >&2; exit 1; fi
bash scripts/stage_site.sh "$output"
python3 - "$output" <<'BUILD'
import json,sys
from pathlib import Path
out=Path(sys.argv[1]); data=json.loads(Path('scripts/services-production.json').read_text())
(out/'services.html').write_text(data['html'])
# Original site scripts/analytics stay preserved. Header CSP is scoped to services.
headers=data['headers'].replace('/*\n','/services.html\n',1)
(out/'_headers').write_text(headers)
BUILD
