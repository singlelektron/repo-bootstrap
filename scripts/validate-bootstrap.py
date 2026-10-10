#!/usr/bin/env python3
"""Check bootstrap structure and, only when supplied, run local commands.

Uses the Python standard library. Structural mode does not write to the target
repository. Explicit --check commands may have their own side effects. An exit
code of zero does not establish application correctness or hosted CI success.
"""

import argparse
import json
import os
from pathlib import Path
import re
import shlex
import signal
import subprocess
import sys
import threading
import time


REQUIRED_DOCUMENTS = (
    "README.md",
    "AGENTS.md",
    "docs/PRODUCT.md",
    "docs/OWNER_GUIDE.md",
    ".github/pull_request_template.md",
)
MAX_FILE_BYTES = 1024 * 1024
MAX_OUTPUT_BYTES = 16 * 1024
TEMPLATE_TOKENS = re.compile(
    # Match this Skill's exact token convention, not ordinary Jinja/Handlebars
    # expressions or GitHub Actions expressions shown in project documentation.
    r"(?<!\$)(?-i:\{\{[A-Z][A-Z0-9_]*\}\})"
    r"|(?-i:__[A-Z][A-Z0-9_]{2,}__)"
    r"|<\s*(?:project[-_ ](?:name|description|purpose)|repository[-_ ](?:name|url)"
    r"|(?:install|run|test|check)[-_ ]command|command|owner|language)\s*>"
    r"|\[\s*(?:TODO|TBD|REPLACE_ME|FILL_IN)(?:\s[^\]\r\n]*)?\]",
    re.IGNORECASE,
)


def positive_seconds(value):
    try:
        result = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("timeout must be a positive number") from exc
    if not 0 < result < float("inf"):
        raise argparse.ArgumentTypeError("timeout must be a finite positive number")
    return result


def stop_process(process):
    """Terminate the check's process group on POSIX, including pipe-owning children."""
    try:
        if os.name == "posix":
            os.killpg(process.pid, signal.SIGKILL)
        else:
            process.kill()
    except ProcessLookupError:
        pass


def run_command(argv, repository, timeout, env=None):
    """Drain output continuously while retaining at most MAX_OUTPUT_BYTES bytes."""
    started = time.monotonic()
    result = {
        "argv": argv,
        "status": "error",
        "returncode": None,
        "output": "",
        "output_truncated": False,
    }
    try:
        process = subprocess.Popen(
            argv,
            cwd=repository,
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=False,
            start_new_session=os.name == "posix",
        )
    except (OSError, ValueError) as exc:
        result["detail"] = f"Could not start command: {exc}"
        result["elapsed_seconds"] = round(time.monotonic() - started, 3)
        return result

    retained = bytearray()
    observed = [0]
    read_errors = []

    def drain():
        try:
            with process.stdout:
                while True:
                    chunk = process.stdout.read(4096)
                    if not chunk:
                        break
                    observed[0] += len(chunk)
                    room = MAX_OUTPUT_BYTES - len(retained)
                    if room > 0:
                        retained.extend(chunk[:room])
        except OSError as exc:
            read_errors.append(str(exc))

    reader = threading.Thread(target=drain, daemon=True)
    reader.start()
    try:
        process.wait(timeout=timeout)
        reader.join(timeout=max(0, timeout - (time.monotonic() - started)))
        if reader.is_alive():
            raise subprocess.TimeoutExpired(argv, timeout)
        result["status"] = "passed" if process.returncode == 0 else "failed"
        if read_errors:
            result["status"] = "error"
            result["detail"] = "Could not capture command output: " + "; ".join(read_errors)
    except subprocess.TimeoutExpired:
        stop_process(process)
        process.wait()
        reader.join(timeout=1)
        result["status"] = "timeout"
        result["detail"] = f"Command exceeded {timeout:g} seconds, including output collection."
    except BaseException:
        stop_process(process)
        process.wait()
        reader.join(timeout=1)
        raise
    result["returncode"] = process.returncode
    result["output"] = bytes(retained).decode("utf-8", errors="replace")
    result["output_truncated"] = observed[0] > MAX_OUTPUT_BYTES or reader.is_alive()
    result["elapsed_seconds"] = round(time.monotonic() - started, 3)
    return result


