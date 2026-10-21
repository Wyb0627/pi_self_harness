# 动态版 Pi 方法说明（返璞归真版）

> 目的：用最简洁、不出错的方式讲清两套机制 —— **动态采样**（决定一次改动保留还是回退）和 **动态回退 RF-CLM**（失败后退到哪、怎么重放）。
> 所有结论对齐源码：`rollback_mvp/adaptive_eval/`（采样）、`pi-rollback/src/`（回退）、`research_output/clm_budgeted_evolution_20260924_125503/dgm200_run/summary.json`（结果）。

---

## 0. 一页速览

- **原版 Pi（P1）**：固定子集评测、archive 只增不删、按分数重选 parent，**没有回退动作**。
- **动态版 Pi（P2）**：两处升级
  1. **动态采样**：不再用固定任务面板，而是**以“一次改动”为 query，用 LLM agentic search 挑最能暴露这次改动好坏的任务**。
  2. **动态回退（RF-CLM）**：把进化史建成可回放的 patch 谱系，用**可执行反事实 replay** 直接定位“最小充分移除集”，退到最早移除点之前再重放后续有效改动。
- **结果**：P1 50.0%（100/200）→ P2 69.5%（139/200），+39 题全为 P2 新增。
- **必须声明的边界**：P2 的 69.5% 用了**一轮隐藏官方评测反馈**，是“恢复上界”，**不是**标准单次提交 SWE-bench 分数；P1 的 50.0% 才是严格可比基线。

---

## 1. 动态采样机制（Agentic Adaptive Evaluation）

### 1.1 它回答的问题 —— 不是“解某个 issue”

评估对象是**一次 harness 改动**，记作一条边 `P → C`：

- **P（parent）**：当前这版 Pi 策略。
- **C（child）**：P 做了**一处改动**后的新版本。

要回答的问题只有一个：**这次从 P 到 C 的改动，该保留还是回退？**

SWE-bench 的 GitHub issue 任务在这里**不是目标，是量尺**（测量工具）。我们按这次改动，从任务全集里挑一批任务，让 P 和 C 都去跑，比较谁更好。

> **没有“根源 task 输入”这回事。** 流水线的起点是“改动的证据”，不是某个任务。

### 1.2 输入（这次改动的“证据包”）

| 字段 | 内容 | 来源 |
|---|---|---|
| `CandidateChangeCard` | P→C 的 diff：改了哪些路径/符号、依赖变化、改动摘要 | 这次 mutation |
| `BadCaseCard`（可多条） | P 以前在哪些任务上、以什么失败模式挂过 | 父代历史 |
| `U` 任务全集 | 冻结的候选任务目录 | 固定数据集 |

关于 `U`：**当前实现 = 全部 200 道**（DGM SWE-bench Verified，hash 锚定）；**协议本意 = 只暴露 `D_evolve=60`，把 `D_test=140` 隐藏作最终 held-out**。60/140 隔离是待实现门，两种说法都要能讲。

**隔离硬约束**：selector 看不到 gold patch、test patch、官方评测私有日志、`D_test`。

### 1.3 LLM 的 agentic search —— 全程由 LLM 驱动

selector 是一个**冻结的 tool-calling LLM**（固定 system prompt 和模型版本）。它每轮能看到的 context（`public_prompt`）包含：这次改动 `change`、`bad_case_ids`、候选全集 `eligible_task_ids`、本轮已选 `selected_task_ids`、**上一轮的配对结果 `prior_round_summaries`**、本轮调用历史、剩余预算。

它能调的工具：

| 工具 | 作用 | 内部算法 |
|---|---|---|
| `search_lexical(query, filters, limit)` | 搜**字面命中**：异常类、API、路径、工具名 | BM25 |
| `search_semantic(query, limit)` | 搜**语义相近**：换措辞也召回 | cosine |
| `get_change()` | 读这次改动 diff | — |
| `get_bad_case(id)` | 读某条父代失败详情 | — |
| `get_task(id)` | 读某任务卡 | — |
| `inspect_round_results(r)` | 看上一轮 P/C 配对结果 | — |
| `marginal_coverage(...)` | 只读查“补盲区”增益（次要） | ΔCoverage |
| `propose_tasks(proposals)` | **输出：直接提一批要选的任务** | — |
| `finish_round(reason, stop)` | 结束本轮；主动停须 `evidence_saturation:` 开头 | — |

**“agentic” 的含义**：LLM 自己写 query、自己选调哪个工具、调几次、读完结果再改写、何时停。BM25/cosine 只是工具**内部**给返回候选排序，**不替 LLM 做选择决定**。

