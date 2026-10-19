# Matched DGM-style Arm 实验结论报告

日期：2026-10-16；P2 状态更新：2026-10-19
实验名称：**matched DGM-style arm / DGM-on-Pi baseline**  
有效运行：`dgm-pilot-s20261014-v2-retry1`  
协议版本：`matched-dgm-pi-v2`

## 1. 结论摘要

这项实验应称为 **matched DGM-style arm**，也可简称
**DGM-on-Pi baseline**。它回答的问题是：在模型、数据划分、任务执行器和
预算均受控时，把 DGM 的 archive search、parent selection 和 staged
evaluation 接到 Pi harness 之上，是否能进一步改进 Pi。它不是原始 DGM
代码库的源码级复现。

主要结论如下。

1. **原始 DGM 没有使用 Claude Code harness。** 原论文使用自行实现的轻量
   Python coding agent，初始工具只有 Bash 和文件查看/编辑工具；Claude
   3.5 Sonnet (New) 是驱动 self-modification 和 SWE-bench task solving 的
   foundation model。把“使用 Claude 模型”写成“使用 Claude Code harness”
   是不准确的。[cite:1][cite:2][cite:3]
2. **本实验确实是 DGM-style search 与 Pi harness 的整合实验。** Pi 同时
   承担 mutation proposer 和 SWE-bench task agent；DGM 部分负责 archive、
   parent sampling、mutation lineage、10-to-60 分阶段评价和最终选择。
3. **本 seed 下结果为明确的 search-level 负结果。** P0 在固定
   `D_evolve-60` 上为 `19/60`；10 个 proposal slot 仅产生一个可完整归档的
   child，该 child 为 `18/60`。最终选择回到 P0，且最终 artifact hash 与
   P0 完全相同：
   `0f5a215ac0bce1aac54cc709e1a86e5e16f6f10547b78b30c711af30726a4c1b`。
4. **因此 DGM 搜索层在本次运行中的增量改进严格为零。** 最终部署策略不是
   “与 P0 相似”，而是同一个 artifact。独立重跑同一 artifact 时，随机模型
   仍可能产生不同的观测分数；这种波动不能归因于 DGM。当前没有运行或暴露
   `D_test big-140`，所以报告不把该身份结论伪装成一个新的 140-task
   实测 accuracy。
5. **可支持的表述是：** 在 seed `20261014`、10-slot pilot、受限可变表面和
   DeepSeek-v4-flash 条件下，DGM-style archive search 没有给先进 Pi
   harness 带来可部署增益。单 seed pilot 不能支持“DGM 对所有先进 harness
   都无效”的普遍结论。
6. **P2 首次重跑没有形成有效结果。** 搜索在 slot 5 的 mutation 请求遇到
   上游 DNS/代理 `502`，按预注册协议标记为 `infrastructure_invalid`。
   `D_test` 未消费，P0 仍可复用，但本次 mutation 和 partial score 不得进入
   P2 对 DGM 的最终效果比较。

## 2. 原始 DGM 实际使用的 harness

原论文把初始系统描述为围绕冻结 foundation model 构建的轻量 coding
agent。该 agent 自主选择工具，初始只有 Bash 和 edit 两类工具；论文明确说
它被有意设计得很简单，以便观察 self-improvement。[cite:1]

官方代码与论文一致：

- `coding_agent.py` 定义本地 `AgenticSystem`，通过 `chat_with_agent` 运行
  自定义 agent loop，并从目标 Git 仓库提取 patch；它不是 Claude Code
  CLI、SDK 或 Claude Code agent harness。[cite:2]
- `llm_withtools.py` 自行实现 Anthropic/OpenAI 请求、tool-call loop 和
  `load_all_tools()`；其中
  `CLAUDE_MODEL = bedrock/us.anthropic.claude-3-5-sonnet-20241022-v2:0`。
  这证明 Claude 是底层模型，而不是被调用的 Claude Code harness。[cite:3]