def structural_check(name, status, detail, path=None):
    result = {"name": name, "status": status, "detail": detail}
    if path is not None:
        result["path"] = str(path)
    return result


def contained_path(repository, relative):
    path = Path(relative)
    if path.is_absolute():
        raise ValueError("Structural paths must be relative to the repository.")
    resolved = (repository / path).resolve()
    try:
        resolved.relative_to(repository)
    except ValueError as exc:
        raise ValueError("Path resolves outside the repository (including through symlinks).") from exc
    return resolved


def substantive_text(text, kind):
    if kind in ("gitignore", "ci-configuration"):
        return any(line.strip() and not line.lstrip().startswith("#") for line in text.splitlines())
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if kind == "document" and (
            stripped.startswith(("```", "~~~"))
            or re.fullmatch(r"[-=*_\s]+", stripped)
        ):
            continue
        lines.append(stripped)
    # This small Unicode-aware floor catches empty stubs. It cannot judge
    # whether prose, commands, ignore patterns, or CI behavior are appropriate.
    return sum(character.isalnum() for character in " ".join(lines)) >= 20


def check_file(repository, relative, kind):
    try:
        path = contained_path(repository, relative)
        if not path.is_file():
            return structural_check(kind, "failed", "Required regular file is missing.", relative)
        with path.open("rb") as stream:
            data = stream.read(MAX_FILE_BYTES + 1)
        if len(data) > MAX_FILE_BYTES:
            return structural_check(kind, "failed", "File exceeds the 1 MiB structural-read limit.", relative)
        text = data.decode("utf-8-sig")
    except (OSError, RuntimeError, ValueError) as exc:
        return structural_check(kind, "failed", f"Cannot read required file: {exc}", relative)
    tokens = TEMPLATE_TOKENS.findall(text)
    if tokens:
        preview = ", ".join(repr(token) for token in tokens[:3])
        return structural_check(kind, "failed", f"Unresolved template token(s): {preview}", relative)
    if not substantive_text(text, kind):
        return structural_check(kind, "failed", "File is empty or contains only a minimal stub.", relative)
    return structural_check(kind, "passed", "Present, populated, and no recognized template tokens.", relative)


def discover_ci(repository, ci_paths):
    if ci_paths:
        return list(dict.fromkeys(ci_paths)), None
    try:
        directory = contained_path(repository, ".github/workflows")
        if not directory.is_dir():
            return [], "No .github/workflows directory; use --ci-path for another CI provider."
        paths = sorted(
            str(path.relative_to(repository))
            for path in directory.iterdir()
            if path.suffix in (".yml", ".yaml")
        )
    except (OSError, RuntimeError, ValueError) as exc:
        return [], f"Cannot discover CI configuration: {exc}"
    return paths, None if paths else "No .yml or .yaml workflow found in .github/workflows."