`propose_tasks` 的每个提议必须带 `evidence_reference`，且该任务必须确实出现在被引用的那次检索结果里 —— **LLM 不能凭空提任务，只能提它检索到过的**。

### 1.4 选择结构：两梯队（这是容易被误解的地方）

LLM `propose_tasks` 之后，由**确定性仲裁器**（非 LLM）处理，分两梯队：

- **梯队 1 · LLM 直接假设（主力）**：LLM 提议的 `repair_cause` + `regression` 任务。正常情况（提议数 ≤ 容量）**原样全部保留**。ΔCoverage 在这梯队**不做筛选**，只在两种情况起作用：① 提议**超容量**时用贪心取舍；② 某任务 ΔCoverage=0 又没写 `necessary_distinct_reason` 时直接报错（fail-closed）。
- **梯队 2 · ΔCoverage 贪心补位**：**仅当梯队 1 没填满容量才触发**，用边际覆盖贪心补多样性。候选池 = **LLM 检索/查看过的 inspected 子集**，池空了才回退全集 `U`。

> 一句话：**选择主力是 LLM 的修复/回归假设；ΔCoverage 贪心只做“超额取舍”和“欠额补位”。** 梯队 2（facility-location 补位）是设计文档 §10 **预注册的可消融项**。

**inspected 候选池怎么来**：不是单独构造，是 LLM 每次检索结果的自动累加 —— 任务出现在 `search_lexical`/`search_semantic` 命中、`get_task`、或 `marginal_coverage` 参数里就进池；`get_change`/`get_bad_case`/`inspect_round_results` 不进池。

### 1.5 为什么 parent 也要跑？—— 因为我们量的是“改动的净变化”

**只跑 child 不够。** child 的绝对分会被任务难度污染：

> child 在 6 个任务上解出 3 个。好还是坏？取决于 parent 的基线 —— parent 本来解出 5 个就是**退化**（该 ROLLBACK），parent 只解出 1 个就是**改进**（该 ACCEPT）。同一个 “3/6” 既可能是改进也可能是退化。

所以必须跑 parent 拿配对基线，逐任务相减：

```
δ(task) = Y(C, task) − Y(P, task)   ∈ {−1, 0, +1}
```

配对相减**抵消掉“任务本身难不难”这个共同项**，只留下改动的净效应。这也是决策用 **paired bootstrap + McNemar**（McNemar 只看 P/C 结果不一致的任务）的原因 —— 它们本质就是配对比较，单跑 child 喂不进去。此外，**回退也需要 parent 作为“退回哪里”的参照**。

### 1.6 search 与量尺是“滚动闭环”，不是单向一步

- **测试集（selected tasks）** = agentic search 的**输出**。
- **配对读数 δ** = 测试集跑完 P/C 后的**测量值**，它①最终喂裁决；②**回流进 LLM 的 context（`prior_round_summaries`），成为下一轮选任务的依据**。

```
Round 1: LLM 看[改动 diff + 历史失败] → 搜 → 选 T1 → P/C 跑 T1 → 得 δ(T1)
Round 2: LLM 看[改动 diff + 历史失败 + δ(T1)] → 再搜 → 选 T2 → ...
停机 → 全部 selected ∪ audit 冻结 → 跑最终配对 → 裁决
```

第一轮没有任何读数，LLM 只靠改动 diff + 历史失败起步；从第二轮起才有前轮 δ 可自适应。**回流给 LLM 的只有脱敏公开配对结果（谁解出谁没解），不含官方私有断言和 gold patch。**

**停机条件**（不是“ΔCoverage 不再增长”）：`task_budget` 用尽 / LLM `finish_round` 声明证据饱和 / `max_rounds` 或 selector 的 token / 时间预算触顶，任一先到。

### 1.7 三态决策（确定性，不调 LLM）

量尺冻结后，决策引擎只消费配对结果和预注册策略：

```
L, U* = δ 的 paired-bootstrap 95% 置信区间下界 / 上界

ACCEPT    : L  > acceptance_margin  且 audit 守卫通过
ROLLBACK  : U* ≤ rollback_margin
ESCALATE  : 其余（或 targeted 与 audit 证据矛盾）→ 挂起、开有限额扩展
INVALID   : manifest / 身份 / 配对证据校验失败 → fail-closed
```

margin、置信水平、bootstrap 种子都是**预注册**值，代码里没有魔法阈值。

### 1.8 公式与 notation

