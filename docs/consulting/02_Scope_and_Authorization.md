---
status: technical-preflight-draft-not-signed
updated: 2026-10-05
---
# Scope and technical authorization worksheet

[Back to launch pack](00_Consulting_Launch.md)

This is a **technical preflight worksheet**, not an executed agreement, legal opinion or authorization to access any system. The owner and client's appropriate reviewer must approve the final engagement documents privately. Empty fields or an informal inquiry do not grant permission.

## Review boundary

| Field | Required private entry |
|---|---|
| Engagement reference / document version | [reference/version] |
| Provider and client legal parties | [confirmed privately] |
| Business outcome | [one decision] |
| Selected offer | [Entra OR CI/CD evidence review] |
| Assets explicitly in scope | [private approved list] |
| Assets / environments excluded | [private list] |
| Client authority and asset ownership verified by | [reviewer and evidence reference] |
| Third-party/platform permission constraints | [reviewed applicability and required permissions] |
| Start/end and timezone | [explicit window] |
| Authorized operators | [approved people only] |
| Approved evidence / access method | [sanitized export by default] |
| Client operational and emergency contacts | [private contact records] |
| Revocation / stop contact and channel | [private agreed channel] |
| Final fee, assumptions, payment and terms reference | [approved private quote and terms] |
| Written approval reference and date | [private executed record] |

## Activity matrix — proposed first engagement

The final matrix must explicitly record each permission. Do not interpret blank cells as approval.

| Activity | Proposed boundary | Final approval |
|---|---|---|
| Review supplied sanitized configuration evidence | Named evidence and one agreed scope | [pending] |
| Ask clarifying questions / hold walkthrough | Approved participants and private channel | [pending] |
| Direct tenant/repository access | Excluded by default; separately approve least-privilege, time-limited access if needed | [pending / excluded] |
| Network scanning, exploitation, phishing or credential testing | Excluded | [excluded] |
| Download production data or unredacted secrets | Excluded | [excluded] |
| Execute a workflow or deploy/change production configuration | Excluded | [excluded] |
| Retest a remediation | Separate approved scope, evidence and window | [pending / excluded] |
| Publish findings, logo, testimonial or case study | Separate explicit client approval | [pending / excluded] |

Do not request standing Global Administrator, broad repository administration, shared passwords or tokens in ordinary email. Any approved direct access is provisioned and revoked by the client's authorized administrator under its access process; this automation does not create permissions.

## Deliverables and acceptance

Proposed deliverables: a scope/evidence summary, prioritized findings with evidence confidence and limitations, practical remediation options, and one agreed walkthrough. Define the number of environments/workflows, evidence volume, review effort, revision/clarification allowance and delivery format before quoting.

Acceptance means receipt and review of the agreed deliverables, with an agreed correction/clarification process. It does not mean every risk is discovered, mitigated or certified. Finding remediation and retesting are separate unless explicitly included.

## Change and stop record

Record privately: requested change, reason, affected assets/activities, fee/timing impact, approvers and version. Pause affected work until approved. Stop immediately for revoked/expired authority, unexpected assets/data, exposed secrets, suspected active incident, unsafe impact or unavailable stop contacts. Record what stopped and notify through the agreed private channel; do not investigate beyond the approved boundary.
