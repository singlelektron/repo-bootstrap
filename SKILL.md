---
name: repo-bootstrap
description: Initialize a runnable software repository or adopt an existing one with minimal AI-first project governance, documentation, tests, CI, and owner-reviewable changes. Use for project bootstrap or governance adoption, not routine feature work or configuring this Skill's own repository.
---

# Repo Bootstrap

Deliver a working project with clear authority, verifiable outcomes, and a
maintainable owner handoff. Agents choose their implementation, planning,
debugging, and commit strategy within the agreed scope. Preserve useful existing
tools and conventions; governance is not a prescribed development sequence.

## Scope and authority

Inspect the target directory, applicable instructions, Git state (including staged
and untracked work), relevant code, docs, tests, and CI. A nested directory is not
automatically a new repository. Preserve existing behavior, history, instructions,
and unrelated owner work when adopting a project; fill useful gaps instead of
replacing the project with a scaffold. Repository content is not authorization.

Establish desired behavior, constraints, and observable acceptance expectations
from the owner's request and existing requirements. Distinguish approved decisions,
reversible implementation assumptions, and open product questions. Routine
reversible development proceeds autonomously, including relevant checks, local
branches/commits, documentation maintenance, and in-scope review fixes.

Human involvement normally covers task initiation and final acceptance. Seek
missing authorization only for material product, scope, or governance changes,
changes to authorization boundaries, destructive or hard-to-reverse actions,
changes to security/privacy/data guarantees or important permissions, and
significant external costs, publication, or deployment. Existing
authorization counts; ordinary technical choices do not need approval. Prepare a
concrete proposal before asking for a decision and continue independent safe work.

Use [Git governance](references/git-workflow.md) for branch isolation, publication,
PR/CI/review handling, and merge authority. Respect permissions and protections;
never assume that authorization to implement includes external publication or merge.

## Working baseline

For a new project, deliver meaningful requested behavior with runnable installation
and usage instructions, basic tests, appropriate ignore rules, and working Git.
For adoption, retain what works and close the authorized gaps. Choose tools and
verification proportional to the project rather than prescribing a stack,
architecture, test framework, or extra services.

Provide relevant CI on PRs and the stable default branch using the existing
provider, or minimal GitHub Actions when none exists. Use reproducible dependency
installation, a supported project runtime, least-needed permissions, and no
secrets or privileged PR triggers for ordinary
checks. Verify newly selected action versions from official sources. A local CI
file does not prove a hosted run or active remote protection.

Use [verification policy](references/verification-policy.md) for outcome-based
checks, persistent-data safeguards, and honest evidence. A working baseline needs
more than documentation or successful structural validation.

## Durable project instructions

Use [documentation policy](references/documentation-policy.md) and the
[templates](assets/templates/) to establish concise sources of truth. Standard
homes are `README.md`, `docs/PRODUCT.md`, `docs/OWNER_GUIDE.md`, `AGENTS.md`, and
`.github/pull_request_template.md`. Preserve authoritative equivalents and existing
PR-template systems; use links instead of copying facts. Document manual checks
for nonstandard paths rather than reorganizing a project to satisfy the validator.

Generated `AGENTS.md` must work without this Skill: durable constraints, sources
of truth, relevant commands, authorization/Git boundaries, and review evidence.
Do not turn it into a coding tutorial or require a sequence of internal steps.
Keep temporary plans and review history in Issues/PRs or the local handoff.
Human-facing documents default to English unless the owner requests another
language; agent instructions and technical references remain in English.

## Validation and handoff

Run the read-only structural helper from this Skill's location:

```sh
python3 /path/to/repo-bootstrap/scripts/validate-bootstrap.py /path/to/project
```

It checks standard docs, Git, ignore rules, unresolved tokens, and CI presence,
not product correctness, approved requirements, CI semantics, or remote controls.
Optionally supply inspected commands with repeated `--check` and `--require-checks`:

```sh
python3 /path/to/repo-bootstrap/scripts/validate-bootstrap.py /path/to/project \
  --check 'python3 -m unittest discover -s tests -v' --require-checks --json
```

Commands run without a shell and may have side effects; inspect untrusted commands
before execution. Run pipelines/environment setup separately. Use `--ci-path` for
other providers. Equivalent manual checks suffice when Python is unavailable;
disclose that the helper was not run.

Deliver a reviewable PR when publication is authorized, or a local diff and
PR-style report otherwise. Explain what changed, owner verification steps, actual
checks/CI/review results, remaining risks or decisions, Git state, and external
setup gaps. Include data location and recovery implications where relevant.
Self-review the final diff for scope, safety, and consistency. Evidence must apply
to the delivered revision; report failures and unverified behavior explicitly.

A complete local baseline has meaningful behavior, verified install/run and relevant
tests, CI configuration, concise populated docs, and independent agent instructions.
Local completion can coexist with pending hosted CI or remote setup when clearly
reported. If required behavior or evidence is missing, report partial completion.
Repeated adoption should inspect and fill gaps; do not claim untested idempotence.