- `DGM_outer.py` 实现 archive、基于 score/children 的 parent sampling、
  keep-all 更新和默认 80 次 evolution iteration。[cite:4]

原始 SWE-bench DGM 的主要设置是：80 次迭代、每次生成一个新 agent，两个
迭代并行；先评估 10 个任务，再扩展 50 个任务；60-task 得分超过 40% 且位于
archive 前二的候选再扩展到累计 200 个任务。self-modification 和 SWE-bench
evaluation 均由 Claude 3.5 Sonnet (New) 驱动。[cite:1]

## 3. DGM 与 Pi 的具体整合方式

本实验没有把原始 DGM agent 放在 Pi 外层调用，而是保留 DGM 的搜索规则，
把“可进化的 coding agent”替换为受控的 Pi strategy/tool artifact。

完整链路如下。

1. **冻结 P0。** Pi core、task runner、官方 grader、模型、prompt/runtime
   stack 和数据划分先冻结。P0 可变 artifact 仅包含 `strategy.md`、
   `tools.json` 和最多四个 `handlers/*.py`。
2. **建立 DGM archive。** P0 作为 archive 的初始节点。parent 权重为
   `sigmoid(10 * (score_60 - 0.5)) / (1 + functioning_child_count)`，并按
   wave 在执行前完成抽样。
3. **Pi 提议 mutation。** mutation 以一个失败的 `D_evolve` entry task
   为锚点，只能读取 parent artifact 和经过清洗的同仓库公开任务文本。Pi
   只能追加一段 strategy 或新增/替换一个工具，不能修改 Pi core 或 host
   harness。
4. **安全验证。** 工具 manifest 和 Python handler 先做静态校验。生成的
   handler 只通过 trusted host proxy 在 task container 中执行；container
   无网络，candidate mount 只读，task workspace 可写。
5. **DGM 分阶段评价。** child 先跑固定 small-10，至少解决 `4/10` 才进入
   additional medium-50。完成累计 60 个任务的有效 child 全部进入 archive，
   即使分数低于 parent。
6. **最终选择与封印。** 按 `score_60`、archive 插入顺序、artifact hash
   依次决胜。搜索封印后才允许物化 `D_test big-140`，避免 held-out 反馈进入
   mutation。

因此，实验中的因果处理不是“换成 DGM 自带 agent”，而是：

> 固定 Pi harness，加入 DGM-style evolutionary search，观察搜索得到的
> Pi strategy/tool artifact 是否优于未经搜索的 P0。

## 4. 公平性与复现边界

### 4.1 对 DGM 核心机制的匹配

| 维度 | 原始 DGM | matched DGM-on-Pi | 判断 |
| --- | --- | --- | --- |
| 初始节点 | 单一 base coding agent | 单一 Pi P0 artifact | 匹配 |
| 变异 | parent 修改自身代码 | Pi 修改自身 strategy/tool artifact | 语义匹配 |
| Archive | 保留具备功能的候选 | 保留完成 cumulative-60 的有效候选 | 匹配 |
| Parent selection | score sigmoid / functioning children | 同一形式，`lambda=10`、midpoint `0.5` | 匹配 |
| Staged evaluation | 10，再加 50 | 固定 small-10，再加 medium-50 | 匹配 |
| 低分 child | 可作为 stepping stone 保留 | 有完整有效 60-task 证据即保留 | 匹配 |
| 评测模型 | 同一候选在同一设置下比较 | P0/children 使用相同 DeepSeek 模型与 Pi runner | 受控 |
| 搜索/测试隔离 | top candidates 可扩展至累计 200 | 搜索只看 60，big-140 严格延后 | 更严格的 holdout |

### 4.2 与原始 DGM 不同的地方

