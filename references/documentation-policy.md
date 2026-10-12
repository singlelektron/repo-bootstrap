# Documentation policy

Read when creating or adapting project documents.

## One authoritative home per fact

| Information | Authoritative home |
| --- | --- |
| Project introduction and getting started | `README.md` |
| Approved requirements, constraints, non-goals, acceptance criteria | `docs/PRODUCT.md` |
| Human-readable operation, verification, troubleshooting, recovery | `docs/OWNER_GUIDE.md` |
| Durable project constraints, sources of truth, commands, authorization boundaries | `AGENTS.md` |
| Incorporated third-party materials, licenses or other legal bases, and sources | Existing notice records or `THIRD_PARTY_NOTICES.md`, when needed |
| Tasks, temporary discussions, change evidence, review history | Issues and PRs; local handoff when unavailable |

Link to the authoritative source instead of copying evolving facts. Add an
architecture/decision document only for a lasting commitment or complexity that
needs explanation; prefer existing records. Generated `AGENTS.md` must stand alone
after handoff, but should not prescribe planning, implementation steps, commit
timing, or extra review agents. Keep only useful persistent development context.

Approved requirements remain the contract. Label assumptions and proposals; do
not rewrite acceptance criteria to fit incomplete behavior. Record owner decisions
already authorized without asking again. Ordinary technical choices and usage-doc
maintenance are autonomous within scope; changes to approved commitments require
owner involvement under the [scope boundaries](../SKILL.md#scope-and-authority).

## Adapt and maintain

[Templates](../assets/templates/) are starting points, not overwrite operations.
Preserve existing authoritative documents and rules, resolve substantive conflicts,
and fill only useful gaps. Replace `{{UPPER_SNAKE_CASE}}` tokens, remove adaptation
comments and irrelevant sections, and supply concrete commands. Keep documents
concise; update them when their underlying behavior, command, or decision changes.

Human-facing output defaults to English unless the owner requests another language.
Update anchors and links when translating. Keep agent instructions and technical
references in accurate English. Check that user instructions match actual behavior,
commands work, and limitations are visible; documentation alone proves no behavior.
