# DGM-on-Pi: 自进化进化器作为 Pi Add-on 的设计方案

> 目标：把 DGM 的**核心自进化算法**（自诊断 → 自改 agent 代码/工具 → 评测 → 存档 → 迭代）融进 pi harness、用 deepseek-v4-flash 重跑，作为一个**完全独立的 add-on**，为论文提供"同模型、同 harness、同预算"的受控 DGM baseline。
>
> 硬约束（用户指定）：
> - **绝不影响现有 pipeline 运行**；DGM 完全变成 pi 的一个 add-on。
> - **直接做工具级进化（Phase 2）**，不止 strategy 层。
> - **不要 novelty**：DGM 不是我们的方法，无需忠实复刻其 QD/child-count novelty 采样；只把其核心算法融入 pi 即可。parent 选择退化为纯 score-based。
>
> 状态：设计待确认，不含实现代码。日期 2026-10-13。

---

## 1. 为什么要做 / 它补上什么

现在论文里所有对 DGM 的比较都带免责声明："DGM 用的是不同 agent / model / 预算，只能当历史参考"（见 [EVOLUTION_ROLLBACK_DIRECTION.md](EVOLUTION_ROLLBACK_DIRECTION.md) §4.2、[dgm200_performance_comparison.md](research_output/clm_budgeted_evolution_20260924_125503/dgm200_performance_comparison.md)）。

一个**同模型、同 harness 底座、同评测预算**的 DGM 复现，能把"历史参考"升级为"受控对照"。注意定位：**DGM 不是我们的方法，是我们融进 pi 的一个 add-on**，因此不追求忠实复刻 DGM 的 QD/novelty 搜索，只复现其核心自进化算法骨架（自诊断 → 自改 agent 代码/工具 → 评测 → 存档 → 迭代），供论文做同底座对照。

---

## 2. 核心映射：DGM 的"改 agent 代码" → pi 上改什么

DGM 进化对象是它自己的 `coding_agent.py` / `tools/` / `prompts/`（已核实：每个节点 `metadata.json` 的 `entry` 是 mutation 标签，`model_patch.diff` 是相对父节点的 agent 代码改动，`self_evo.md` 是改动推理）。

pi 的 agent 是**已发布的 npm 包**，不能像 DGM 那样直接改源码。但 pi 自我定位就是 "self extensible coding agent"，可进化面是**磁盘文件**（已核实，见 [SELF_EVOLUTION_ANALYSIS.md](SELF_EVOLUTION_ANALYSIS.md) §0 和 [extensions.eval.ts](packages/evals/src/extensions.eval.ts) 的自著循环测试）：

| DGM 改的东西 | pi 上的等价可进化面 | 加载机制 |
|---|---|---|
| `prompts/` 里的 system prompt | **strategy 文本**（appendSystemPrompt） | 已有 `--strategy-file`（见下）|
| `tools/` 新工具 | `.pi/extensions/*.ts` 自定义工具 | `resourceLoader` + `reload` |
| 可复用技能 | `.pi/skills/<name>/SKILL.md` | 渐进式披露 + `reload` |
| `coding_agent.py` 控制流 | compaction / retry / 检索策略（SettingsManager + extension）| `reload` |

**一个"候选 harness" = 一组 {strategy 文本 + skill 文件 + extension/tool 文件}**。进化就是让 LLM 生成/修改这组文件。**工具级进化是一等目标**（不止 strategy 层）。