| 维度 | 原始 SWE-bench DGM | 本 pilot |
| --- | --- | --- |
| 搜索规模 | 80 次迭代，2 路并行 | 10 个 proposal slot，单路执行 |
| Foundation model | Claude 3.5 Sonnet (New) | `byteplus/deepseek-v4-flash-ga` |
| Agent substrate | 自定义轻量 Python agent | Pi harness |
| 可变表面 | 可修改 coding-agent Python codebase | 仅 strategy、tool manifest、受限 handler |
| 完整评估 | 强候选可在搜索期扩展至累计 200 | big-140 对搜索完全不可见 |
| 目标 | 证明 DGM 可改进其简单 base agent | 检验 DGM-style search 能否继续改进 Pi |

这些差异意味着本实验不能复现或反驳论文中的 `20% -> 50%` 数值。它仍然是
公平的 baseline，因为目标问题本来就是 **DGM 的搜索原则加到相同 Pi
harness 后是否有增量效果**。DGM 与 P2 后续比较共享同一个 P0、模型、
split、mutation policy、slot 数、container、grader、任务上限和 archive
规则；唯一预注册的算法差异是 P2 的 adaptive gate 与 Repair-First CLM。

## 5. DGM-on-Pi 结果

### 5.1 搜索结果

| 指标 | 结果 |
| --- | ---: |
| P0 cumulative-60 | `19/60` (`31.67%`) |
| Proposal slots | `10/10` |
| 完整归档 children | `1` |
| 最佳 child cumulative-60 | `18/60` (`30.00%`) |
| 最终 archive 大小 | `2` |
| 最终 artifact | P0 |
| 最终相对 P0 改变 | `0` |

10 个 slot 的终态分解：

| 终态 | 数量 | 含义 |
| --- | ---: | --- |
| `ARCHIVED` | 1 | 完成 60-task，但比 P0 少解决 1 题 |
| `REJECT_SMALL` | 4 | 未通过 small-10 晋级阈值 |
| `CANDIDATE_INVALID_REJECTED` | 2 | 工具名或 handler 静态安全校验失败 |
| `EDGE_EVALUATION_INVALID` | 3 | task provider/runner 失败，未作为分数证据 |

### 5.2 成本

| 口径 | Reported tokens | API calls | Task executions | Active time |
| --- | ---: | ---: | ---: | ---: |
| 导入的审计 P0 panel | 21,821,181 | 60 | 60 | 21,847.840 s |
| 本次运行新增 | 55,834,155 | 166 | 156 | 37,331.341 s |
| Search ledger 合计 | 77,655,336 | 226 | 216 | 59,179.181 s |

P0 import 只复用旧 infrastructure-invalid run 中已经完成并逐条绑定 hash 的
60-task P0 panel；没有导入 mutation、child 或 `D_test` 结果。新增成本约
10.37 小时 active time，最终没有改变部署 artifact。

## 6. 负结果分析

### 6.1 直接原因：搜索没有找到优于 P0 的有效 child

唯一完成 60-task 的 child 为 `18/60`，低于 P0 的 `19/60`。DGM 的 keep-all
archive 正确地保留了这个 stepping stone，但最终选择规则也正确地回到了
P0。负结果不是“改进后在 big-140 上碰巧打平”，而是搜索阶段根本没有产生
可部署的优胜 artifact。

### 6.2 Candidate yield 很低

10 个 proposal 中，只有 1 个形成完整归档节点。其余 9 个由 4 个早筛失败、
2 个静态非法候选和 3 个 provider/runner-invalid edge 构成。这说明当前
mutation 生成质量、受限工具 schema 与评测基础设施共同压低了有效搜索宽度。
特别是 3 个无效 edge 不应算作模型失败，但它们客观减少了本 pilot 的有效
搜索机会。

### 6.3 10-slot pilot 远小于原始 DGM 搜索规模