def validate(repository, ci_paths, commands, timeout, require_checks):
    try:
        repository = Path(repository).expanduser().resolve()
    except (OSError, RuntimeError, ValueError) as exc:
        return {
            "schema_version": 1,
            "repository": str(repository),
            "status": "failed",
            "structural_validation": {
                "status": "failed",
                "checks": [structural_check("repository", "failed", f"Cannot resolve repository: {exc}")],
            },
            "executed_checks": [],
            "hosted_ci": {"status": "unverified", "detail": "Hosted CI was not inspected."},
            "warnings": ["Application correctness has not been established."],
            "errors": [],
        }
    checks = []
    errors = []
    warnings = []
    usable_directory = repository.is_dir()
    if not usable_directory:
        checks.append(structural_check("repository", "failed", "Repository directory does not exist.", repository))
    else:
        git_env = dict(os.environ)
        for key in (
            "GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_COMMON_DIR",
            "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES",
        ):
            git_env.pop(key, None)
        git_env["GIT_OPTIONAL_LOCKS"] = "0"
        git_result = run_command(
            ["git", "-C", str(repository), "rev-parse", "--show-toplevel", "--is-inside-work-tree"],
            repository, timeout, env=git_env,
        )
        lines = git_result["output"].strip().splitlines()
        if git_result["status"] == "passed" and len(lines) == 2 and lines[1] == "true":
            repository = Path(lines[0]).resolve()
            checks.append(structural_check("git-worktree", "passed", "Working tree found; a first commit is not required.", repository))
        else:
            detail = git_result.get("detail") or git_result["output"].strip() or "Not a Git working tree."
            checks.append(structural_check("git-worktree", "failed", detail, repository))
        checks.append(check_file(repository, ".gitignore", "gitignore"))
        checks.extend(check_file(repository, path, "document") for path in REQUIRED_DOCUMENTS)
        found_ci, ci_error = discover_ci(repository, ci_paths)
        if ci_error:
            checks.append(structural_check("ci-configuration", "failed", ci_error))
        checks.extend(check_file(repository, path, "ci-configuration") for path in found_ci)

    executed = []
    for command in commands:
        try:
            argv = shlex.split(command)
            if not argv:
                raise ValueError("Command is empty.")
        except ValueError as exc:
            executed.append({"command": command, "status": "error", "detail": f"Invalid command: {exc}", "argv": []})
            continue
        if not usable_directory:
            executed.append({"command": command, "argv": argv, "status": "not_run", "detail": "Repository directory is unavailable."})
            continue
        result = run_command(argv, repository, timeout)
        result["command"] = command
        executed.append(result)

    if not commands:
        warnings.append("No project checks supplied. Installation, build, tests, and runnable behavior remain unverified.")
        if require_checks:
            errors.append("--require-checks requires at least one explicit --check command.")
    warnings.append("Structural validation and passing local commands are not proof of application correctness.")
    structural_ok = all(check["status"] == "passed" for check in checks)
    commands_ok = all(check["status"] == "passed" for check in executed)
    status = "failed" if not structural_ok or not commands_ok or errors else (
        "passed_with_local_checks" if executed else "structure_only"
    )
    return {
        "schema_version": 1,
        "repository": str(repository),
        "status": status,
        "structural_validation": {"status": "passed" if structural_ok else "failed", "checks": checks},
        "executed_checks": executed,
        "hosted_ci": {"status": "unverified", "detail": "Configuration presence does not verify hosted CI execution."},
        "warnings": warnings,
        "errors": errors,
    }


def print_report(report):
    print(f"Repository: {report['repository']}")
    print(f"Structural validation: {report['structural_validation']['status']}")
    for check in report["structural_validation"]["checks"]:
        label = check.get("path", check["name"])
        print(f"  {check['status'].upper()}: {label}: {check['detail']}")
    print("Local commands: " + ("none supplied" if not report["executed_checks"] else "explicitly executed"))
    for check in report["executed_checks"]:
        print(f"  {check['status'].upper()}: {check['command']}")
        if check.get("detail"):
            print("    " + check["detail"])
        if check.get("output"):
            print(check["output"].rstrip())
        if check.get("output_truncated"):
            print(f"    Output limited to the first {MAX_OUTPUT_BYTES} bytes.")
    print("Hosted CI: unverified")
    for message in report["errors"]:
        print("ERROR: " + message)
    for message in report["warnings"]:
        print("WARNING: " + message)
    print(f"Result: {report['status']}")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", nargs="?", default=".", help="Repository directory (default: current directory; subdirectories resolve to the Git root).")
    parser.add_argument("--ci-path", action="append", default=[], metavar="PATH", help="Exact repository-relative CI configuration file; repeat for multiple files. Replaces GitHub workflow discovery.")
    parser.add_argument("--check", action="append", default=[], metavar="COMMAND", help="Explicit local command; repeat to run several. POSIX shlex tokenization, shell=False, noninteractive, repository root as cwd.")
    parser.add_argument("--timeout", type=positive_seconds, default=120.0, metavar="SECONDS", help="Timeout for each command, including Git inspection (default: 120 seconds).")
    parser.add_argument("--require-checks", action="store_true", help="Fail when no explicit --check command is supplied.")
    parser.add_argument("--json", action="store_true", help="Emit one JSON report instead of human-readable text.")
    args = parser.parse_args(argv)
    try:
        report = validate(args.repository, args.ci_path, args.check, args.timeout, args.require_checks)
    except KeyboardInterrupt:
        print("Validation interrupted.", file=sys.stderr)
        return 130
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_report(report)
    return 1 if report["status"] == "failed" else 0


if __name__ == "__main__":
    sys.exit(main())
