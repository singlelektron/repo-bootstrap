# repo-bootstrap

English / 简体中文

A reusable Agent Skill for AI-first projects: initialize a runnable project or adopt an existing repository with minimal governance for scope, Git, verification, and owner acceptance.

面向主要由 AI 编程代理开发的项目：初始化可运行的软件，或接入已有仓库，为任务范围、Git、验证和负责人验收建立最小治理规则。

Agents choose their implementation approach within the authorized scope, preserving existing tools and conventions. Templates and validation helpers support real project behavior and an understandable handoff. **English is the default output language.** Human-facing project documents use another language when explicitly requested; agent instructions, technical references, and template sources remain English. This README is bilingual.

代理在授权范围内自主选择实现方式，保留已有工具和约定；模板与校验器辅助实现真实功能，并形成易于理解的交付。**默认输出语言为英文。** 负责人明确要求时，人类文档可使用其他语言；代理指令、技术参考资料和模板源文件保持英文。本 README 使用中英双语。

## Contents / 文件结构

| Path | Responsibility / 职责 |
| --- | --- |
| `SKILL.md` | Entry point, scope, completion evidence, authorization boundaries / 入口、范围、交付证据和授权边界 |
| `agents/openai.yaml` | Codex UI metadata and invocation prompt / Codex 显示信息和调用提示 |
| `references/documentation-policy.md` | Documentation authority, maintenance, and approval / 文档权威位置、维护与审批 |
| `references/git-workflow.md` | Git boundaries, PR review, and remote controls / Git 边界、PR 审查和远端控制 |
| `references/verification-policy.md` | Proportionate evidence and owner verification / 按风险提供证据与负责人验收 |
| `assets/templates/README.md` | Project introduction and run instructions / 项目介绍与运行说明模板 |
| `assets/templates/AGENTS.md` | Durable constraints, context, commands, and authority / 持久约束、上下文、命令和授权模板 |
| `assets/templates/PRODUCT.md` | Approved requirements, assumptions, and acceptance criteria / 已批准需求、假设与验收标准模板 |
| `assets/templates/OWNER_GUIDE.md` | Usage, verification, updates, troubleshooting, recovery / 使用、验收、更新、排查与恢复模板 |
| `assets/templates/pull_request_template.md` | Human Review and Technical Verification / 人类验收与技术验证表单 |
| `scripts/validate-bootstrap.py` | Structural checks and explicitly selected local commands / 结构检查与明确指定的本地命令 |
| `tests/test_validate_bootstrap.py` | Validator behavior and failure-path tests / 校验器行为与失败路径测试 |
| `tests/test_skill_package.py` | Metadata and bundled resource checks / 元数据与资源链接检查 |
| `tests/SCENARIOS.md` | Actual forward-test scenarios, results, and limitations / 实际代理测试场景、结果与限制 |
| `.github/workflows/check.yml` | Automated tests for this Skill / 本 Skill 的自动测试配置 |
| `AGENTS.md`, `.gitignore` | Maintenance instructions and generated-file exclusions / 仓库维护约定与生成物忽略规则 |

Adapt templates rather than overwriting existing files. Replace `{{UPPER_SNAKE_CASE}}`, remove irrelevant sections and adaptation comments, and keep linked heading anchors correct when translating output. Load references only when needed; do not copy the entire Skill into each generated project's instructions.

模板应按项目调整，不直接覆盖已有文件。替换 `{{UPPER_SNAKE_CASE}}`，删除无关章节和适配注释；翻译生成文档时同步修正标题锚点。按需读取参考资料，不把整个 Skill 复制成每个项目的代理指令。

## Installation and invocation / 安装与调用