原始 DGM 运行 80 次迭代，本实验只有 10 个 proposal slot。DGM 的论点依赖
低分 stepping stone 在后续 lineage 中产生价值；当 archive 最终只有 P0
和一个 18/60 child 时，这种长期复用机制几乎没有展开。因此，结果足以否定
“10-slot 条件下即可稳定改进 Pi”，但不能否定更大预算下出现改进的可能。

### 6.4 Pi 的起点更强，可变表面更窄

原始 DGM 从只有 Bash 和整文件 edit 的简单 agent 出发，论文中的重要改进
包括更细粒度文件查看、字符串替换、多次尝试和候选评审。[cite:1] Pi 已经
内置成熟的 agent loop、上下文管理和工具基础设施，而本实验又冻结 Pi core，
只允许 strategy/tool 扩展。因此，原始 DGM 最容易获得的 scaffold 增益在
Pi 上可能已经存在，剩余增益空间更小。

### 6.5 60-task 差一题不足以证明 child 真正更差

`19/60` 与 `18/60` 只有一个任务差异，且 task agent 使用随机 foundation
model。该差异足以按预注册规则选择 P0，但不应被解释为稳定的真实退化。
可靠的 policy-level 优越性需要多个独立 matched seed，而不是把 60 个 task
当成 60 次独立 evolution replicate。

### 6.6 关于“DGM accuracy 与 Pi 完全一样”

准确表述分两层：

- **算法与部署层面：完全一样。** 最终 hash 就是 P0 hash，DGM 没有引入
  任何策略或工具改变，因此 DGM-specific treatment effect 为零。
- **独立随机评测的观测层面：不保证逐题完全一样。** 同一 artifact 再跑
  一次仍可能因模型随机性得到不同分数。若出现差异，它是 rollout noise，
  不是 DGM 发现了新 harness。

当前 `big-140` 未物化、未评测。这保住了后续 P2 的 held-out 完整性，也避免
为同一 artifact 支付两次端点评测成本。

## 7. P2 公平重跑

P2 使用同一 `matched-dgm-pi-v2` 协议重新运行。与 DGM arm 完全共享：

- seed `20261014`、P0 artifact 与审计导入的 60-task observations；
- literal DGM small-10、medium-50 和隔离的 big-140；
- DeepSeek 模型、Pi task agent、mutation policy、10 slots / 2 per wave；
- task/mutation token 上限、timeout、Docker image 和官方 grader；
- DGM parent sampling、small promotion、keep-all archive 与 final selection。

P2 的唯一算法增量是：

1. mutation proposer 从同仓库 `D_evolve` 中选择最多 4 个 adaptive probe；
2. parent 与 child 在这些 probe 上成对执行；
3. 若出现 `parent pass -> child fail`，Repair-First CLM 搜索最小充分移除集；
4. 从最早受影响 lineage prefix 恢复，并按依赖关系安全 replay 后续 mutation；
5. gate 处理后的 artifact 仍必须接受与 DGM 完全相同的 fixed small-10 /
   medium-50 archive scoring。

### 7.1 首次 P2 重跑终态

运行 `p2-pilot-s20261014-v2` 已于 2026-10-16 10:11 UTC 终止。slot 5 的
mutation 请求收到本地 buffered proxy 返回的 `502`，根因文本为
`urlopen error [Errno 8] nodename nor servname provided, or not known`。
控制面文件 hash 与有效 DGM baseline 完全一致，因此该错误归类为外部基础设施
故障，而不是 P2 算法失败。

协议保护按设计生效：

- `search-invalid.json` 标记 `SEARCH_INFRASTRUCTURE_INVALID`；
- `d_test_consumed=false`，big-140 未物化；
- `p0_reusable=true`，审计 P0 panel 可供 fresh retry 复用；
- `search_mutations_reusable=false`，当前 partial lineage 不得续跑或进入结论；
- archive 只有 P0，未产生完成 cumulative-60 的 P2 child。

### 7.2 P2 partial slot 诊断

