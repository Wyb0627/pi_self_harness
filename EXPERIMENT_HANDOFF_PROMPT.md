# 给新 Session 的执行 Prompt

你现在负责在我交还电脑前，停止正在运行的 DGM→P2 实验，冻结所有已完成结果，
生成可审计的统计与可恢复 checkpoint，并将必要信息 commit、push 到 GitHub。
不要只给方案，直接执行到远端验证完成。

## 固定上下文

- 仓库：`/Users/bytedance/codes/pi`
- 分支：`main`
- GitHub remote：`origin`，仓库 `https://github.com/Wyb0627/pi_self_harness.git`
- 开始本任务前本地 HEAD 应至少包含：
  `64de49831ac64144b0981428cd6c104bb8f97196`
- 当前本地 `main` 在创建本 prompt 时比 `origin/main` 多 2 个提交：
  - `ca58a46de`：provider retry 修复
  - `64de49831`：sandbox timeout 修复
- 正式运行入口：
  `research_output/rerun_20261020/start_timeoutfix1_both.command`
- 总日志：
  `research_output/rerun_20261020/timeoutfix1-terminal.log`
- DGM partial run：
  `research_output/rerun_20261020/dgm_seed20261014_v2_timeoutfix1`
- P2 prepared run：
  `research_output/rerun_20261020/p2_seed20261014_v2_timeoutfix1`
- DGM run ID：`dgm-pilot-s20261014-v2-timeoutfix1`
- P2 run ID：`p2-pilot-s20261014-v2-timeoutfix1`
- 协议：`matched-dgm-pi-v2`
- seed：`20261014`
- 当前每小时巡检任务名：`每小时监测 DGM-P2 实验`
- 当前实验并发必须保持为 1；`D_test` 尚未消费，也不得因本次交接而消费。
- API key 只能从 Keychain 服务 `pi.rollback-endpoint-api-key` 或安全环境注入。
  绝不能读取后打印、写入报告、提交到 Git，或保存完整进程环境。

## 硬性规则

1. 先完整读取并遵守 `/Users/bytedance/codes/pi/AGENTS.md`。
2. 不得使用 `git reset --hard`、`git checkout .`、`git clean`、`git stash`、
   `git add .`、`git add -A`、`git commit --no-verify` 或 force push。
3. 不得改写 Git 历史，不得删除用户或其他 session 的改动。
4. 不得把普通任务未解决、task budget exhausted 或模型未生成 patch 当成基础设施错误。
5. 不得把被中断且没有完整 `observation.json` 的任务计入有效统计。
6. 不得提交 workspace、Docker 镜像、node_modules、缓存、CA PEM、`.execution.lock`、
   API key、`auth.json`、完整环境变量、Keychain 内容或其他凭据。
7. 单文件必须小于 90MB；整个 checkpoint 应尽量控制在 25MB 内。不要为了方便
   直接提交约 473MB 的原始 run 目录。
8. 只 stage 本任务明确生成或筛选出的 handoff/checkpoint 文件。当前无关的
   `harness2_pipeline.html`、`research_output/rerun_20261016/`、
   `research_output/rerun_20261019/` 不得加入提交。
9. 不要重新启动实验。最终状态必须是实验、proxy、caffeinate 和相关 task
   container 均已停止，checkpoint 已推送。
10. 本次任务明确授权：暂停巡检、停止当前实验、生成 handoff 文件、commit，
    并 push 到 `origin/main`。不要再次询问这些操作的许可。

## 第一阶段：暂停巡检并安全停止实验

1. 使用 Schedule 能力先 `list`，按名称找到 `每小时监测 DGM-P2 实验`，然后
   `pause`。不要创建新定时任务。记录暂停结果和最后一次执行时间。