记 `sim(a,b) = max(0, 归一化向量点积) = max(0, cosine) ∈ [0,1]`。

| 公式 | 定义 | notation | 用途 |
|---|---|---|---|
| 相似度 | `sim(i,j) = max(0, cosine(emb(i), emb(j)))` | i,j=任务；emb=L2 归一化 1024-D 向量 | 检索 & 覆盖的基础量 |
| 覆盖度 | `Coverage(S) = (1/\|U\|) Σ_{u∈U} max_{s∈S} sim(u,s)` | S=已选集；U=任务全集；u,s=其中任务 | **冻结后只报告** |
| 边际覆盖 | `ΔCoverage(x\|S) = (1/\|U\|) Σ_{u∈U} max(0, sim(u,x) − max_{s∈S} sim(u,s))` | x=未入选候选 | 梯队 2 补位 / 超额取舍 |
| 冗余度 | `Redundancy(S) = (1/\|S\|) Σ_{s∈S} max_{t∈S,t≠s} sim(s,t)` | t=S 中另一任务 | **只报告** |
| 配对差 | `δ(task) = Y(C,task) − Y(P,task) ∈ {−1,0,1}` | Y(v,task)=版本 v 是否解出 ∈{0,1} | 决策输入 |

两点要记牢：

1. **cosine 这同一公式用在两处**：检索里是 `sim(query, 任务)`，覆盖里是 `sim(任务, 任务)` —— 公式一样，比较对象不同。BM25 只用于检索。
2. **边际 ΔCoverage 才驱动选择；聚合 Coverage 和 Redundancy 都是冻结后只报告**，不进 `_arbitrate`、不进 audit、不进决策引擎。它们是“仪表盘”，不是“闸门”。

### 1.9 两道护栏（次要，但对严谨性重要）

- **独立 audit**：从 `U` 里 LLM 看不到的任务中，按确定性种子抽一组混入量尺。目的是查 selector 的系统性盲区；若 targeted 证据与 audit 证据矛盾 → ESCALATE，不自动接受。
- **Coverage / Redundancy 报告**：防 batch 塌缩成“同一失败 trace 的近重复”，并让不同消融实验可比。

> 面试提示：若被追问“自适应选出的子集有偏，凭什么代表整体？”——答案就是 audit + 60/140 held-out 这套护栏；自适应 batch 是**操作性门控**，不是 200 题的无偏估计。

---

## 2. 动态回退机制（Repair-First CLM）

### 2.1 它回答的问题

进化失败后：**退到谱系上哪个祖先？** DGM 没有这个动作（archive 只增、按分数重选 parent）。我们直接找“删掉就能修复”的**最小充分移除集**。

### 2.2 输入

| 输入 | 内容 |
|---|---|
| `checkpoints` | 线性 lineage：每个 patch 一个节点，带 `changedFiles`、`dependsOn` |
| `FailureBundle` | 失败摘要、候选 patch slice、LLM 软先验 `priorOrder`、`sliceAuditRecall` |
| `probe()` | 给定一组 active patch → 是否复现失败（可执行验证，奇数次重复取多数票去噪） |

### 2.3 三因子

- **因子 A · 候选先验**：用失败信息、依赖、历史 credit 给候选 patch 排序。LLM 输出是**软先验，不得硬删候选**。
- **因子 B · 反事实验证**：先验证“移除最高先验的单个 patch”能否修复；不行再对**移除集**跑 `ddmin`（delta-debugging 最小化）。
- **因子 C · rollback-and-replay**：落点 = **最早被移除 patch 的父节点**；对其后 patch 按依赖拓扑重放，只保留“不依赖移除集且通过 probe”的增益。

关键判据：

```
repairs(R) = ¬ probe( 全部 patch ∖ R ).failed      # 移除集合 R 后失败是否消失
```

### 2.4 成本硬门控

```
sliceFraction = |候选 slice| / |全部 patch|
启用 sliced ddmin  ⟺  sliceFraction ≤ 0.30  且  sliceAuditRecall ≥ 0.95
否则 → full ddmin（准确优先）
```

门控是预注册实验定下的：实测只有在此条件内，sliced 才能保持 exact=1.0 的同时省调用；门控外无条件省钱的说法已被证伪。

### 2.5 输出（`DiagnosisRecord`）

