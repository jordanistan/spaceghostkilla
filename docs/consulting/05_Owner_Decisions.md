---
status: owner-confirmations-pending
updated: 2026-10-05
---
# Owner decisions before consulting launch

[Back to launch pack](00_Consulting_Launch.md)

Keep completed decision/evidence records private. Public status can say confirmed or pending without publishing employment, client, financial or agreement details.

| Gate | Exact owner action | Current evidence |
|---|---|---|
| Outside-work boundaries | Review applicable employer/confidentiality/conflict restrictions and confirm this work can proceed; use no employer accounts, equipment or confidential information | Pending |
| Offer and capacity | Choose one Entra OR CI/CD evidence-review boundary; approve effort, included deliverables/revisions, exclusions and actual availability | Pending |
| Final fee | Review effort and costs, then approve the written quote; current site says from $800 as draft pricing | Pending |
| Client authority | Verify the approving person and asset control; obtain written approved activities/window and any necessary third-party permissions | Pending for each engagement |
| Client commercial terms | Review final parties, payment, cancellation/refunds, confidentiality, liability, acceptance and dispute terms with an appropriate reviewer; use the executed private version | Pending |
| Evidence channel | Choose and verify restricted transfer/storage, readers, approved tools, incident contact and retention/deletion procedure | Pending |
| Invoice and payment | Select owner-controlled processor, verify account/access/payout setup privately, and agree when invoicing/payment occurs; no card form on this site | Pending |
| Commercial inquiry hosting | Use the separate production export on an approved commercial host; verify HTTPS/headers/email link/receipt before any reviewed cutover | Pending |
| Account protections | Verify applicable secret scanning, push protection, branch rules and MFA with owner/admin access; workflow files alone are insufficient evidence | Pending |

## Owner-controlled launch verification

1. Confirm preview `services.html` has no live booking/payment or inquiry capture.
2. Build production with `bash scripts/build_production.sh <fresh-output>` after reviewing the services snapshot source/version. Confirm the inquiry link targets the existing support address and opens an email app without sending automatically.
3. On the approved commercial staging host, verify HTTPS, services-page security response headers, navigation and free PDF/ZIP downloads.
4. Owner sends a synthetic nonsensitive inquiry from a separate test mailbox and verifies receipt/routing/reply. This automation sends no email.
5. Owner verifies processor/invoice behavior privately. A real charge/refund requires specific authorization; never infer settlement from a mock response.
6. Review final destination and rollback before changing hosting/DNS. Preserve mail routing and the research/download audience.
7. Accept one engagement only after all applicable gates and its private authorization record pass.

Field Manual and KubeScan remain unreleased. No client has been acquired, work authorized, invoice issued, payment received or revenue earned by creating these templates.
