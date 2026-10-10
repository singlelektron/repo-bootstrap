# Maintaining this Skill

This repository contains a reusable skill, not a bootstrapped application.
`SKILL.md` is the entry point; references hold conditional policy and
`assets/templates/` holds project starting points. Do not render templates into
this repository or apply a sample project's product requirements here.

Keep instructions concise, language-agnostic and self-contained after handoff.
Preserve user authorization boundaries. Change templates and instructions together
when their actual behavior changes; avoid duplicate policy sources.
Keep this repository's README bilingual in English and Chinese. Author all other
agent/maintainer documentation and template sources in accurate English. Generated
human-facing project documentation defaults to English unless the owner explicitly
requests another language. Preserve non-English test data needed to verify Unicode.

Work on a task branch after the initial bootstrap commit. Commit only task changes.
Run `python3 -m unittest discover -s tests -v`; run the available official skill
metadata validator when changing frontmatter. Tests need Python 3.10+ and Git;
the structural helper uses only the standard library.

For substantial workflow changes, forward-test the relevant scenario from
`tests/SCENARIOS.md` through an independent agent in a disposable directory.
Preserve evidence and report actual checks, unverified CI and approval gaps.
Never use real user data, publish, deploy or merge as part of a test.