- `method` ∈ {`singleton-removal`, `sliced-repair-ddmin`, `full-repair-ddmin`, `abstain`}
- `removedPatchIds`：最小充分移除集
- `RollbackPlan`：`rollbackCheckpointId`（落点）+ `replayPatchIds`（可重放的后续增益）+ `skippedPatches`（跳过原因：`causal` / `dependency` / `overlapping-files`）
- **`apply` 默认 dry-run，必须用户确认，严禁操作 git 历史**（硬约束）。
- 无法可靠定位时 `abstain`，不给方案（而不是乱退）。

### 2.6 核心成果

Repair-First 相比旧的 failure-first 路径，**减少 42.86%–49.89% probe 调用**；clean repair=1.000，5%/10% 噪声下 repair=0.973/0.970（均在预注册 2-point non-inferiority margin 内），call-reduction 的 paired bootstrap 95% CI 严格大于 0。

**成本模型**：`C_total = M × c_node`（M=被评测节点数，c_node=每节点评测成本）。主力省幅来自**杠杆 2：回退剪污染子树 → 降 M**（与改动是否局部无关）；杠杆 1（partial 复评降 c_node）仅对局部改动有效，是有条件加成。

---

## 3. 实验结果与诚实边界

### 3.1 三指标对比（固定 200 题 DGM-200 清单）

| 系统 | 准确率 | Reported tokens | 直接执行时间 |
|---|---:|---:|---:|
| P1 原版 Pi（one-shot） | 100/200 = **50.0%** | 70.725M | 8.75h |
| P2 动态版 Pi（+RF-CLM 回退） | 139/200 = **69.5%** | 76.639M（+8.19%） | +4.82h 增量（累计 13.57h） |

配对证据：+39 题全为 P2 新增（recovery-only=39，original-only=0）；paired bootstrap 95% 区间 [+14.0, +25.0] pp；McNemar 精确 p=0.0。

### 3.2 时间（防“两周”误解）

18.23 天日历跨度里 **16.99 天是显式暂停**（用户暂停、Docker 恢复、依赖修复、凭据恢复）。协议记录活跃墙钟 **29.89 小时**，其中直接执行 **13.57 小时**（P1 8.75h + P2 增量 4.82h）。“两周”是 DGM 论文开放式进化描述，不是可比时间基线。

### 3.3 必须守住的边界

- 🔴 **P2 的 69.5% 用了一轮隐藏官方评测反馈，是“恢复上界（recovery upper bound）”，不是标准单次提交 SWE-bench 分数。** 不能据此宣称打赢 DGM 或原版 Pi。
- 严格可比基线是 **P1 原版 Pi 单提交 50.0%**。
- DGM 论文 50% 是历史参考；本地审计只能复现其 30/60=50% 端点，不复现 100/200。
- 动态采样的 60/140 隔离、A3 多代回退（Phase-2 release gate）仍是待实现门。

---

## 4. 进化范围（现状 vs 目标）

| | 范围 | 状态 |
|---|---|---|
| **实际能跑的 MVP** | 仅 `strategy.md` 可变 = **策略 / prompt 层** | 已跑 |
| **设计目标** | 整个 harness：源码 + tools + prompts + 依赖 | 受隔离门限制 |

**卡点**：进化 tool / 源码需把 child 整个进程关进**容器隔离**（否则进化出的代码会在宿主 Pi 进程里执行）—— 这道门还没建，所以源码/工具级自我修改目前被 fail-closed 挡着。P2 那次 69.5% 进化的也不是 tool，是 RF-CLM 的反馈辅助修复。

---

## 5. LLM vs 确定性 —— 分工总表

| 环节 | 谁做 | 依据 |
|---|---|---|
| 写 query / 选工具 / 调几次 / 何时停 | **LLM** | 改动 diff + 历史失败 + 前轮 δ |
| 检索候选（BM25 / cosine 排序） | 代码（工具内部） | query 与任务卡 |
| 选任务（提议修复/回归假设） | **LLM** | `propose_tasks` |
| 超额取舍 / 欠额补位 | 代码 | ΔCoverage 贪心 |
| 独立 audit 抽样 | 代码 | 确定性种子，LLM 看不到 |
| 配对执行 P 和 C | 代码 | 冻结任务集 |
| 三态裁决 | 代码 | δ + bootstrap + McNemar + audit 守卫 |
| 回退诊断（ddmin / replay plan） | 代码（LLM 只给软先验） | 可执行 probe 验证 |

> **核心一句话**：动态采样 = “以一次改动的 diff + 历史失败为 query 的 agentic 检索”，产出一批任务当**配对量尺**，再用确定性统计裁决保留还是回退；LLM 负责“搜与提”，确定性代码负责“量与判”。