2. 记录停止前证据：
   - UTC 与本地时间；
   - `git status --short`、当前 branch、HEAD、`origin/main`；
   - DGM/P2 的进程树、PGID、运行时间；
   - proxy、caffeinate、Node runner、Docker/Colima 状态；
   - 当前 arm、phase、slot、已完成 observation 数、最新完整 observation；
   - `search-state.json`、`archive.json`、`global-cost-ledger.jsonl`、
     `search-seal.json`、`search-invalid.json` 和 `.execution.lock` 状态。
3. 仅停止本次 formal run 的进程，不影响其他 session：
   - 若当前 `pi_swe_runner.mjs` 正在执行，优先等待当前任务完成并写出
     `observation.json`，最多等待 10 分钟；
   - 然后向 formal DGM search 的进程组发送 `SIGINT`，等待清理；
   - 120 秒后仍未退出才发送 `SIGTERM`；
   - 只有再等待 30 秒仍未退出，才对本次 run 的残留进程或命名容器使用
     `SIGKILL`/`docker rm --force`；
   - 不得按宽泛关键词杀死无关 Python、Node、Docker 或 Terminal 进程。
4. 阻止顺序脚本在 DGM 停止后启动 P2。确认 P2 没有产生 task observation。
5. 停止本次 run 的 local SSE proxy 和 caffeinate。确认没有相关容器残留。
6. 所有相关进程确认退出后，检查 `.execution.lock`：
   - 若程序已自行删除，记录正常；
   - 若锁仍存在且 PID 已不存在，先把其内容复制到 handoff 证据，再删除原 run
     中的 stale lock，以便未来恢复；
   - 若锁对应进程仍活着，不得删除，继续处理进程。
7. 不要创建假的 `search-seal.json`，不要把人工停止写成成功或
   `infrastructure_invalid`。这是 **user-requested partial checkpoint**。

## 第二阶段：冻结并统计完整结果

以停止完成后的文件为唯一统计快照。只把存在完整、可解析 `observation.json`
的任务视为已完成 observation。若任务目录只有 `result.json`、trace 或 workspace，
将其列入 `interrupted_or_incomplete_tasks`，不得计入分母、resolved 或 token 汇总。

在以下目录生成交接包：

`research_output/checkpoints/20261020_timeoutfix1_handoff/`

至少生成：

1. `HANDOFF.md`
2. `metrics-summary.json`
3. `metrics-by-phase.csv`
4. `task-outcomes.csv`
5. `interrupted-tasks.json`
6. `file-manifest.sha256`
7. `remote-restore-and-resume.md`
8. `terminal-log-tail.txt`，保存停止前后各必要日志，去除任何敏感内容
9. `dgm_seed20261014_v2_timeoutfix1/`，可恢复的精简 DGM 状态
10. `p2_seed20261014_v2_timeoutfix1/`，已 prepare 但未执行的精简 P2 状态

`metrics-summary.json` 和 `HANDOFF.md` 必须包含：

- snapshot UTC/local 时间、停止方式、是否有强杀；
- source branch、source HEAD、protocol revision、run IDs；
- execution stack hash、config hash、split binding hash、fixed policy hash、
  P0 artifact hash、seed、model/provider、并发；
- `D_test` 是否消费，必须用文件证据确认；
- DGM 当前 slot/phase、已生成 proposal slot、已完成/未开始/中断 slot；
- 每个 phase 的 completed、valid、invalid、resolved、accuracy；
- 每个 artifact/slot 的 small-10 与 medium-50 分数及 promotion 状态；
- P0 的完整 60-task 分数；
- archive 全部 entry、parent、artifact hash、score、resolved/evaluated；
- 当前最佳 artifact，并明确它是 partial-search best，不是 final sealed result；
- ledger 的 reported tokens、conservative charge、API calls、task executions、
  active seconds、agent/evaluator/image/pacing 时间；
- status 分布，包括 completed、task budget exhausted、provider/runner invalid；
- provider errors、timeout、budget abort 的数量，但要区分“有效零分 observation”
  与基础设施 invalid；
