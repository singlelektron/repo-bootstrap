# Git and PR governance

Read when establishing Git boundaries, delivering a PR, or assessing remote controls.

## Isolation and preservation

Keep the stable default branch free of ordinary direct development. Use task
branches or worktrees suited to the change and existing conventions. A new empty
repository may receive an initial bootstrap commit; later development is isolated.
Keep commits and PRs traceable and reasonably scoped, without a fixed count,
sequence, naming scheme, or permanent branching model.

Preserve unrelated owner edits, staged/untracked files, data, and history. Never
reset, discard, stash, amend, stage, or commit unrelated work. Inspect staged
content and use explicit task paths. If overlapping edits cannot be safely
separated, isolate the work or obtain the missing direction.

Local reversible Git work is covered by an authorized task. Remote creation,
pushes, visibility/collaborator/secret/protection changes, publication, and
deployment need authorization covering those actions. Permission to open a PR
includes necessary branch publication, not deployment or merge. Without remote
authorization or access, deliver a local branch, diff, and PR-style report.

## PR, CI, and review

The normal handoff is an owner-defined task, autonomous development, a reviewable
PR, CI and available review, in-scope fixes, and owner acceptance. This describes
decision boundaries, not a mandatory implementation sequence. When implementation
and relevant local verification are complete, create a regular PR ready for review.
Use a draft only for incomplete work or an explicit need for early feedback; do
not require a draft-to-ready transition for completed work. Allow CI and available
automated review to run, address substantive findings, and provide concise evidence
for owner acceptance. Disclose outstanding verification and approval gaps.

Relevant CI checks must pass before merging. Report actual runs for the delivered
revision, distinguishing configured checks from observed results. When hosted CI
is unavailable, disclose the gap for an explicit owner decision; local checks do
not establish hosted success. Never add dummy checks or bypass repository rules.

Use Codex Code Review when available and configured for the repository; do not
assume account-level availability guarantees a review on every PR. Report review
availability and results honestly. It is supplemental, not another required review
framework or proof of correctness. AI comments are distinct from formal GitHub
approving reviews and from owner authorization to merge. Do not require an
independent approving reviewer where none is eligible; respect existing protections.

Evaluate findings: address confirmed correctness, security, and data-integrity
issues within scope. Decline stylistic suggestions or unnecessary refactoring
with a reason. Escalate findings that require new product or authorization
decisions. Substantive changes after review need affected verification and renewed
review when the change invalidates prior conclusions. Avoid open-ended automated
review/fix loops; surface unresolved substantive issues in the handoff.

Merge requires authorization covering that action. The owner may grant it in the
initial task or after reviewing the PR; do not ask again for authorization already
granted. Once authorized, the agent may merge and perform routine cleanup of
merged task branches, subject to repository protections. Use merge commit, squash,
or rebase according to project conventions and the structure of the changes.
Respect permissions, required checks, and branch protection.

## Remote controls

Recommend PRs, relevant required checks, and protection against default-branch
force pushes/deletion, with a practical maintainer recovery path. Verify repository
permissions and supported features before claiming settings can be configured.
Change controls only when authorized and read them back. Distinguish verified,
recommended/manual, unavailable, and unverified controls; a local configuration
file or successful API request alone does not prove enforcement.
