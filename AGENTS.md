# SpaceGhostKilla agents

Preserve the original research design, free v1.2 downloads, and all release-state limitations. `services.html` is a new static design review, not a live checkout or booking system. It uses `service-assets/`; keep those out of unsafe DOM/network operations.

Coordination source: `jordanistan/illnetwork/AGENTS.md` and `.github/portfolio/`. Read live STATUS/ROADMAP/TEAM and open PRs before edits. No secret values, private client findings, or realistic token fixtures in repositories. Consulting requires scoped written authorization. Do not claim accreditation or released paid products. Native scanning/push-protection settings must be verified separately from workflow code.

Run `python3 scripts/check_site.py`, `node --check script.js`, `node --check service-assets/site.js`, and stage with `bash scripts/stage_site.sh <fresh-directory>`. Checkpoint actual tests, commit, PR, deployment, remaining work and blockers before context limits. Source for the services design is in `illnetwork/portfolio`. Production build command is `bash scripts/build_production.sh <fresh-directory>`; its caller must first regenerate `scripts/services-production.json` from the current central source after making services changes. Do not release Field Manual or KubeScan without their recorded release checks.