- 最新完整 observation 时间；
- P2 状态，明确 prepared/not started；
- 为什么本 run 未完成：user-requested machine handoff，而不是算法失败；
- 未来恢复后仍剩哪些 slot/phase；
- 明确禁止把 partial metric 当成最终 DGM/P2 对比结论。

`task-outcomes.csv` 每行至少包含：

`phase,slot,artifact_hash,instance_id,valid,resolved,status,reported_tokens,`
`agent_duration_seconds,evaluator_duration_seconds,image_build_seconds,`
`observation_hash,identity_hash`

所有聚合值至少用两种独立方法交叉验证：

- 从 `observation.json` 聚合；
- 从 hash-chained `global-cost-ledger.jsonl` 聚合。

两者若有差异，报告差异原因，不能静默选一个数。校验 ledger hash chain、archive
hash、observation hash/identity hash，以及 JSON 可解析性。对百分比明确分母，
不要把 incomplete task 放进分母。

## 第三阶段：制作可恢复的精简 checkpoint

不要修改或删除原始 473MB run。将必要文件复制到 checkpoint，保留相对路径。
使用结构化脚本或 `rsync` include/exclude 规则，不要手工漏选。

DGM checkpoint 必须包含：

- `protocol-lock.json`
- `cold-start-attestation.json`
- `archive.json`
- `search-state.json`
- `global-cost-ledger.jsonl`
- 所有 top-level 审计 JSON，包括 `dgm-pi-*.json`
- `frozen-inputs/**`
- `artifacts/**`
- `artifact-records/**`
- `artifact-lineages/**`、`artifact-proposals/**`、`state/**`，若存在
- `search/slots/**` 中 mutation、terminal、lineage、proposal 和 RF-CLM 状态；
  可排除大 trace/runner log，但必须保留影响恢复与计分的 JSON
- `runtime/evolve-inputs/**`
- `runtime/images/**/image.json`，排除 build log
- 对每个 **完整** observation，保留：
  `observation.json`、`result.json`、`identity.json`、`invocation.json`、
  `evaluation.json`、`prediction.json`、`evaluator-invocation.json`，存在才复制
- 若代码恢复逻辑经静态检查还依赖其他小文件，也必须包含，并在
  `HANDOFF.md` 说明依据

明确排除：

- 所有 `workspace/`
- `trace.jsonl`
- `runner.log`、`evaluator.log`、build logs
- `.execution.lock`
- `*.pem`
- proxy logs
- auth/API key/env/keychain 数据
- Docker layers/images
- 只有部分写入且没有完整 observation 的任务目录

P2 checkpoint 必须包含其完整 prepared control-plane state、协议锁、冻结输入、
P0 artifact/record 和 cold-start attestation；确认没有 observation，也没有
`D_test` consumption state。

然后：

1. 检查 checkpoint 总体积和每个文件体积。
2. 对 checkpoint 内全部文件生成 SHA-256 manifest，并反向验证。
3. 全量扫描 secrets，至少包括 `ROLLBACK_ENDPOINT_API_KEY` 的真实值风险、
   `gho_`、`github_pat_`、`sk-`、`Bearer `、`apiKey`、`auth.json`、PEM 私钥、
   完整进程环境。配置字段名可以存在，但真实凭据不得存在。
4. 在 `/tmp` 复制 checkpoint 做一次恢复演练：
   - 校验 JSON、hash manifest、ledger/hash；
   - 用代码的 cache/resume 读取逻辑确认已完成 observation 可复用；
   - 确认恢复不会把 incomplete task 当完成，也不会消费 `D_test`；
   - 不进行付费调用，不真正重启 search。
5. 若精简 checkpoint 不能可靠断点续跑，则在 25MB/90MB 限制内补齐缺失小文件，
   直到恢复演练通过。不得用“以后再说”代替验证。

## 第四阶段：写清楚新电脑恢复方法

`remote-restore-and-resume.md` 必须给出另一台 macOS 电脑上的准确步骤：

