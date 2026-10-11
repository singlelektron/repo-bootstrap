# Verification and owner acceptance

Read when choosing checks or preparing evidence for a bootstrap or change.

## Evidence proportional to consequences

Choose verification from the changed behavior and plausible failure, not patch
size or a fixed activity checklist. Inspect documentation/appearance changes;
exercise public behavior and affected error paths for logic changes. Use the
project's tools and relevant tests without imposing a framework or mandatory risk
label. Repeat or broaden checks for changed behavior, failures, or unresolved
concerns, rather than arbitrary iterations.

Persistent data needs observable save/reload, clear overwrite/failure behavior,
and recovery instructions. Verify claimed backup/restore procedures on disposable
data. Money, authentication, sensitive data, destructive migrations, and valuable
persistent state need stronger failure-path and integration evidence, including
recovery/migration rehearsals where relevant. Never use real owner data for
destructive tests. During adoption, verify preservation of existing work and history.

Seek qualified human technical review where consequences exceed available
verification. Critical safety/security use or release needs a qualified human's
validation and approval plan. Passing tests, structural validation, and a clean
AI review are different forms of evidence; none alone proves product correctness.
For CI/review handling and merge authority, use [Git governance](git-workflow.md).

## Reviewable results

Give the owner enough evidence to accept or reject the outcome without reading
every line of code. The [PR template](../assets/templates/pull_request_template.md)
separates two audiences; size the content to the change and omit irrelevant fields:

- **Human Review:** what changed and why; reproducible actions, inputs, and expected
  outcomes; remaining limitations, risks, or product decisions. Use screenshots,
  runnable commands, or public API examples where they clarify acceptance.
- **Technical Verification:** actual checks and results for the delivered revision,
  observed CI and review status, substantive findings and their disposition, and
  failures, skipped checks, or unverified assumptions. Include compatibility,
  migration, and recovery evidence when relevant.

Exercise the documented install/run and acceptance path before claiming a working
baseline. Report owner-only checks as pending. Structural success confirms only
scaffolding; do not invent tests, logs, screenshots, remote protections, hosted
runs, or approvals. Separate local completion from external readiness, and make
any required owner action concrete.