| Slot | Adaptive gate / mutation | Fixed scoring | 终态 |
| ---: | --- | --- | --- |
| 0 | Gate 通过；4 个 probe 无观测回归 | small-10 为 `3/10` | `REJECT_SMALL` |
| 1 | 发现 2 个回归；RF-CLM probe 后回退 baseline 也复现失败 | 未进入 small-10 | `RF_CLM_ABSTAIN_REJECTED` |
| 2 | 发现 2 个回归；没有同时通过回归任务的 lineage prefix | 未进入 small-10 | `RF_CLM_NO_PASSING_BASELINE_REJECTED` |
| 3 | Mutation proposer 超过冻结 token budget | 未评测 | `CANDIDATE_INVALID_REJECTED` |
| 4 | Gate 通过；4 个 probe 无观测回归 | small-10 为 `4/10`；medium 跑到 41 条时出现 invalid edge | `EDGE_EVALUATION_INVALID` |
| 5 | Mutation 请求遭遇 DNS/代理 `502` | 未评测 | 整个 search 标记 infrastructure-invalid |

P2 gate 的局部行为得到了验证：它识别并拒绝了两个带成对回归证据的候选。
但没有发生成功的 RF-CLM repair，也没有完整 P2 child 进入 archive。这只能
作为机制诊断，不能作为 P2 accuracy 或优于 DGM 的证据。

### 7.3 与 baseline 的可比结果表

| Arm | 运行有效性 | 完成 proposal slots | 非 P0 完整归档节点 | 最佳完整 child | 最终选择 / evolve-60 | 相对 P0 | D_test |
| --- | --- | ---: | ---: | ---: | --- | ---: | --- |
| Pi P0 | 有效审计 reference | - | - | - | P0：`19/60` | - | 未消费 |
| Matched DGM-on-Pi | **有效并封印** | `10/10` | 1 | `18/60` | P0：`19/60` | `0` | 未消费 |
| P2 adaptive + RF-CLM | **基础设施无效** | 5；slot 5 中止 | 0 | N/A | N/A | **不可估计** | 未消费 |

| Arm / 口径 | 新增 reported tokens | 新增 API calls | 新增 task executions | 新增 active time |
| --- | ---: | ---: | ---: | ---: |
| Matched DGM-on-Pi，有效完整搜索 | 55,834,155 | 166 | 156 | 37,331.341 s |
| P2，无效 partial search | 41,662,573 | 107 | 101 | 23,969.202 s |

P2 比 DGM 多出的 adaptive gate/RF-CLM task 是算法处理的一部分，但本次 P2
只运行到中途，因此成本不能直接解释为完整两臂的效率差异。预注册假设 H2
“P2 优于 matched DGM”在当前证据下是**未决**，不是接受，也不是拒绝。

### 7.4 Fresh retry

经付费重跑确认后，新运行已于 2026-10-19 03:25 UTC 在本机 Terminal 启动：

- run ID：`p2-pilot-s20261014-v2-retry1`
- 输出目录：`research_output/rerun_20261019/p2_seed20261014_v2_retry1`
- config hash：
  `2e5a9514ae671a360f2c3e8246d219d973ea8c273668e1c4ed9a197a2b3c56de`
- P0 artifact、P0 panel、evolve-60 manifest、execution stack、split binding
  和 endpoint commitment 均与 matched DGM baseline 相同
- 非付费与付费 preflight 均通过
- slot 0 已生成有效 mutation artifact
  `423f0485cdd071a1e82e895dfe2c1774ec1d82f16314d1d96d08bdd6c7719c01`
- proposer 已选择 4 个同仓库 Sphinx probe，当前进入
  `p2-slot-0000-gate-parent`
- `search-seal.json` 和 `D_test` manifest 均不存在

