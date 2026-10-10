# Documentation policy

Read when creating/adapting project documents or changing their responsibilities.

## One authoritative home per fact

| Information | Authoritative home |
| --- | --- |
| Approved purpose, requirements, constraints, non-goals, acceptance criteria | `docs/PRODUCT.md` |
| Current user behavior and practical instructions | Running software, `README.md` for entry steps, `docs/OWNER_GUIDE.md` for daily operation |
| Pending work | GitHub Issues when available; otherwise the handoff/PR records the unavailable tracking setup |
| Agent workflow and project validation commands | `AGENTS.md` |
| Executed checks, failures, evidence and review decisions | PR and CI; local verification report when no remote PR is available |
| Lasting technical decisions that merit explanation | Existing architecture/decision record; create one only for actual complexity |

The README introduces supported behavior and links to detail; it does not reproduce the product contract or owner's manual. The owner guide explains how to use and verify the software without reading source code. Examples of verification can link to acceptance criterion IDs; they need not copy the full requirements list. Temporary plans, debugging notes and completed work belong in Issues/PRs, not a growing set of Markdown files.

If implementation contradicts an approved requirement, report the discrepancy and fix the implementation or obtain a product decision. Do not rewrite the requirement to describe incomplete work. Clearly label assumptions and unresolved decisions; a proposed technology stack is not an approved product requirement.

## Adapt, preserve, and maintain

The files under `assets/templates/` are English writing aids, not a mandatory renderer or replacement operation. Inspect existing content first. Merge only missing useful guidance, preserve established rules, and explain substantive conflicts before replacing them. Adapt paths, commands, and optional sections to the real project. Resolve every `{{UPPER_SNAKE_CASE}}` token and remove adaptation comments and inapplicable sections from generated documents. Human-facing documents default to English unless the owner explicitly prefers another language; when translating them, update heading anchors and links as well. Keep agent instructions and technical references in accurate English.

Prefer editing a relevant existing document. Create a document only if someone will need it after this task. Keep entry documents readable in a short sitting; length is a judgment, not a hard threshold. Do not require every document to be read for a trivial change. Update documents when the behavior, command, decision or rule they describe changes, rather than on every commit.

Agents can maintain implemented usage, corresponding technical explanations and stale links within an authorized task. Substantial changes to approved requirements, development governance, security/privacy assumptions, user-data guarantees, or major architectural/operational commitments need explicit owner approval. Existing explicit approval counts: record the decision without asking for it again. A proposal may be drafted for review, but must be visibly proposed and must not be enforced as approved policy.

Before handoff, read the human documents together: commands must be executable, supported behavior must match actual software, limits must be visible, and evolving facts must not acquire contradictory homes. Documentation is supporting evidence, never proof that the software works.
