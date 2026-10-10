# Skill 实测记录

日期：2026-10-11（Asia/Shanghai）。这些测试验证代理实际执行 Skill 后的产物，不只检查模板。独立代理在 `/tmp` 隔离目录实现任务；主代理另行运行功能检查并比较已有仓库状态。临时项目不会作为脚手架随 Skill 复制，也没有远端操作。

## 重跑方法

先运行本仓库的确定性测试：

```sh
python3 -m unittest discover -s tests -v
```

然后给独立代理本 Skill 的 `SKILL.md` 绝对路径和以下任务之一。仅授权临时目录中的本地文件、Git 和测试操作。不要给代理预期实现或已发现的缺陷。完成后实际运行其使用指南，核查测试结果、文档一致性和 Git 状态。

### A：简单 CLI

任务：在临时目录新建 Node/JavaScript 标准库项目，不安装依赖。实现 word-count CLI：读取指定 UTF-8 文件，输出非空行数及按空白分隔的词数；允许空文件；读取失败时给出明确错误和非零退出码。目标 Linux，中文人类文档；生成测试、CI、产品说明、使用说明、独立代理流程及本地提交，不设置远端。

验收重点：真实输入输出、空文件、读取失败、使用步骤可重现；项目没有无用框架、架构文档或空目录。

### B：持久化应用

任务：在临时目录新建 Python 标准库 pantry-notes CLI，支持添加中文条目和列出记录，重新启动仍能读取，显式选择数据文件路径。不存在的文件可初始化；已有损坏文件应报错并保留原字节。目标 Linux，中文使用文档与数据备份恢复步骤，测试、CI 和本地提交；只用测试数据、不设置远端。

验收重点：跨进程保存/读取、损坏文件保留、失败处理、实际备份恢复演练，文档不承诺未验证的数据保证。

### C：已有仓库

先用临时 Python greeter 仓库建一个历史提交和 `trunk` 分支。现有 README 有运行/测试步骤；AGENTS 要求 Python 标准库、保留 README/AGENTS 原文，治理补充须批准。制造 `notes.txt` 同时有暂存与未暂存内容、`greet.py` 未暂存修改及未跟踪的 `private-data.txt`。在代理开始前保存所有现有文件 SHA-256、HEAD、分支、Git 索引、状态、暂存/未暂存差异。

任务：保持现有行为、工具和所有用户工作，补必要产品/使用说明与本地 CI。明确未批准更改旧 README、AGENTS 或治理规则；允许独立临时 worktree 和本地提交，不添加远端。

验收重点：历史/分支/暂存/未暂存/未跟踪内容保持原样；原规则不被覆盖。授权缺口应准确报告为未完成，不能为了通过结构校验擅自加治理文件。

## 已执行结果

本 Skill 的 27 项确定性测试通过（Python 3.14.8、Git 2.56.0）。官方 `skill-creator/scripts/quick_validate.py` 返回 `Skill is valid!`；UI 元数据与本 Skill 的 CI YAML 解析通过。所有辅助脚本/测试文件接受 Python 3.10 语法；未在实际 Python 3.10 环境运行。CI 动作版本通过 GitHub 官方 release/tag API 核实并固定到提交 SHA。

独立审查发现并修复了两种误报：普通 Python `__init__` 等名称，以及合法 Jinja 示例 `{{ user.name }}`。新增行为回归测试通过；独立代理另行重建仓库验证 6 种模板表达式与真实占位符结果，证据为 `/tmp/repo-bootstrap-independent-review-jinja-fix.json`。校验器只识别声明的精确大写 token 和常见占位符形式，不尝试解释模板语言。

### A：完成可运行的 CLI

项目：`/tmp/repo-bootstrap-cli-forward-kSmRvA/project`，分支 `bootstrap/word-count`，提交 `16ec95c13f2051ae06f503cf9343b7b7210ce77d`。`main` 保留 `.gitignore` 初始化提交；任务工作树干净，没有远端。程序仅 25 行，使用 Node 标准库，无安装依赖或编译步骤。9 项公开行为测试通过，0 失败、0 跳过；结构与三个显式 Node 检查通过。

代理交接：`/tmp/repo-bootstrap-cli-forward-kSmRvA/HANDOFF.md`，命令日志和最终 validator JSON 在同目录 `evidence/`。主代理另用新输入确认中文/英文文本计数为 2 行/4 词，空文件为 0/0，缺失与无读取权限分别给 ENOENT/EACCES 和退出码 1，原输入字节不变；另行执行语法检查及 9 项测试。证据：`/tmp/repo-bootstrap-root-cli.json`。

复查命令：

