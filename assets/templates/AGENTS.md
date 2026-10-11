<!-- Adapt paths, commands, and boundaries; resolve tokens and remove this comment. Keep instructions in English and merge with existing rules. -->
# Agent instructions

## Sources and project context

- `docs/PRODUCT.md`: approved requirements and acceptance criteria. Label assumptions; do not change approved criteria to fit incomplete work.
- `README.md`: introduction and getting started. `docs/OWNER_GUIDE.md`: operation, verification, and recovery.
- Issues/PRs: tasks, temporary discussion, verification evidence, and review history. Use a local handoff when unavailable.
- This file: durable constraints and development commands. Update the authoritative source when its facts change; link instead of duplicating.

Read what is relevant to the task. Human-facing docs default to English unless the
owner requests otherwise; agent instructions and technical references use English.

{{PROJECT_BOUNDARIES}}

## Authority and Git

Choose implementation and development strategy autonomously within the authorized
task. Routine reversible edits, checks, local commits, documentation maintenance,
and in-scope review fixes need no extra approval. Ask only for missing decisions or
authorization affecting material product/scope or governance commitments,
authorization boundaries, destructive actions, security/privacy/data guarantees,
important permissions, significant costs, or external publication/deployment.
Existing authorization counts.

Keep `{{DEFAULT_BRANCH}}` stable; use task branches or worktrees. Preserve unrelated
edits, data, and history, including staged/untracked work; never discard, stash,
stage, or commit unrelated work. Keep commits/PRs focused and traceable. Follow
repository conventions for branch names and merge method.

Remote creation, pushes, access/protection changes, publishing, and deployment
need authorization covering them. Authorization to open a PR covers its branch
publication, not merge. The owner may authorize merge in the initial task or after
PR review; do not request granted approval again. Once authorized, the agent may
merge and clean up merged task branches, respecting permissions and protections.

## Checks and acceptance

Run relevant commands from `{{VALIDATION_CONTEXT}}`:

```sh
{{VALIDATION_COMMANDS}}
```

Scale verification to consequences. Persistent data, money, authentication,
sensitive data, and destructive migrations need affected failure/recovery evidence;
use disposable data. Critical safety/security release needs a qualified human's
validation plan. Structural checks, tests, and AI review do not prove correctness.

When implementation and relevant local checks are complete, create a regular PR
ready for review; use a draft only for incomplete work or an explicit need for
early feedback. Completed work needs no draft-to-ready transition. Without remote authorization,
deliver a local diff/report. Use `.github/pull_request_template.md` for what/why, owner
verification steps, actual checks/CI/review results, and remaining risks or gaps.

Relevant CI must pass before merge; unavailable CI needs an explicit owner decision.
Allow CI and configured automated review, including Codex Code Review when
available, to run. Evaluate findings, fix confirmed correctness/security/data-integrity
issues, and justify declining stylistic or
unnecessary changes. Substantive revisions need affected checks and renewed review
when prior conclusions no longer hold; avoid endless review loops. AI comments are
not formal approving reviews or merge authorization. Do not require an independent
approving reviewer when none is eligible. Evidence must cover the delivered revision.
