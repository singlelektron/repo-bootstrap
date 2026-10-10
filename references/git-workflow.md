# Git and GitHub workflow

Read when initializing Git, adopting an existing repository, creating a PR, or recommending remote controls.

## Local lifecycle

Use the existing default branch, or `main` for a new repository. Keep one stable mainline and short-lived task branches; do not add permanent integration/release branches without a concrete need. One logical task normally produces one branch and one PR. Prefer meaningful commits and squash merge. Delete merged task branches automatically only where configured.

Inspect branch, status, remotes, recent history and applicable instructions before mutation. Record the initial state when adoption or a dirty tree makes preservation important. Never discard, reset, stash, amend, stage or commit unrelated user work. Use explicit paths for staging. If task work overlaps a user's edit and cannot be safely separated, preserve it and obtain the missing direction; do not clean the tree to make a check pass.

The development path is: understand the task → inspect → plan in proportion to scope → create a task branch → implement → commit → validate → self-review → draft PR → human review → merge only when authorized. Earlier checks during implementation are useful; the final commit must have relevant verification. If self-review changes code, commit and rerun affected checks. Disclose failed/skipped checks rather than presenting the PR as ready.

A new, empty repository may receive one controlled bootstrap commit before protection exists. After initialization, implementation belongs on a task branch. Existing repositories retain their branches/history and conventions unless a change is authorized. If a local-only repository has no remote, prepare a reviewable local branch, diff and PR-style report; do not fabricate a PR URL or publish merely to complete a checklist.

Routine reversible branch creation, focused edits, relevant tests and local commits are part of an authorized development task. Avoid repeated confirmation. Destructive operations, sensitive access changes and major product decisions require approval at their actual boundary. A request to implement does not authorize creating a remote repository, changing visibility, inviting collaborators, configuring remote secrets, publishing packages, deploying, pushing, or merging. Perform those actions only when the user's request/session explicitly covers them. Permission to open a PR includes its necessary branch publication; it does not include merge or deployment.

## Remote controls and honest status

For GitHub, recommend PRs for ordinary changes, relevant CI checks, no default-branch force pushes and no default-branch deletion. Retain a practical recovery path for the maintainer. A solo owner must be able to review and merge their own PR: do not require independent approvals when no eligible reviewer exists. High-risk technical review remains a risk decision even when branch settings cannot enforce it.

Discover the actual repository, available permissions and supported plan features before promising configuration. Some settings may be editable by the authenticated tools; others require owner/admin action or plan support. Remote mutation still needs authorization. Read back any changed settings and required check names. Record each control as verified, recommended/manual, unavailable, or unverified. Never equate a configuration file or successful API request with an active verified rule.

CI checks must correspond to real runnable project checks. A newly added workflow is configuration until a real run is observed; report hosted CI as not run/unverified until then. Do not add dummy success checks to satisfy protection requirements.