该运行于 2026-10-19 03:40 UTC 在第四个 parent probe
`sphinx-doc__sphinx-8475` 处退出。任务 trace 中两次 `Connection error`
均被 Pi 自动重试，最终 assistant message 为成功 `stop`，且完整 patch 已
生成；但 `pi_swe_runner.mjs` 保留了早先的 stale `providerError`，导致成功
恢复后的任务仍以退出码 1 被误判为 `provider_or_runner_invalid`。

共享 runner 已修复为只保留最后一个 assistant turn 的 provider 状态：后续
成功的 `toolUse` 或 `stop` 会清除已经恢复的连接错误。端到端回归测试覆盖
“连续两次连接断开、第三次成功”的真实 retry 流程。

审计发现 matched DGM-on-Pi 的 slot 8 也存在相同模式：trace 最终成功
`stop`，但 stale `Connection error` 将 edge 误记为 invalid。另两个 DGM
invalid edge 是未恢复的真实 403/abort。由此，旧 DGM 结果仍是 protocol-v2
的已封印结果，但不能作为修复后 P2 的严格 matched comparator。公平的后续
比较需要让 DGM 与 P2 都使用修复后的同一 runner 重新搜索。

### 7.5 Runner-fix matched 双臂重跑

runner 修复已提交为
`c0d7ea6d4ac1f2fd7f613b685254c7222f5e30b1`。新的 DGM 与 P2 协议目录
使用相同的 execution stack
`71a9ee0b03657e4c2c7c3e64208e209f1a8f037156a7573cc06d24c0cba7a30d`、
split binding 和 P0 artifact；除 run ID、arm 与 P2 adaptive gate 外，
冻结配置一致。

旧 P0 panel 的导入被 fail-closed 校验拒绝，因为 runner 修复改变了
execution-stack hash。为避免把旧 runner 的 observations 混入新 runner
证据，本轮两个 arm 均 fresh 评测 P0 cumulative-60，不放宽导入校验。

双臂串行付费重跑已于 2026-10-19 04:16 UTC 在本机 Terminal 启动：

- DGM run ID：`dgm-pilot-s20261014-v2-runnerfix1`
- P2 run ID：`p2-pilot-s20261014-v2-runnerfix1`
- DGM config hash：
  `c1fcb5047b2827274040c3d2d7a093540860d1df72abb9937d6b773f181a4ec2`
- P2 config hash：
  `ba9fb43543342e05bad883fba801eba4fd1aa721fd601f4c5ddbeaab4b14a7ed`
- 两臂非付费与付费 preflight 均通过
- 当前阶段：DGM `search-p0`；首题已形成有效 observation 与成本账本记录，
  进度 `1/60`，第二题已启动
- 执行顺序：DGM 正常封印后才启动 P2；DGM 非零退出时不启动 P2
- `search-seal.json` 和 `D_test` manifest 在两臂均不存在

## 8. 建议对外表述

推荐：

> Under a matched 10-slot DGM-style search budget, evolution did not improve
> the Pi harness for seed 20261014. The selected final artifact was exactly the
> unchanged Pi baseline (19/60), while the only fully evaluated child achieved
> 18/60. This is a seed-level negative result for DGM-on-Pi, not a claim that
> DGM is universally ineffective.

不推荐：

> DGM 在先进 harness 上没有任何作用。

后者超出了单 seed、10-slot、受限可变表面的证据边界。

## 9. 本地证据