1. clone `origin` 并 checkout 本次 handoff commit；
2. 安装项目依赖，遵守仓库 `npm install --ignore-scripts` 规则；
3. 按仓库已有文档/脚本恢复 Python runtime、SWE-bench dataset 和 preprocessing；
4. 启动符合协议的 Colima：8 CPU / 16GB RAM / 120GB Disk；
5. 重新从用户安全渠道注入 `ROLLBACK_ENDPOINT_API_KEY`，说明凭据未提交；
6. 验证 model endpoint、localhost buffered SSE proxy、Docker 和镜像构建；
7. 从 checkpoint 恢复到明确的 output path；
8. 先执行非付费一致性检查和 paid preflight；
9. 用原 seed、run ID、10 slots、2 proposals/wave、并发 1 和相同 protocol
   恢复 DGM search；不得 fresh 重跑已完成 observation；
10. DGM 成功 sealed 后才启动 prepared P2；
11. 不得提前物化或消费 `D_test big-140`。

不要猜 dataset/setup 命令。搜索现有 README、handoff、脚本和历史命令，引用真实
路径与参数。若某依赖无法由 GitHub 恢复，明确列出外部依赖、下载来源、校验 hash
和重建步骤。

## 第五阶段：提交并推送

1. 先运行：
   - checkpoint JSON/CSV/schema/hash/secret/size 验证；
   - 用现有聚合代码或精确测试验证 metrics；
   - `git diff --check`。
2. 本任务如果不修改源码/测试，不必为 docs/data checkpoint 运行全量测试或
   `npm run check`。如果为了 checkpoint 修改了源码，则必须遵守 `AGENTS.md`
   的代码测试与 `npm run check` 规则，并把源码和测试单独说明。
3. 检查 `git status`，只 stage：
   - `EXPERIMENT_HANDOFF_PROMPT.md`，若它仍是未跟踪文件；
   - `research_output/checkpoints/20261020_timeoutfix1_handoff/**`
   - 为本交接新增且必要的 handoff 文档/脚本
4. 使用显式路径或经过人工审阅的 `--pathspec-from-file` 文件列表 stage。
   绝不能 `git add .` 或 `git add -A`。
5. 提交消息：
   `docs(agent): checkpoint partial DGM-P2 experiment`
6. `git fetch origin`，确认不会覆盖远端工作。若 `origin/main` 有新提交，按
   `AGENTS.md` 安全 rebase；若冲突出现在本任务未修改文件，立即 abort 并报告，
   不得擅自解决或 force push。
7. push 到 `origin main`。绝不 push 到 `upstream`。
8. 远端验证必须包括：
   - `git rev-parse HEAD` 与 `git ls-remote origin refs/heads/main` 一致；
   - GitHub 上 handoff commit 可见；
   - checkpoint 关键文件可通过远端 commit 读取；
   - 远端 commit tree 中没有 >90MB 文件、凭据、workspace、trace 或 PEM；
   - 本地 `main` 不再 ahead of `origin/main`。

## 完成标准和最终回复

只有以下全部满足，才可说“交接完成”：

- 巡检已暂停；
- formal DGM/P2、proxy、caffeinate、runner、相关 Docker 容器均已停止；
- partial metrics 已生成并交叉验证；
- checkpoint 恢复演练通过；
- resume 文档包含另一台电脑的可执行步骤；
- secrets 和大文件扫描通过；
- commit 成功；
- push 到 `origin/main` 成功；
- 远端 SHA 与本地 HEAD 一致。

最终用简洁中文报告：

- 停止时间与停止方式；
- 完成到哪个 arm/slot/phase；
- P0、完整候选和 partial 候选的关键指标；
- 总 tokens/API/tasks/active time；
- incomplete task 如何处理；
- checkpoint 大小和文件数；
- commit SHA 和 GitHub commit URL；
- 新电脑恢复文档路径；
- 任何不能随 GitHub 迁移、需要重新下载/配置的依赖。

若 push 或恢复验证失败，明确写“交接未完成”，保留本地文件并给出最短修复路径；
不要在失败后重新启动实验。
