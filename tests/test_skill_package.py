"""Check that the installed skill can actually find its bundled resources."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PackageTests(unittest.TestCase):
    def test_instruction_links_resolve_inside_package(self):
        # Relative file links are also the navigation API for compatible agents.
        for document in [ROOT / "SKILL.md", *sorted((ROOT / "references").glob("*.md"))]:
            for target in re.findall(r"\]\(([^)]+)\)", document.read_text(encoding="utf-8")):
                if "://" in target or target.startswith("#"):
                    continue
                path = (document.parent / target.split("#", 1)[0]).resolve()
                with self.subTest(document=document.name, target=target):
                    self.assertTrue(path.is_relative_to(ROOT))
                    self.assertTrue(path.exists(), f"Missing bundled resource: {path}")

    def test_metadata_discovery_contract(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        frontmatter = skill.split("---\n", 2)[1]
        # This package intentionally uses only plain scalar name/description.
        fields = dict(line.split(": ", 1) for line in frontmatter.strip().splitlines())
        self.assertEqual(fields["name"], ROOT.name)
        self.assertRegex(fields["name"], r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
        self.assertGreater(len(fields["description"].strip()), 0)
        self.assertLessEqual(len(fields["description"]), 1024)
        self.assertTrue(skill.split("---\n", 2)[2].strip())


if __name__ == "__main__":
    unittest.main()
