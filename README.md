# repo-bootstrap

给主要由 AI 编程代理开发的个人软件项目建立一个小而可靠的起点：可运行的功能、实际测试、CI、少量长期文档，以及无需逐行看源码的验收流程。支持新项目初始化和已有仓库接入；技术栈由项目决定。

这是可直接读取的 Agent Skill，不是固定语言的脚手架生成器。代理仍需根据真实需求实现程序；模板和校验器只辅助它工作。

## 内容

| 路径 | 职责 |
| --- | --- |
| `SKILL.md` | 元数据、分阶段工作流程、成功条件和授权边界 |
| `agents/openai.yaml` | Codex 显示名称、简介和默认调用提示 |
| `references/documentation-policy.md` | 文档权威位置、维护和审批规则 |
| `references/git-workflow.md` | 单主线开发、本地与远端边界、单人仓库保护建议 |
| `references/verification-policy.md` | 风险等级、验证深度和两层 PR 证据 |
| `assets/templates/README.md` | 项目入口文档起点 |
| `assets/templates/AGENTS.md` | 不依赖原 Skill 的后续代理指令起点 |
| `assets/templates/PRODUCT.md` | 已批准需求、假设、非目标和可观察验收标准 |
| `assets/templates/OWNER_GUIDE.md` | 运行、验收、更新、故障处理及适用的数据恢复步骤 |
| `assets/templates/pull_request_template.md` | 人类验收与技术验证表单 |
| `scripts/validate-bootstrap.py` | 只读结构检查；可选择执行明确指定的命令 |
| `tests/test_validate_bootstrap.py` | 校验器的正常、失败、安全与保留行为测试 |
| `tests/test_skill_package.py` | Skill 元数据约束和内部资源链接检查 |
| `tests/SCENARIOS.md` | 独立代理实测任务、结果和验证限制 |
| `.github/workflows/check.yml` | 本 Skill 的自动测试配置 |
| `AGENTS.md`、`.gitignore` | 本 Skill 仓库的维护约定和生成物忽略规则 |

模板需按项目编辑，替换 `{{UPPER_SNAKE_CASE}}`，删除不适用内容。已有文件通过最小补充接入，不直接覆盖。Skill 只在需要时加载相关参考资料，不将整个资料包复制到每个项目。

## 安装与调用

当前目录本身就是 `repo-bootstrap` Skill。安装只需放置完整目录或创建符号链接，不需要 Python 包安装器、连接器或插件服务。

按 [Codex 官方安装位置说明](https://learn.chatgpt.com/docs/build-skills)，可以在用户范围放到 `~/.agents/skills/repo-bootstrap`，或在目标项目中放到 `.agents/skills/repo-bootstrap`。Codex 支持符号链接。以下是手动安装示例，本次交付没有执行安装：

```sh
mkdir -p "$HOME/.agents/skills"
ln -s /absolute/path/to/repo-bootstrap "$HOME/.agents/skills/repo-bootstrap"
```

项目范围则在目标仓库执行：

```sh
mkdir -p .agents/skills
ln -s /absolute/path/to/repo-bootstrap .agents/skills/repo-bootstrap
```

如果目标名称已存在，先检查现有安装；不要强制覆盖。若需要让他人随仓库使用，复制完整 Skill 目录并保留名称，而不是提交只适用于本机的绝对路径链接。避免在多个范围重复安装同名 Skill。Codex 会发现 Skill 变化；若没有出现，重启后再检查。

在 Codex 中用 `$repo-bootstrap` 调用，也可由任务描述自动匹配。未安装时，可以直接让代理读取本目录下 `SKILL.md` 的绝对路径并执行。

新项目示例：

```text
$repo-bootstrap 在 /path/to/new-project 创建一个本地待办 CLI。
用户是我自己，支持添加和列出待办，重启后仍能读取数据。
目标 Linux，优先简单工具；人类文档用中文。
允许初始化本地 Git 和任务提交；先做本地可验收版本。
```

已有项目示例：

```text
$repo-bootstrap 为 /path/to/existing-project 接入最小 AI 开发流程。
保持现有行为、工具和未提交工作，先检查现有 AGENTS、测试与 CI。
补足缺失文档，重大治理修改先提出具体方案；仅做本地更改。
```

如果需要推送、创建远端仓库、调整保护规则、发布或部署，请在请求中明确授权对应动作。普通的可逆实现与验证不需要重复确认；合并仍需授权。

## 校验器

结构检查仅需要 Python 3.10+ 和 Git，无第三方 Python 依赖。项目本身可以使用其他语言。

```sh
python3 scripts/validate-bootstrap.py /path/to/project
python3 scripts/validate-bootstrap.py /path/to/project \
  --check 'python3 -m unittest discover -s tests -v' --require-checks --json
python3 scripts/validate-bootstrap.py /path/to/project --ci-path .gitlab-ci.yml
python3 scripts/validate-bootstrap.py --help
```

默认检查 Git、`.gitignore`、五份标准文档和 GitHub Actions 配置，拒绝未填写模板和空壳文档。`--ci-path` 可重复指定其他 CI 文件；路径必须属于仓库。`--check` 可重复，每条命令在仓库根目录运行，使用参数拆分而非 shell，支持 `--timeout`。

默认只读；显式指定的检查命令可能产生文件、访问数据或其他副作用，执行前应检查其内容。流水线、重定向和环境变量设置需要单独运行，不要期待 shell 展开。

缺失结构、检查命令失败或超时会返回非零。没有检查命令时，即使返回零，也只表示结构检查通过；`--require-checks` 可使未执行命令的情况失败。JSON 分开呈现结构检查、实际执行结果和未验证的远端 CI。

## 维护与验证

```sh
python3 -m unittest discover -s tests -v
```

元数据还应使用官方 `skill-creator/scripts/quick_validate.py` 或 Agent Skills 的 `skills-ref validate` 校验；这些是维护工具，不是使用本 Skill 的安装依赖。包格式遵循 [Agent Skills 规范](https://agentskills.io/specification)。实际执行证据与三个临时项目的交接结果见 [实测记录](tests/SCENARIOS.md)。

## 限制

- 结构检查不证明程序正确、文档中的需求已获批准、CI 语义正确或 GitHub 保护规则已生效。
- 外部权限、计划支持、CI 托管执行和部署必须单独核实；没有远端也能完成本地基线并提供可评审差异。
- 无自动合并、数据迁移或全局安装功能；Skill 通过代理执行授权范围内的工作。
- 已有仓库的非标准文档/PR 模板可以保留，但标准路径校验可能需要人工补充。不会为校验器强制重组项目。
- 重复接入先检查再补缺。本次测试覆盖代表场景，不声称所有项目和技术栈完整幂等。
- Python 命令检查使用 POSIX 风格的参数拆分；Windows、复杂命令与其他运行环境需要相应的人工验证。