> **我们自己的方法是否已支持 tool 进化？** 设计上支持、工程上尚未端到端跑通。[pi-rollback](pi-rollback/README.md) 从一开始就把进化对象定义为 "evolving prompts, skills, **tools**, and other harness artifacts"，且是**路径通用**的——`artifactPaths` 配 `.pi/extensions/evolving`、`.pi/skills/evolving`，快照/回退按文件路径做（[state.ts](pi-rollback/src/state.ts) `createSnapshot`），对 tool 无特殊逻辑。[AGENTIC_ADAPTIVE_EVALUATION_DESIGN.md:43](AGENTIC_ADAPTIVE_EVALUATION_DESIGN.md#L43) 也写明 "full DGM-equivalent self-modification: evolved extension/tool code"。但其容器执行器目前只测了契约 + fake runtime，真实 Docker 下的 tool 进化还没跑过。**结论：DGM add-on 做 tool 进化后，我们自己的方法也应一并支持同一能力——两者共用同一套"候选资源目录 + 容器评测"机制。**

pi 原生支持 agent 自著工具并即时生效：[extensions.eval.ts:98-123](packages/evals/src/extensions.eval.ts#L98-L123) 有一条已通过的测试——prompt 让 agent 写一个带 `hello` 工具的 extension → `reload` → 立刻调用。SDK 的 `customTools` / `resourceLoader` / `reload` 就是这条闭环的接口。

### 2.1 决定性发现：评测注入点已存在

[pi_swe_runner.mjs](rollback_mvp/pi_swe_runner.mjs) 已经有现成的 harness 注入 seam，**无需改动**：

- `--strategy-file`（[line 59](rollback_mvp/pi_swe_runner.mjs#L59)，可重复）读取策略文件，拼接后 `appendSystemPrompt`（[line 202-205](rollback_mvp/pi_swe_runner.mjs#L202-L205)）。
- `strategyHash` 已进评测 identity（[line 315](rollback_mvp/pi_swe_runner.mjs#L315)），天然可审计。
- 默认 `--strategy-file []` 为空 → **不传就是现有行为，零影响**。

这意味着：进化器只需在调用 runner 时多传 `--strategy-file`，就能让候选 harness 在**完全相同的隔离评测路径**（Docker `--network none`、workspace 限制、budget、official grader）下生效。extension/skill 注入则通过候选自己的 `agent-dir`/资源目录实现（见 §4.3）。

---

## 3. 隔离原则：如何做到"零影响现有 pipeline"

**物理隔离 + 只读复用**，三条红线：

1. **新目录、新入口**。所有新代码进 `rollback_mvp/dgm_evolve/`（新 Python 包）+ 一个新编排脚本；产物进 `research_output/dgm_pi_evolution_<timestamp>/`。**不改**任何现有文件：`orchestrate_endpoint_200.py`、`pi_swe_runner.mjs`、`build_local_swebench_images.py`、`config.py`、冻结清单、`summary.json` 一律只读复用。
2. **复用而非 fork 评测器**。进化器通过 `subprocess` 调现有 runner/builder/grader（和现有 orchestrator 用法完全一致），不复制、不改它们的逻辑。若将来需要 runner 支持 extension 目录注入，用**新增可选 flag**（默认关闭）实现，不改默认分支。
3. **独立预算与状态**。进化 run 有自己的 token/time cap、自己的 append-only 状态目录，不写任何现有 run 的 state。freeze 一份自己的配置快照。

验证"零影响"的判据：`git status` 下现有 pipeline 文件无改动；现有 `--offline` 实验与 DGM200 复跑结果不变。

---

## 4. 架构

```text
rollback_mvp/dgm_evolve/            # 新增，完全独立
├── archive.py        # 候选 harness 存档：append-only，节点=harness 版本
├── mutate.py         # LLM 变异：parent harness + 诊断 → child harness 文件（strategy/skill/tool）
├── select.py         # parent 选择：纯 score-based（greedy / 分数加权），无 novelty
├── evaluate.py       # 调用现有 runner/grader 评测一个候选（subprocess）
├── evo_loop.py       # 外层进化循环（对标 DGM_outer.py）
├── budget.py         # 独立 token/time cap + 付费确认
├── state.py          # 复用 adaptive_eval/state.py 的 append-only 原语（import）
└── harness_spec.py   # 候选 harness 的数据结构 + 内容寻址 hash
run_dgm_pi_evolution.py            # 新增 CLI 入口（唯一对外命令）
```

### 4.1 进化循环（对标 DGM_outer.py）

```text
初始化 archive = { node0 = 空 harness（= 原版 pi，strategy 为空）}
for gen in 1..G:
    parent      = select(archive)                      # §4.4
    diagnosis   = diagnose(parent 在 D_evolve 上的 bad cases)   # 复用 DGM 的 "改进建议" 范式
    child       = mutate(parent, diagnosis)            # §4.2，LLM 产出新 strategy/skill/ext 文件
    score,ledger= evaluate(child, D_evolve_subset)     # §4.3，调现有 runner
    archive.add(child, score, ledger)                  # append-only
    checkpoint(archive)                                 # 可恢复
# 搜索冻结后，最优节点在 D_test 上跑一次（复用现有 200 题评测）
```

边界：候选 harness（strategy/skill/tool）可变；**进化控制器（select/mutate/archive/grader）在一次 run 内固定**；候选整个评测在容器内。注意这是 DGM 核心算法的 score-based 移植，不含其 novelty/QD 搜索。

### 4.2 变异 mutate.py

- 输入：parent harness 文件 + 该 parent 在 D_evolve 子集上的失败证据（problem + 被拒 patch + 失败任务 id）。
- LLM（deepseek-v4-flash，走现有 `llm_client.py` 直连网关，或走 proxy）产出以下任意组合：新的 strategy 文本、新的 skill 文件、**新的 extension/tool 文件（`.pi/extensions/*.ts`）**。工具级变异是一等能力，不是可选项。
- 记录 `self_evo` 等价物：完整 prompt/response 落盘（对标 DGM 的 `self_evo.md`），保证可审计、可写进论文附录。
- 失败闭合：产出不合法（空 strategy、非法 TS、tool 定义缺 `tool_info`/schema）→ 该候选记为 invalid，不进 archive 分数。

### 4.3 评测 evaluate.py（复用现有隔离路径）

对候选 harness 的每个任务：

1. 复用 [build_local_swebench_images.py](rollback_mvp/build_local_swebench_images.py) 产出/复用实例镜像（**镜像与现有 run 完全相同、可共享缓存**）。
2. 给候选一个**专属 agent-dir / 资源目录**：拷贝现有 `pi_home/agent` 的 models.json/auth 配置（指向同一 proxy + deepseek-v4-flash），再放入候选自己的 strategy、`.pi/extensions`、`.pi/skills`。
3. 调 [pi_swe_runner.mjs](rollback_mvp/pi_swe_runner.mjs)：strategy 走已有 `--strategy-file`；**候选的 extension/tool 需要 runner 加载候选资源目录**。当前 runner 默认 `noExtensions/noSkills=true`，所以给它加一个**默认关闭的新 flag**（如 `--candidate-extensions-dir`），只在该 flag 显式传入时加载候选资源——不传时行为与现在逐字节一致，**对现有 DGM200 pipeline 零影响**（§3 红线②）。
4. 用现有 `python -m swebench.harness.run_evaluation` 官方评分。
5. 记录完整 ledger：token / time / tool trace / strategyHash + 候选资源内容哈希（进评测 identity）。

> runner 的这一处 flag 是整个方案里**唯一**对现有文件的改动，且是纯增量、默认关闭、可被我们自己的方法共用。若想连这一处都不碰，备选是 Phase 3 的 headless SDK 自建执行器（§6），但那样要重实现 runner 的容器沙箱/预算逻辑，反而更重、更易偏离现有评测语义。推荐走新 flag。

### 4.4 parent 选择 select.py（纯 score-based，无 novelty）

从 archive 选 parent 继续进化。**按用户决定，不实现 DGM 的 child-count novelty**：

- 默认：greedy，选当前最高分节点作 parent（或按分数做 softmax 加权采样，温度可配）。
- 理由：DGM 是融进 pi 的 add-on，不是需要严格复刻的对照基线；novelty/QD 是 DGM 的开放式探索机制，与"把核心自进化算法接进 pi"无关，省略不影响同底座对照的有效性。
- 文档/论文里据实说明：这是**score-based 的 DGM 核心算法移植**，非 DGM 原版 QD 搜索的逐项复现。

---

## 5. 数据与防泄露（沿用方向文档 §4.2 三防线）

- **D_evolve / D_test 切分**：进化只在 D_evolve（建议 small 10 + medium 50）上做；D_test（big 140 或全 200）全程不进任何评测/选择，只在搜索冻结后跑一次。
- **复用冻结清单**：直接读现有 [dgm_swebench_verified_200.v1.json](research_output/clm_budgeted_evolution_20260924_125503/dgm_swebench_verified_200.v1.json)，按 small/medium/big 分区切 D_evolve/D_test。保证与 P1/P2 同一任务宇宙，可直接对比。
- **评测环境隔离**：候选 agent 不可写测试/评测文件（runner 的 `isForbiddenEvaluationPath` 已强制）。

---

## 6. 分期实施（降风险，但目标是工具级进化）

**Phase 0 · 可行性冒烟（~0.5 天，几乎零成本）**
- 复用 `pi_sdk_smoke.mjs` 确认个人机 deepseek-v4-flash + proxy + Docker 跑通。
- 两个端到端冒烟，各跑 1 个任务：
  1. 手写一个 strategy 文件，用现有 runner `--strategy-file` 跑通、评分正常（零改 runner）。
  2. 手写一个最小 extension/tool，经新 flag `--candidate-extensions-dir` 加载，确认 `reload` 后工具生效、评分正常。
- **出口判据**：两条链路都单任务跑通拿到分数。不通过先修环境/flag，不进 Phase 1。

**Phase 1 · 工具级进化主体（含 strategy + skill + extension/tool）**
- 实现 archive/mutate/select/evaluate/evo_loop/budget；候选 harness 允许 strategy + skill + extension/tool 任意组合（§2、§4.2）。
- parent 选择纯 score-based，无 novelty（§4.4）。
- 在 small(10)+medium(50) 上跑少数几代（如 G=5~10），固定 model=deepseek-v4-flash、固定 mutation 提议器。
- 产出初步 DGM-on-pi 分数 + 完整 self_evo 审计日志（含每代产出的 tool 源码）。
- **出口判据**：拿到 D_evolve 进化曲线；评估 token/time 成本，决定是否上 D_test / 全量。

**Phase 2 · 冻结后终评 + 对齐**
- 搜索冻结，最优 harness 在 D_test（big 140 或全 200）跑一次，与 P1(50%)/P2(69.5%) 同任务宇宙对比。

**Phase 3 · （可选）headless SDK 自建执行器**
- 若想连 runner 的新 flag 都不加，可用已确认的 SDK 面（`createAgentSessionServices` + `createAgentSessionFromServices` + `transformSystemPrompt`/`customTools`/`resourceLoader`）自建候选执行器。代价是重实现容器沙箱/预算逻辑，更重且易偏离现有评测语义，**不推荐**，仅作备选。

---

## 7. 成本与规模预估

参照现有 DGM200：P1 单任务 agent 均时 ~128s、均 tokens ~355k。进化成本 ≈ `代数 G × 每代候选数 × D_evolve 任务数 × 单任务成本`。

- Phase 1 保守估：G=5，每代 1 候选，D_evolve=60 → ~300 任务次 ≈ P1 规模的 1.5 倍。免费 API 下主要代价是墙钟（Docker 评测），**无 GPU 需求**。
- 建议：先 G=3、D_evolve=small(10)+medium 子集跑通，再按 budget.py 的 cap 放大。付费确认沿用现有 `I_APPROVE_...` 模式。

---

## 8. 风险与规避

| 风险 | 规避 |
|---|---|
| 不小心改到现有 pipeline | 物理隔离（§3）；现有文件只读；runner 唯一新增 flag 默认关闭；提交前 `git status` 核对 |
| 候选自写 tool 不合法/不生效 | mutate 产出校验（`tool_info`/schema）；Phase 0 冒烟先验证 extension 加载链路；非法候选 fail-closed 不计分 |
| 候选 harness reward-hack 评测 | 复用 runner 的 forbidden-path/网络隔离；D_test 零可见；候选资源内容哈希进 identity |
| 候选 tool 在容器内有副作用/越权 | 候选 tool 仍受 runner 的 workspace 限制与 `--network none` 容器约束，和内置工具同等沙箱 |
| 成本失控 | 独立 budget cap + 付费确认 + 先小规模冒烟 |
| 离职后网关失效 | Phase 0 先在公司网关期内把可行性与初步数据跑出来 |

---

## 9. 验收标准

1. 现有 pipeline 文件零改动（唯一例外：runner 的默认关闭新 flag），现有实验结果可复现。
2. `run_dgm_pi_evolution.py` 能在 D_evolve 上跑完 ≥3 代、产出 archive + 每代分数 + self_evo 审计（含每代自写的 tool 源码），且至少有一代候选含自写 extension/tool 并真实生效。
3. 搜索冻结后最优 harness 在 D_test 上有一次性成绩，与 P1(50%)/P2(69.5%) 在同一任务宇宙下可直接比较。
4. 得到可写进论文的 **score-based DGM 核心算法移植（DGM-on-pi）** 结果，据实标注非 DGM 原版 QD 搜索的逐项复现。
