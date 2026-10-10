# Verification and owner review

Read when choosing checks, completing a bootstrap, or preparing a meaningful development PR.

## Choose depth from risk

Classify the changed behavior by the most consequential plausible failure, not by patch size. Record the tier and brief reason in the PR/report.

| Risk | Typical behavior | Proportionate evidence |
| --- | --- | --- |
| Low | Documentation, appearance, minor presentation | Inspect the changed result, check applicable links/rendering and relevant build checks; do not invent tests for wording |
| Medium | Application logic, file operations, ordinary local data | Relevant automated tests plus observable acceptance steps; cover affected errors and compatibility |
| High | Money, authentication, sensitive data, destructive migrations, important persistent state | Failure-path and integration evidence, backup/restore or migration rehearsal where relevant, explicit risk decisions, and independent qualified human technical review where appropriate |
| Critical | High-impact safety/security systems | Stop before critical external use or release until a qualified human defines and reviews the validation/approval plan; ordinary tests or AI review alone are insufficient |

Simple persistent storage can be medium risk; a destructive migration or valuable irreplaceable data raises it. Use disposable data for recovery/rehearsal checks. Do not test destruction on a real user project. An additional AI reviewer can find defects, but cannot stand in for a qualified human or prove correctness.

## Two review layers

Every meaningful PR/report includes both layers, sized to the change:

- **Human review:** What changed and why, observable behavior, reproducible owner steps with inputs and expected results, remaining risks/limits, and any pending product decision. UI changes benefit from actual screenshots; CLI/backend changes from runnable commands and sample outputs; libraries from a minimal public API example. The owner can reject work that fails observable acceptance criteria without inspecting its implementation.
- **Technical verification:** Relevant modules and implementation choices, tests added/changed, exact commands actually executed and outcomes, CI run status/link where observed, failures/skips, compatibility/migrations, and important unverified assumptions. State which commit or local revision the evidence covers.

Use `assets/templates/pull_request_template.md` as an adaptation aid. Describe actual results, including failures. Never invent screenshots, logs, passing tests, hosted CI runs, branch protection, or reviewer approval. If an owner action is necessary, provide its concrete steps and explain what remains unverified.

## Evidence at bootstrap completion

Run the program/library through its documented installation/build path and demonstrate its meaningful behavior. Use standard checks suitable for the actual toolchain and project; do not force one language or add tools without a reason. Provide basic automated tests and a corresponding CI configuration. A structural validator can confirm files, metadata and Git scaffolding; it cannot establish working software or product correctness.

For a persistent-data project, demonstrate save/reload and relevant failure handling; verify any documented backup/recovery procedure on disposable data before claiming it works. For adoption, verify preservation of initial history, existing instructions and unrelated user edits. For all modes, ensure approved criteria are satisfied or clearly report outstanding decisions/checks.

Report completion separately from external readiness: local checks may pass while hosted CI, remote controls or deployment remain unconfigured. Do not conceal those gaps or invent remote activity to close them. After checks pass, repeat or broaden them only for changed code, failures, new evidence or an unresolved concern.
