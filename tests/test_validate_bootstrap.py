"""Behavior tests for the read-only, language-neutral bootstrap validator."""

import hashlib
import json
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest


VALIDATOR = Path(__file__).resolve().parents[1] / "scripts" / "validate-bootstrap.py"
DOCUMENTS = (
    "README.md", "AGENTS.md", "docs/PRODUCT.md", "docs/OWNER_GUIDE.md",
    ".github/pull_request_template.md",
)


@unittest.skipUnless(shutil.which("git"), "Git is needed for working-tree tests")
class BootstrapValidatorTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="repo-bootstrap-validator-")
        self.base = Path(self.temporary.name)
        self.repo = self.base / "repository"
        self.repo.mkdir()
        self.git("init", "-q")
        self.populate()

    def tearDown(self):
        self.temporary.cleanup()

    def git(self, *args):
        return subprocess.run(
            ["git", "-C", str(self.repo), *args], capture_output=True,
            text=True, check=True, timeout=10,
        ).stdout

    def write(self, relative, text):
        path = self.repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def populate(self):
        self.write(".gitignore", "# Project generated files\n*.cache\n")
        for name in DOCUMENTS:
            self.write(name, "# Project guide\nExplain current behavior, usage commands, limitations, and approval boundaries.\n")
        self.write(
            ".github/workflows/check.yml",
            "name: Checks\non: [push, pull_request]\njobs:\n  check:\n    runs-on: ubuntu-latest\n    steps:\n      - run: printf 'example'\n",
        )

    def run_validator(self, *args, repository=None):
        result = subprocess.run(
            [sys.executable, str(VALIDATOR), str(repository or self.repo), "--json", *args],
            capture_output=True, text=True, timeout=15,
        )
        self.assertEqual(result.stderr, "", result.stderr)
        return result.returncode, json.loads(result.stdout)

    def python_check(self, code):
        return shlex.join([sys.executable, "-c", code])

    def snapshot(self):
        return {
            str(path.relative_to(self.repo)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in self.repo.rglob("*") if path.is_file()
        }

    def test_unborn_repository_without_checks_is_structure_only(self):
        code, report = self.run_validator()
        self.assertEqual(code, 0)
        self.assertEqual(report["status"], "structure_only")
        self.assertEqual(report["executed_checks"], [])
        self.assertEqual(report["hosted_ci"]["status"], "unverified")
        self.assertTrue(any("No project checks" in item for item in report["warnings"]))

    def test_structural_validation_preserves_existing_bytes_and_git_state(self):
        self.write("existing.bin", "User data with trailing whitespace.  \n")
        self.git("add", ".")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "existing history")
        self.write("README.md", "# Existing owner rules\nOwner's edited usage and acceptance criteria stay exactly as written.\n")
        before = self.snapshot()
        status = self.git("status", "--porcelain")
        head = self.git("rev-parse", "HEAD")
        code, _ = self.run_validator()
        self.assertEqual(code, 0)
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(self.git("status", "--porcelain"), status)
        self.assertEqual(self.git("rev-parse", "HEAD"), head)

    def test_missing_documents_and_ci_fail(self):
        (self.repo / "docs/PRODUCT.md").unlink()
        shutil.rmtree(self.repo / ".github/workflows")
        code, report = self.run_validator()
        self.assertEqual(code, 1)
        failures = [item for item in report["structural_validation"]["checks"] if item["status"] == "failed"]
        self.assertTrue(any(item.get("path") == "docs/PRODUCT.md" for item in failures))
        self.assertTrue(any(item["name"] == "ci-configuration" for item in failures))

    def test_heading_and_comment_only_documents_fail(self):
        self.write("README.md", "# README\n<!-- Fill this in later with extensive useful instructions. -->\n## Usage\n---\n")
        code, report = self.run_validator()
        self.assertEqual(code, 1)
        self.assertTrue(any(item.get("path") == "README.md" and "stub" in item["detail"] for item in report["structural_validation"]["checks"]))

    def test_template_tokens_fail_but_github_expressions_are_allowed(self):
        self.write("README.md", "# Project\nRun the supported tool using {{RUN_COMMAND}} and verify its output.\n")
        code, report = self.run_validator()
        self.assertEqual(code, 1)
        self.assertTrue(any("Unresolved template" in item["detail"] for item in report["structural_validation"]["checks"]))
        self.populate()
        self.write(".github/workflows/check.yml", "name: Check\non: push\nenv:\n  TOKEN: ${{ secrets.TEST_TOKEN }}\njobs:\n  check: ordinary config\n")
        self.assertEqual(self.run_validator()[0], 0)

    def test_real_python_symbols_todo_prose_and_shell_variables_are_allowed(self):
        self.write("AGENTS.md", "# Python conventions\nThe __init__, __name__, and __main__ symbols have normal Python meanings.\nTrack ordinary TODO work in Issues. Read ${PROJECT_HOME} from the environment.\n")
        self.assertEqual(self.run_validator()[0], 0)
        self.write("AGENTS.md", "# Project conventions\nUse the documentation for __PROJECT_NAME__ to understand approved requirements.\n")
        self.assertEqual(self.run_validator()[0], 1)

    def test_documented_template_language_examples_are_allowed(self):
        self.write(
            "README.md",
            "# Greeting templates\nThe public examples render Hello, {{ user.name }}! "
            "or {{name}} and reference {{ PROJECT_TITLE }} in a real template language.\n",
        )
        self.assertEqual(self.run_validator()[0], 0)
        self.write(
            "README.md",
            "# Project guide\nInstall the project with {{INSTALL_COMMANDS}} before using it.\n",
        )
        self.assertEqual(self.run_validator()[0], 1)

    def test_ci_can_delegate_to_another_configuration(self):
        shutil.rmtree(self.repo / ".github/workflows")
        self.write(".gitlab-ci.yml", "include: ci.yml\n")
        self.assertEqual(self.run_validator("--ci-path", ".gitlab-ci.yml")[0], 0)

    def test_chinese_content_is_populated(self):
        self.write("docs/OWNER_GUIDE.md", "# 使用指南\n运行应用后输入姓名即可查看问候信息。修改设置前请备份数据，检查显示结果符合预期。\n")
        self.assertEqual(self.run_validator()[0], 0)

    def test_comment_only_gitignore_fails(self):
        self.write(".gitignore", "# Generated files should be ignored by the owner.\n")
        self.assertEqual(self.run_validator()[0], 1)

    def test_custom_ci_paths_replace_github_discovery(self):
        shutil.rmtree(self.repo / ".github/workflows")
        self.write(".gitlab-ci.yml", "check:\n  script:\n    - python -m unittest discover\n")
        self.write("ci/build.config", "build command = python -m compileall application\n")
        code, report = self.run_validator("--ci-path", ".gitlab-ci.yml", "--ci-path", "ci/build.config")
        self.assertEqual(code, 0)
        ci = [item["path"] for item in report["structural_validation"]["checks"] if item["name"] == "ci-configuration"]
        self.assertEqual(ci, [".gitlab-ci.yml", "ci/build.config"])

    def test_explicit_commands_run_in_repository_and_shell_metacharacters_are_literal(self):
        command = self.python_check("import os, sys; print(os.getcwd()); print(sys.argv[1])") + " " + shlex.quote("$(touch unwanted) ; $HOME")
        code, report = self.run_validator("--check", command, "--require-checks")
        self.assertEqual(code, 0)
        self.assertEqual(report["status"], "passed_with_local_checks")
        self.assertIn(str(self.repo), report["executed_checks"][0]["output"])
        self.assertIn("$(touch unwanted) ; $HOME", report["executed_checks"][0]["output"])
        self.assertFalse((self.repo / "unwanted").exists())
        self.assertEqual(report["hosted_ci"]["status"], "unverified")

    def test_failed_command_is_reported_and_later_command_still_runs(self):
        code, report = self.run_validator(
            "--check", self.python_check("import sys; print('known failure'); sys.exit(7)"),
            "--check", self.python_check("print('later check')"),
        )
        self.assertEqual(code, 1)
        first, second = report["executed_checks"]
        self.assertEqual(first["status"], "failed")
        self.assertEqual(first["returncode"], 7)
        self.assertIn("known failure", first["output"])
        self.assertEqual(second["status"], "passed")

    def test_require_checks_without_commands_fails(self):
        code, report = self.run_validator("--require-checks")
        self.assertEqual(code, 1)
        self.assertEqual(report["structural_validation"]["status"], "passed")
        self.assertTrue(report["errors"])

    def test_timeout_reports_failure(self):
        code, report = self.run_validator("--timeout", "0.3", "--check", self.python_check("import time; time.sleep(5)"))
        self.assertEqual(code, 1)
        self.assertEqual(report["executed_checks"][0]["status"], "timeout")
        self.assertLess(report["executed_checks"][0]["elapsed_seconds"], 3)

    @unittest.skipUnless(sys.platform != "win32", "Process-group termination is POSIX-specific")
    def test_timeout_covers_children_that_keep_output_pipe_open(self):
        command = self.python_check("import subprocess, sys; subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(5)']); print('parent finished')")
        code, report = self.run_validator("--timeout", "0.3", "--check", command)
        self.assertEqual(code, 1)
        self.assertEqual(report["executed_checks"][0]["status"], "timeout")
        self.assertIn("parent finished", report["executed_checks"][0]["output"])

    def test_missing_check_executable_is_reported(self):
        code, report = self.run_validator("--check", shlex.quote(str(self.base / "missing-executable")))
        self.assertEqual(code, 1)
        self.assertEqual(report["executed_checks"][0]["status"], "error")
        self.assertIn("Could not start", report["executed_checks"][0]["detail"])

    def test_output_is_bounded_and_non_utf8_output_does_not_crash(self):
        code, report = self.run_validator("--check", self.python_check("import sys; sys.stdout.buffer.write(b'\\xff' + b'x' * 1000000)"))
        self.assertEqual(code, 0)
        check = report["executed_checks"][0]
        self.assertTrue(check["output_truncated"])
        self.assertLessEqual(len(check["output"]), 16 * 1024)
        self.assertEqual(check["status"], "passed")

    def test_external_document_symlink_and_parent_path_fail(self):
        outside = self.base / "owner.md"
        outside.write_text("Private outside documentation with sufficient real content.\n", encoding="utf-8")
        target = self.repo / "docs/OWNER_GUIDE.md"
        target.unlink()
        target.symlink_to(outside)
        code, report = self.run_validator("--ci-path", "../owner.md")
        self.assertEqual(code, 1)
        failures = [item for item in report["structural_validation"]["checks"] if item["status"] == "failed"]
        self.assertTrue(any(item.get("path") == "docs/OWNER_GUIDE.md" and "outside" in item["detail"] for item in failures))
        self.assertTrue(any(item.get("path") == "../owner.md" and "outside" in item["detail"] for item in failures))

    def test_external_workflow_directory_symlink_fails(self):
        outside = self.base / "workflows"
        outside.mkdir()
        (outside / "check.yml").write_text("name: External check\non: push\njobs: elsewhere\n", encoding="utf-8")
        shutil.rmtree(self.repo / ".github/workflows")
        (self.repo / ".github/workflows").symlink_to(outside, target_is_directory=True)
        self.assertEqual(self.run_validator()[0], 1)

    def test_document_symlink_within_repository_is_allowed(self):
        target = self.repo / "docs/OWNER_GUIDE.md"
        target.unlink()
        target.symlink_to(self.repo / "README.md")
        self.assertEqual(self.run_validator()[0], 0)

    def test_invalid_utf8_is_a_structural_failure(self):
        (self.repo / "README.md").write_bytes(b"\xff\xfe invalid text")
        code, report = self.run_validator()
        self.assertEqual(code, 1)
        self.assertTrue(any(item.get("path") == "README.md" and "Cannot read" in item["detail"] for item in report["structural_validation"]["checks"]))

    def test_existing_git_worktree_and_subdirectory_are_supported(self):
        self.git("add", ".")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "initial")
        worktree = self.base / "worktree"
        self.git("worktree", "add", "-q", "-b", "test-adoption", str(worktree))
        self.assertTrue((worktree / ".git").is_file())
        code, report = self.run_validator(repository=worktree / "docs")
        self.assertEqual(code, 0)
        self.assertEqual(report["repository"], str(worktree))

    def test_directory_without_git_fails(self):
        shutil.rmtree(self.repo / ".git")
        code, report = self.run_validator()
        self.assertEqual(code, 1)
        self.assertTrue(any(item["name"] == "git-worktree" and item["status"] == "failed" for item in report["structural_validation"]["checks"]))

    def test_missing_directory_and_invalid_command_are_clear_failures(self):
        code, report = self.run_validator("--check", "'unterminated", repository=self.base / "missing")
        self.assertEqual(code, 1)
        self.assertEqual(report["executed_checks"][0]["status"], "error")
        code, report = self.run_validator("--check", self.python_check("print('unused')"), repository=self.base / "missing")
        self.assertEqual(code, 1)
        self.assertEqual(report["executed_checks"][0]["status"], "not_run")


if __name__ == "__main__":
    unittest.main()