- 预注册协议：[`MATCHED_DGM_PI_PREREGISTRATION.md`](MATCHED_DGM_PI_PREREGISTRATION.md)
- 冻结策略：[`fixed-policy.json`](research_output/rerun_20261015/dgm_seed20261014_v2_retry1/frozen-inputs/fixed-policy.json)
- P0 审计导入：[`p0-import-contract.json`](research_output/rerun_20261015/dgm_seed20261014_v2_retry1/p0-import-contract.json)
- 最终 archive：[`archive.json`](research_output/rerun_20261015/dgm_seed20261014_v2_retry1/archive.json)
- 搜索封印：[`search-seal.json`](research_output/rerun_20261015/dgm_seed20261014_v2_retry1/search-seal.json)
- 完整成本账本：[`global-cost-ledger.jsonl`](research_output/rerun_20261015/dgm_seed20261014_v2_retry1/global-cost-ledger.jsonl)
- 运行日志：[`terminal.log`](research_output/rerun_20261015/dgm_seed20261014_v2_retry1/terminal.log)
- P2 冻结策略：[`fixed-policy.json`](research_output/rerun_20261016/p2_seed20261014_v2/frozen-inputs/fixed-policy.json)
- P2 无效终态：[`search-invalid.json`](research_output/rerun_20261016/p2_seed20261014_v2/search-invalid.json)
- P2 partial archive：[`archive.json`](research_output/rerun_20261016/p2_seed20261014_v2/archive.json)
- P2 成本账本：[`global-cost-ledger.jsonl`](research_output/rerun_20261016/p2_seed20261014_v2/global-cost-ledger.jsonl)
- P2 运行日志：[`terminal.log`](research_output/rerun_20261016/p2_seed20261014_v2/terminal.log)
- P2 fresh retry 冻结策略：[`fixed-policy.json`](research_output/rerun_20261019/p2_seed20261014_v2_retry1/frozen-inputs/fixed-policy.json)
- P2 fresh retry 日志：[`terminal.log`](research_output/rerun_20261019/p2_seed20261014_v2_retry1/terminal.log)
- P2 fresh retry 失败 observation：[`observation.json`](research_output/rerun_20261019/p2_seed20261014_v2_retry1/observations/p2-slot-0000-gate-parent/0f5a215ac0bce1aac54cc709e1a86e5e16f6f10547b78b30c711af30726a4c1b/sphinx-doc__sphinx-8475/observation.json)
- P2 fresh retry trace：[`trace.jsonl`](research_output/rerun_20261019/p2_seed20261014_v2_retry1/observations/p2-slot-0000-gate-parent/0f5a215ac0bce1aac54cc709e1a86e5e16f6f10547b78b30c711af30726a4c1b/sphinx-doc__sphinx-8475/trace.jsonl)
- Runner-fix 双臂启动脚本：[`start_both.command`](research_output/rerun_20261019/start_both.command)
- Runner-fix 双臂合并日志：[`runnerfix1-terminal.log`](research_output/rerun_20261019/runnerfix1-terminal.log)
- Runner-fix DGM 日志：[`terminal.log`](research_output/rerun_20261019/dgm_seed20261014_v2_runnerfix1/terminal.log)
- Runner-fix P2 日志：[`terminal.log`](research_output/rerun_20261019/p2_seed20261014_v2_runnerfix1/terminal.log)

## Sources

- [cite:1] Zhang, J., Hu, S., Lu, C., Lange, R., & Clune, J. *Darwin Gödel
  Machine: Open-Ended Evolution of Self-Improving Agents*. arXiv:2505.22954,
  Sections 3, 4.1, 4.2, C.1-C.2.
  https://arxiv.org/html/2505.22954
- [cite:2] Official DGM repository, `coding_agent.py`, commit
  `682eb38a3eb232f4396924cacd0a083bf1444cf8`.
  https://github.com/jennyzzt/dgm/blob/682eb38a3eb232f4396924cacd0a083bf1444cf8/coding_agent.py
- [cite:3] Official DGM repository, `llm_withtools.py`, commit
  `682eb38a3eb232f4396924cacd0a083bf1444cf8`.
  https://github.com/jennyzzt/dgm/blob/682eb38a3eb232f4396924cacd0a083bf1444cf8/llm_withtools.py
- [cite:4] Official DGM repository, `DGM_outer.py`, commit
  `682eb38a3eb232f4396924cacd0a083bf1444cf8`.
  https://github.com/jennyzzt/dgm/blob/682eb38a3eb232f4396924cacd0a083bf1444cf8/DGM_outer.py