```sh
cd /tmp/repo-bootstrap-cli-forward-kSmRvA/project
node --check word-count.mjs
node --check tests/word-count.test.mjs
node --test --test-reporter=tap tests/word-count.test.mjs
```

初次 Node 子进程启动被执行环境沙箱以 EPERM 阻止，授权的隔离执行环境下能够运行。示例测试曾因清理钩子的顺序错误失败；修复后 9/9 通过，最初诊断保存在 `evidence/initial-test-diagnostics.txt`，没有隐藏失败。主代理首次汇总假定默认报告为 TAP，实际 Node 使用 spec 报告；指定 reporter 后完成汇总，程序测试本身两次均通过。

中文 README 21 行、PRODUCT 35 行、OWNER_GUIDE 43 行、AGENTS 35 行，没有额外架构文档。空白行、词边界、整体读入内存等解释列为实现假设。实际运行版本 Node 26.11.1；CI 中的 Node 24 目标和托管 CI 尚未执行。

### B：完成可运行的持久化应用

项目：`/tmp/repo-bootstrap-pantry-notes-q0PFIn`，分支 `feat/persistent-notes-cli`，提交 `a456db203280831ccaac79465378fb43ff2ec5fe`。`main` 只保留初始化提交，任务分支工作树干净，没有远端。程序使用标准库；10 项自动测试、编译检查、8 项结构检查及两个显式命令通过，最终 validator 状态为 `passed_with_local_checks`。

代理报告：`/tmp/repo-bootstrap-pantry-notes-q0PFIn-evidence/REPORT.md`，完整命令在同目录 `commands.json` 和 `final-commands.json`。主代理另用新的可丢弃数据运行真实 CLI：两条中文记录跨进程读取、另一数据路径为空、非法 UTF-8 文件被查看/添加拒绝且字节不变、用实际 `cp` 备份/恢复后原记录和字节均恢复。证据：`/tmp/repo-bootstrap-root-persistence.json`。

可复查：

```sh
cd /tmp/repo-bootstrap-pantry-notes-q0PFIn
python3 -m unittest discover -s tests -v
python3 -m py_compile pantry_notes.py
```

中文 README 25 行、PRODUCT 30 行、OWNER_GUIDE 65 行、AGENTS 43 行；没有额外架构文档或服务。使用指南提供命令、预期输出、更新、故障排查及已演练的恢复步骤。单人顺序写入是假设；没有承诺并发、断电、未来格式迁移或加密保证。

### C：保留已有仓库并准确报告授权缺口

已有仓库实测产物：`/tmp/repo-bootstrap-e2e-existing-tqo9v3fa-maintenance`，分支 `task/local-maintenance`，提交 `8a37cc9eb14b093608913ba14960314c5d0a2fac`。代理只新增 `docs/PRODUCT.md`、`docs/OWNER_GUIDE.md`、`scripts/check.py`；检查原测试和 CLI 输出通过。破坏 CLI 输出与函数返回的两份一次性副本均被本地检查以非零退出码拒绝。

完整报告：`/tmp/repo-bootstrap-e2e-existing-tqo9v3fa-adoption-report.json`。主代理独立比较 7 个原文件哈希及 HEAD、分支、Git 索引、状态、暂存与未暂存差异，全部与开始前一致。原 README/AGENTS 也在新 worktree 保持原提交字节。原历史是新任务提交的祖先。

复查命令：

```sh
python3 /tmp/repo-bootstrap-e2e-existing-tqo9v3fa-maintenance/scripts/check.py
python3 scripts/validate-bootstrap.py \
  /tmp/repo-bootstrap-e2e-existing-tqo9v3fa-maintenance \
  --ci-path scripts/check.py --check 'python3 scripts/check.py' --require-checks --json
```

第二条退出码为 1，唯一结构失败项是缺少 PR 模板。原规则禁止未获批的治理扩展，因此没有新增模板或改写 AGENTS。报告区分“已完成授权的接入工作”和“完整 bootstrap 仍未完成”；这正是本场景的正确安全结果。本地检查脚本由人工确认用途，`--ci-path` 只检查文件存在，不将其解释为已配置的托管 CI。

## 证据解释和限制

结构校验通过只说明标准文件存在、内容非空、没有已识别的占位符和有 CI 配置；显式命令通过也不能证明所有行为正确。远端 CI、分支保护、合并、部署和 Codex 自动发现均需独立验证。

`/tmp` 中项目与完整日志是本次会话的检查材料，可能被系统清理。此文件保留任务、结果和具体命令，确定性测试每次重新创建自己的临时仓库。重复接入、所有语言和平台的完整幂等性均不在本次验证范围内。
