<!-- Adapt paths, commands, boundaries and language; resolve tokens, remove this comment and optional sections. Merge with existing instructions instead of replacing them. -->
# Agent instructions

## Sources of truth

- `docs/PRODUCT.md`: approved requirements, constraints, non-goals and acceptance criteria. Label assumptions/proposals; never change approved scope to fit incomplete code. Record already approved owner decisions without asking again.
- Running software and user documentation: current behavior. `README.md` holds entry steps; `docs/OWNER_GUIDE.md` holds daily operation, verification and recovery.
- GitHub Issues: pending work when available. PR/CI: executed verification and review evidence. Use a local PR-style report when a remote is unavailable.
- This file: agent workflow and validation commands. Lasting technical decisions belong in existing architecture/decision records only when complexity warrants them.

Read the documents relevant to the task; a trivial change does not require reading everything. If these sources disagree, identify the conflict and preserve approved requirements.

## Work and Git

1. Inspect applicable instructions, current branch/status, relevant code and the task. Plan in proportion to scope.
2. Create a short-lived task branch from `{{DEFAULT_BRANCH}}`; do not implement directly on that branch after initialization. One logical task normally has one branch and one PR.
3. Make focused changes. Preserve unrelated edits, files and history. Never reset, discard, stash, amend, stage or commit unrelated user work. Stage explicit task paths. If overlapping user edits cannot be safely separated, obtain direction.
4. Commit meaningful changes, run relevant checks, and self-review the diff for correctness, safety, scope and documentation. Earlier checks are encouraged. Commit fixes and rerun affected checks so evidence covers the final revision.
5. Create a draft PR when publication is authorized; otherwise prepare a local diff and PR-style report. Include human review and technical verification. Merge only with explicit authorization; prefer squash merge.

Routine reversible implementation, local branches/commits, relevant checks and maintenance of corresponding usage docs are covered by an authorized task. Do not ask repeatedly. Obtain approval for destructive operations, security-sensitive changes, expensive actions, substantial product/governance changes, changed privacy/data guarantees, or major architectural/operational commitments. Existing explicit approval counts. A proposed decision must remain labeled as proposed until approved.

Remote repository creation, pushes, visibility/collaborator/secret changes, publishing and deployment require authorization covering those actions. Authorization to open a PR includes necessary branch publication, but not merge or deployment. Never claim remote protections or hosted CI ran without observing them.

## Project checks and boundaries

Run from `{{VALIDATION_CONTEXT}}`:

```sh
{{VALIDATION_COMMANDS}}
```

{{PROJECT_BOUNDARIES}}

Choose checks relevant to the changed behavior. Report exact commands, actual outcomes, skipped/failed checks and unverified assumptions; do not hide failures. Structural checks alone do not prove correctness. Do not write tests that merely mirror low-impact wording edits.

Classify risk: low (appearance/docs), medium (ordinary logic/local data), high (money, auth, sensitive data, destructive migration or important persistent state), critical (high-impact safety/security). Scale verification accordingly. High-risk changes need failure-path/recovery evidence and qualified independent human review where appropriate; critical use/release needs a qualified human-approved validation plan. AI review is supplemental.

## Documentation and review deliverables

Update the existing authoritative document when its underlying behavior or decision changes. Keep temporary analysis in Issues/PRs; avoid speculative documents and duplicated evolving facts. Substantial changes to approved requirements, development governance, security/privacy assumptions, user-data guarantees or major commitments require owner approval.

Every meaningful PR/report must include plain-language what/why, observable owner verification steps, remaining risks and product decisions; and technical details, affected modules/tests, executed commands/results, hosted CI status, compatibility/migration notes and unverified assumptions. Use `.github/pull_request_template.md`. Evidence must cover the final revision. The owner may reject failed acceptance criteria without reviewing source code.
