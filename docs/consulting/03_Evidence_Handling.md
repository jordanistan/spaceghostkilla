---
status: proposed-process-owner-and-client-review
updated: 2026-10-05
---
# Evidence handling plan

[Back to launch pack](00_Consulting_Launch.md)

Agree this plan **before receiving evidence**. Completed plans and evidence stay in a separately approved private workspace. Public GitHub, Pages, public Drive links and public Obsidian sync are not client evidence channels.

## Private handling record

| Control | Owner/client decision required |
|---|---|
| Evidence needed for the scoped question | [minimal list] |
| Client-side sanitization requirements | [remove credentials, customer records and unnecessary identifiers] |
| Approved transfer destination | [specific private client-controlled or approved channel] |
| Authorized readers | [named people and least-privilege roles] |
| MFA, encryption, device and download rules | [agreed controls and verification] |
| Allowed processing tools | [approved local tools; any external service separately reviewed] |
| Working copies / backups | [locations, access and deletion handling] |
| Retention trigger and deadline | [explicit approved event/date; no default promise] |
| Incident/secret exposure contact | [agreed private channel] |
| Final deletion and access-revocation record | [reviewer and evidence reference] |

Do not upload evidence to an AI service, external scanner, support ticket, paste site or new subprocess unless the client-approved plan explicitly covers that destination and processing. Prefer minimal sanitized excerpts and offline review. This pack does not establish a secure transfer destination by itself.

## Receipt and review

1. Verify the engagement is authorized and the sender/destination match the approved plan.
2. Inventory the minimum received files privately: approved evidence reference, received time, type, source/version and reviewer. Hashes can help track file versions; they do not prove authenticity or confidentiality.
3. Inspect for unexpected secrets or sensitive records before wider processing. If present, stop, restrict access, notify the authorized client contact, and follow the client's approved exposure procedure. Do not copy secret values into findings or GitHub issues.
4. Separate source evidence from working notes and deliverables. Do not execute received files, macros or workflows as part of an evidence review.
5. Reference redacted evidence in the report with enough context to reproduce the reasoning inside the approved environment. Public examples must be synthetic and contain no realistic credentials.

## Closeout

Confirm deliverable receipt privately. Remove granted access, revoke temporary shares, and delete working copies/backups according to the agreed retention plan and any specifically reviewed obligations. Record what was removed and what remains with its reason and deadline. Do not claim deletion was completed until verified; a documentation checklist is not evidence of deletion.