The repository root is the `repo-bootstrap` Skill directory. Install the complete directory or a symlink; no package installer, connector, or custom service is required. Follow the [official Codex skill locations](https://learn.chatgpt.com/docs/build-skills): user scope is `~/.agents/skills/repo-bootstrap`; project scope is `.agents/skills/repo-bootstrap`.

仓库根目录就是 `repo-bootstrap` Skill。安装完整目录或符号链接即可，无需包安装器、连接器或自定义服务。按 [Codex 官方位置说明](https://learn.chatgpt.com/docs/build-skills)，用户范围使用 `~/.agents/skills/repo-bootstrap`，项目范围使用 `.agents/skills/repo-bootstrap`。

User scope / 用户范围：

```sh
mkdir -p "$HOME/.agents/skills"
ln -s /absolute/path/to/repo-bootstrap "$HOME/.agents/skills/repo-bootstrap"
```

Project scope, from the target repository / 在目标仓库执行，安装到项目范围：

```sh
mkdir -p .agents/skills
ln -s /absolute/path/to/repo-bootstrap .agents/skills/repo-bootstrap
```

Inspect an existing destination before changing it; do not force-overwrite it. For a shared repository, copy the complete directory with its `repo-bootstrap` name instead of committing a machine-specific absolute symlink. Avoid duplicate installations of the same name. Codex detects skill changes; restart it if the Skill does not appear.

目标名称已存在时，先检查现有安装，不强制覆盖。若要随仓库共享，复制完整目录并保留 `repo-bootstrap` 名称，不提交只适用于本机的绝对路径链接。避免重复安装同名 Skill；若没有被发现，重启 Codex 后再检查。

Invoke `$repo-bootstrap`, or describe a matching task for automatic selection. Without installation, ask the agent to read this repository's `SKILL.md` by its absolute path.

使用 `$repo-bootstrap` 调用，也可通过匹配的任务描述自动选择。未安装时，可让代理读取本仓库 `SKILL.md` 的绝对路径。

New project / 新项目：

```text
$repo-bootstrap Create a local todo CLI in /path/to/new-project.
Support adding and listing tasks, with data readable after restarting.
Target Linux and prefer simple tools. Use English documentation by default.
Initialize local Git and make task commits; deliver a locally verifiable baseline.
```

```text
$repo-bootstrap 在 /path/to/new-project 创建本地待办 CLI。
支持添加和列出任务，重启后仍能读取数据。目标 Linux，优先简单工具。
文档默认英文；允许初始化本地 Git 和任务提交，先交付本地可验收版本。
```

Existing project / 已有项目：

```text
$repo-bootstrap Adopt /path/to/existing-project into minimal AI-first project governance.
Preserve current behavior, tools, and uncommitted work; inspect AGENTS, tests, and CI first.
Fill documentation gaps and propose major governance changes for approval.
Make local changes only.
```

```text
$repo-bootstrap 为 /path/to/existing-project 建立最小 AI 项目治理规则。
保留行为、工具和未提交工作，先检查 AGENTS、测试与 CI。
补足缺失文档，重大治理修改提出具体方案供审批；仅做本地更改。
```

The owner defines the task and acceptance expectations; the agent develops autonomously. When implementation and relevant local checks are complete and publication is authorized, create a regular PR ready for review. Drafts are for incomplete work or an explicit need for early feedback; completed work needs no draft-to-ready transition. Allow CI and available Codex Code Review to run, address substantive findings, and provide concise acceptance evidence. AI comments are not formal GitHub approval or proof of correctness. Relevant CI must pass before merge; disclose unavailable checks. The owner may authorize merge in the initial task or after PR review. That authorization covers merge and routine cleanup of merged task branches, subject to repository protections; do not request it again. Choose the merge method to fit the changes and repository conventions.

负责人定义任务与验收预期，代理自主开发。实现与相关本地验证完成且发布获授权后，直接创建可审查的普通 PR。仅在工作未完成或明确需要提前反馈时使用草稿，已完成工作无需经过草稿转正式的步骤。让 CI 和可用的 Codex Code Review 运行，处理实质问题并提供简明验收证据。AI 评论不等于 GitHub 正式批准，也不证明正确性。合并前须通过相关 CI，不可用的检查需明确披露。负责人可在初始任务或 PR 审查后授权合并；授权涵盖合并及已合并任务分支的常规清理，并须遵守仓库保护规则，无需重复确认。合并方式依变更结构和仓库约定选择。

Routine reversible development needs no repeated approval. Ask only for missing material product decisions, destructive operations, changed security/privacy/data guarantees or important permissions, significant external costs/publication/deployment, or substantial scope expansion not already authorized. Permission to create a PR covers its necessary branch publication, not merge or deployment.

常规可逆开发无需重复审批。仅对尚未授权的重要产品决策、破坏性操作、安全或隐私及数据保证或重要权限变更、重大外部费用或发布部署，以及明显超出任务范围的工作，请求必要决定。创建 PR 的授权包含所需分支推送，不包含合并或部署。

## Validator / 校验器

The helper requires Python 3.10+ and Git, with no third-party Python dependencies. It imposes no programming language on the project.

辅助工具需要 Python 3.10+ 和 Git，无第三方 Python 依赖，不限制项目使用的编程语言。

```sh
python3 scripts/validate-bootstrap.py /path/to/project
python3 scripts/validate-bootstrap.py /path/to/project \
  --check 'python3 -m unittest discover -s tests -v' --require-checks --json
python3 scripts/validate-bootstrap.py /path/to/project --ci-path .gitlab-ci.yml
python3 scripts/validate-bootstrap.py --help
```

Default checks cover Git, `.gitignore`, five standard documents, recognized unresolved placeholders, document stubs, and GitHub Actions file presence. Repeat `--ci-path` for other providers' repository-relative files. Repeat `--check` for inspected commands, each executed at the Git root without a shell; `--timeout` limits each command.

默认检查 Git、`.gitignore`、五份标准文档、已识别的未填写占位符、空壳文档，以及 GitHub Actions 文件是否存在。`--ci-path` 可重复指定其他 CI 文件的仓库相对路径；`--check` 可重复提供经过检查的命令，每条在 Git 根目录运行，不经过 shell，支持 `--timeout`。

Structural mode is read-only. Explicit commands may have side effects; inspect them first. Run pipelines, redirects, and environment setup separately. Missing structure, failed commands, and timeouts return nonzero. With no commands, exit zero means only structural checks passed; `--require-checks` rejects omission. JSON separates structure, executed commands, and unverified hosted CI.

结构模式只读；显式命令可能有副作用，执行前应检查。流水线、重定向和环境设置需单独运行。缺失结构、命令失败或超时返回非零。未提供命令时，返回零仅表示结构通过；`--require-checks` 可拒绝这种情况。JSON 分开呈现结构、实际命令结果和未验证的托管 CI。

## Maintenance and verification / 维护与验证

```sh
python3 -m unittest discover -s tests -v
```

Validate metadata with the available official `skill-creator/scripts/quick_validate.py` or `skills-ref validate`. These maintenance tools are not installation dependencies. The package follows the [Agent Skills specification](https://agentskills.io/specification). See [actual scenario results](tests/SCENARIOS.md) for the original independent executions and their limits; those scenarios explicitly requested Chinese project documentation and do not define the current English default.

可用官方 `skill-creator/scripts/quick_validate.py` 或 `skills-ref validate` 检查元数据；它们是维护工具，不是安装依赖。包结构遵循 [Agent Skills 规范](https://agentskills.io/specification)。[实测记录](tests/SCENARIOS.md) 保留最初独立执行的结果与限制；那些场景明确要求中文项目文档，不代表当前的英文默认值。

## Limitations / 限制

- Structure and passing commands do not prove correctness, approved requirements, valid CI semantics, or active remote protections. / 结构与命令通过不证明软件正确、需求获批、CI 语义正确或远端保护生效。
- Verify hosted CI, permissions, plan support, and deployment separately. A local baseline can be complete without a remote, with external setup clearly disclosed. / 托管 CI、权限、计划支持和部署需单独核实；本地基线可以完成，同时明确列出外部设置缺口。
- There is no built-in merge, migration, or global-install command. / 不提供内置的合并、迁移或全局安装命令。
- Existing nonstandard document and PR-template paths may need manual checks; do not reorganize a project solely for this validator. / 非标准文档和 PR 模板路径可能需要人工检查，不为校验器强制重组项目。
- Repeated adoption inspects before filling gaps; full idempotence across all projects is not claimed. / 重复接入先检查再补缺，不声称对所有项目完全幂等。
- Command parsing uses POSIX-style `shlex`; Windows and complex command environments need separate verification. / 命令参数使用 POSIX 风格解析；Windows 和复杂命令环境需另行验证。
