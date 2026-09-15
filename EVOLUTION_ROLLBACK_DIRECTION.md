# Diagnosis-Guided Rollback for Self-Evolving Harnesses

本文件记录我们想做的研究方向、与最相关三篇工作的逐点对照、防审稿人弹药、problem statement，以及在 pi 上可跑的最小实验设计。定位：在 pi harness 上做一个不 fork core 的研究 extension，支撑一篇技术报告 + 开源仓库。写完供对齐，不含实现代码。

配套：`SELF_EVOLUTION_ANALYSIS.md`（早期分层设想，仅参考）、`OBSERVATION_MEMORY_DESIGN.md`（记忆系统，仅参考）。本方向已收窄，不再沿用那两份文档的框架。

---

## 0. 一句话方向（headline）

> 现有 harness 自进化把进化史当成"只增 archive + 按分数重选 parent"，**回退是缺失的一等操作**。我们把进化谱系建成可回溯的搜索树，失败后用 **failure attribution 决定回退到哪个祖先版本**（不是上一个、也不是当前最高分那个，而是"缺陷引入点之前"），并用**回退点之后整段分支的成败分析**做 credit assignment，指导回退点选择与回退后的再进化。

可证伪 claim：这种"诊断式回退 + 分支级学习"，在相同评测预算下，比 DGM 式"重选 parent"、以及固定"回退一版 / keep-revert" 的盲回退，**更快逃出坏区、更省 rollout、且更不容易被污染分支带偏**。若在这三个指标上无可测优势，claim 被推翻。

**第三条 claim（成本/复杂度，与上面并列）**：DGM 类系统的进化成本随生成的 agent 数线性累积，且每个新 agent 都要从零评测、跨代零复用。我们用 attribution 驱动的 **partial 复评（只重跑受影响任务）** + **回退剪枝（收缩被评测的节点集）**，把"到达目标分数的总评测成本"显著降低。详见 §3.4。

---

## 1. 问题定义

Harness 自进化本质是一个无梯度搜索：提出对 harness 的改动（prompt / tool / 检索 / compaction / 控制策略）→ 在任务集上评测 → 保留有用的 → 继续。这条搜索路径天然是一棵树：一次改动是一个节点，改动叠改动形成谱系。

真实进化里失败不可避免，且有两个特点让"回退"变成核心而非边角：

1. **缺陷延迟暴露**：某个早期改动引入的问题，可能要到很多代之后、在特定任务上才崩。此时"退一版"退不到病灶，"退到当前最高分节点"可能恰好丢掉了后续所有有效增益所依赖的那个前提改动。
2. **失败分支不是垃圾**：从回退点到崩溃点这一整段 trajectory，包含"哪些改动其实有效、哪个是毒、什么组合导致回归"的信息。丢掉它等于每次失败都从零重来。

因此需要回答两个现有系统没正面回答的问题：

- **Q1（回退点选择）**：失败后应该退回到谱系上的哪个祖先节点？
- **Q2（分支 credit）**：如何把"回退点之后整段分支的成败与根因分析"回流，用来指导 Q1 的选择、以及回退后的再进化方向？

---

## 2. 与最相关三篇的逐点对照（related work 弹药）

精读后的事实修正（对本方向有利）：

- **DGM 没有"回退"这个动作**。archive 只增不删，从 archive 按 (performance + child-count novelty) 加权采样一个 parent 去 mutate；分支坏了是"换祖先重新长"，不是"退到某版本"。节点间除 parent 指针外无信息回流，每节点独立评测。
- **MARS 有智能回退，但对象是"单次任务执行轨迹"**，不是进化谱系。Rollback/Guided Repair/Continuation 跑在一次任务的 MCTS 上，用 14 条 MAST failure taxonomy 对 partial rollout 打 reward，回退点由 LLM 诊断反馈定。
- **Safe Harness Self-Evolution 是纯理论**，只建模单线顺序更新，明确无 evolution tree、无回退算法，只给可行性/代价的界，并自陈"stagnation 会发生""接近奖励上界时评测代价发散"。

| 维度 | DGM (ICLR'26, 2505.22954) | MARS (2607.29055) | Safe Harness (2609.08175) | 本方向 |
|---|---|---|---|---|
| 进化对象 | coding agent 自身代码 | 单次任务 MAS 轨迹 | harness (prompt/tool/code/orch) | pi harness 组件 |
| 结构 | archive/tree（只增） | 单任务 MCTS 树 | 单线顺序更新 | 进化谱系树（可回溯） |
| 失败后动作 | 换祖先重选 parent | Rollback 到诊断步 | 不采纳（无回退） | 诊断式回退到祖先 |
| 回退点如何定 | 无回退 | 诊断/attribution 定步 | 无 | attribution 定"缺陷引入点之前" |
| 分支信息回流 | 无（节点独立评测） | MCTS 回传 + 存诊断 f | 无 | 分支级 credit → 指导回退+再进化 |
| 驱动信号 | benchmark 分数 | failure taxonomy reward | expected reward 界 | 失败根因 + 分支成败分析 |
| 载体/证据 | SWE-bench/Polyglot | STATEMAS | 纯理论 | pi session tree + evals |

**空白**：把"failure-attribution 驱动的回退点选择"+"分支级 credit assignment"放到 **harness 进化谱系** 这一层，三篇都没占。

## 2.1 预判审稿人质疑与回应

1. "这不就是 DGM？" — DGM 无回退、parent 只看分数+novelty、节点间零信息回流；"退到哪"这个决策在 DGM 里不存在。
2. "这不就是 MARS 换场景？" — MARS 修一条任务轨迹（分钟级、状态可 replay），回退=丢弃后续步；我们修进化谱系（每节点=一整套 harness，评一次跑一批任务），回退=切到某祖先 harness 并携失败分支教训再进化。层级、代价结构、回退语义均不同。
3. "盲回退/keep-revert 不够？" — Hermes/L4-ratchet/event-sourcing 都是盲回退（掉阈值退上一版 或 keep/revert 二选一），没有"退到哪、为什么"的决策。这正是我们要打赢的 baseline。
4. "attribution 不可靠？"（真风险） — 借 MARS 的 failure taxonomy 思路做廉价归因，并把"attribution 质量"设成一个可消融、可度量的轴，而非黑箱假设（见 §5 风险）。注意术语区分：MARS 的 "partial rollout" 是**任务轨迹层**（只往前推 L 步不跑到终局），我们的 "partial 复评" 是**谱系层**（只重跑受影响任务子集 A(e)），两者同名但不同层，别混。
5. "Safe Harness 已理论覆盖？" — 它只证单线更新可行性界，明确无 tree、无回退算法，并自陈会 stagnation。我们把它的 open problem 做成算法系统，可反过来引用它当理论动机。
6. "你说 DGM 成本指数增长/搜索空间大，不对吧？" — 对，所以我们不这样写。DGM 每代生成 1 个 agent，实际评测节点数是 O(N) 线性；它也用了分级评测。我们攻击的是"每节点从零评测、跨代零复用、坏区不剪枝"，主张的是 **realized 评测成本 C_total 更低**，不是"空间更小"（见 §3.4 诚实边界）。

---

## 3. 方法草图（一个系统，三个可拆解部件）

三个部件对应三条可消融的因子，全开是 full method，逐个关掉即 ablation，保证 attribution 干净。

```text
          一次 harness 改动 (mutation)
                    │  评测(任务集)
                    ▼
        ┌───────────────────────────┐
        │  进化谱系树 EvoTree        │  节点 = 一个 harness 版本
        │  node: {patch, score,     │  边   = 一次改动
        │   diag, branch_stats}     │
        └───────────┬───────────────┘
                    │ 出现回归/失败
     因子A ─────────► Failure Attribution
                    │  (定位缺陷在哪条边引入)
                    ▼
     因子B ─────────► Rollback Point Selection
                    │  (退到"缺陷引入点之前"的祖先, 非上一版/非最高分)
                    ▼
     因子C ─────────► Branch Credit → Re-Evolution
                       (回退点之后整段分支的成败/根因回流,
                        指导下一步改动, 避免重犯)
```

- **因子 A（Attribution）**：给"这次失败"归因到谱系上的某条边/某个改动。信号来源：MARS 式 failure taxonomy 打分 + 逐边 partial 复评（只重跑受影响任务子集，而非全量）。
- **因子 B（Rollback Point Selection）**：候选回退点 = 缺陷引入边的父节点及其祖先；用"该祖先在受影响任务上的表现 + 其保留了多少下游有效增益"打分，选净收益最高的回退点。对照：DGM 的"重选最高分 parent"、盲回退的"退一版"。
- **因子 C（Branch Credit + Re-Evolution）**：把 A 段 trajectory 里"有效改动 / 毒改动 / 危险组合"蒸馏成再进化时的约束与提示，注入回退后的 mutation prompt，并降权已知会导致回归的方向。

数据结构（节点）：
```text
EvoNode {
  id, parent_id
  patch            // 相对父节点的 harness 改动 (extension diff)
  score            // 在固定任务集上的评测(pass/token/cost)
  diag             // 该节点失败模式诊断(taxonomy 标签 + 根因文本)
  branch_stats     // 该节点作为分支根时, 下游成败聚合(credit)
  affected_tasks   // 该 patch 影响到的任务子集(供 partial 复评)
}
```

pi 载体优势：session 本身是树（`/tree`、fork、branch summary），extension 是可热插拔文件，`/reload` 即切换 harness 版本 —— 进化谱系 = 一棵可导航的 session/extension 版本树，无需自造版本管理。评测闭环现成（`evalHarnessTable(baseline, candidate)` + repetitions 出 pass/token/cost 的 lift）。

### 3.4 成本 / 复杂度分析（第三条 claim 的展开）

先厘清 DGM 的真实成本机制（读原文核对，避免被审稿人反驳）：

- DGM 每代只生成 **1 个** 新 agent（论文跑了 **80 代**），所以它**实际评测过的节点数是 O(N)（随迭代数线性），不是指数**。
- DGM 已经用了**分级评测**（staged evaluation, Appendix E.1）：先 10 个任务筛"能否编辑代码"，通过再 50/60 个；SWE-bench 上进 archive 前二名才上 200 个。所以"它每轮全量跑 benchmark"的说法**不准确**，不要这样写。
- 真正可攻击的三点：(a) 每个新 agent 仍要**从零**评测（至少筛选批），**跨代零复用**，没有增量/局部复评；(b) archive 只增不删、所有节点保留非零采样概率，**坏区不会被排除**；(c) 因此到达目标分数所需的总评测量 ∝ 生成的 agent 数，且被无效/污染分支稀释。

**统一成本模型**（用它，别用"我的搜索空间比它小"这种硬定理）：

```text
总评测成本 C_total = (被评测的节点数 M) × (每节点评测成本 c_node)
```

术语约定（全文统一）：**B̄ = 双方可比的同一评测子集大小**，即"评一个 harness 版本时跑多少个任务"。DGM 用固定子集（10→50/60→少数晋级到 200，见上），我们的"full 复评"也以同一个子集为基准。**B̄ 不是全 benchmark 任务总数**——若按全集算会高估 DGM 成本，正好犯我们自己立的"别夸大 DGM 成本"的戒。

我们从两个正交杠杆同时压这个乘积（注意：这里的"杠杆1/杠杆2"是**成本杠杆**，与 §3 方法组件的"因子 A/B/C"是两套不同编号，别混）：

- **杠杆1 · 降 c_node（partial 复评）**：DGM 每节点从零跑一批任务，成本 ≈ B̄。我们借因子 A 的 attribution，只对一次改动 e **影响到的任务子集 A(e)** 复评，其余用缓存分数，c_node 从 B̄ 降到 |A(e)|。**关键限制：这只对"局部改动"成立（|A(e)| ≪ B̄）；对全局改动 |A(e)|≈B̄，几乎不省——详见 §3.5 失效条件。** 所以杠杆1 是有条件加成，不是普遍省。
- **杠杆2 · 降 M（回退剪枝）**：达到深度 d、分支因子 b 的**可达配置空间是 Θ(b^d)——这是"空间"，DGM 和我们共享，不能声称我们空间更小**。区别在**实际评测的节点数 M**：DGM 不剪枝，坏区持续被采样；我们用回退把被 attribute 为污染的子树降权/剪掉，等价于把**有效分支因子**从 b 收到 b′<b，达到同一深度所需评测节点从 O(b^d) 降到 O(b′^d)。**杠杆2 与改动是否局部无关，全局改动照样受益，是鲁棒主力。**

**可证的部分（放附录 §8，理想假设）**：在 §8 的三个假设 (A1) attribution 安全覆盖、(A2) 缓存命中、(A3) 去噪 下，给出 C_total 的上界，证明 Ours ≤ DGM-式重选（同样到达目标分数）。**真实中假设部分破**，差距靠实验兜底（见 §4.3 的 attribution 准确率、决策一致性、逃逸代价）。

**关键诚实边界（写作必须守住，否则被反驳）**：
- 不说"DGM 成本是指数"——它实际是 O(N) 线性；指数的是共享的可达空间。
- 不说"我们的搜索空间更小"——空间相同，是**被评测的节点集 realized cost** 更小。
- partial 复评的正确性依赖 attribution；attribution 错则可能漏评真正受影响任务 → 需把"partial vs 全量复评"的差异作为一个可控性指标报告（见 §3.5）。
- **成本主张主力是杠杆2（降 M），不是杠杆1（降 c_node）**：杠杆2 减少被评测节点数，与改动是否局部无关，全局改动照样受益，是鲁棒主张；杠杆1 只对局部改动有效（见 §3.5 的失效条件），降级为有条件加成。即便杠杆1 完全失效，杠杆2 独立成立。

### 3.5 partial 复评的正确性边界（safe-RTS 视角 + 冻结归因器 + decision-consistency）

因子1（partial 复评）会引入 DGM 没有的偏差面，本节把它的成立条件、失效条件、防线、度量一次讲清。这些"自曝"是为了让 attribution 边界可信，不是可省的谦辞。（注：本节的"partial 复评"即 §3.4 的**成本杠杆1**；下文沿用"杠杆1"称呼。）

**记号**：`e`=一次改动（谱系树的一条边）；`A(e)`=改动 e 的受影响任务集（partial 复评只重跑 A(e)，其余复用父代缓存分）；`B̄`=评测子集大小（同 §3.4，即评一个版本跑多少任务，非全 benchmark）；`Attr-fwd: e→A(e)`=前向归因器（partial 复评用，要求高 recall）；`Attr-bwd: 失败→罪魁边`=后向归因器（回退用，要求定位/argmax）。

**三类失败模式，别混为一谈**：
- **C1 测量偏差（本方法独有）**：复用缓存分数，若 A(e) 漏掉真正受影响任务 → 节点分数是有偏估计。DGM 每个 agent 在固定子集上从零新跑、不复用缓存，故**无 C1**（它只有无偏的子集方差）。
- **C2 优化器钻盲区（本方法在 C3 之上多出的一层）**：进化是优化器，只要有"从不重跑的缓存任务"这个结构性盲区，选择压力会让"看着局部、实则全局"的改动因被漏评而存活。这是 selection drift，非恶意 craft。
- **C3 过拟合到评测集（自进化共病，DGM 也有）**：优化器过拟合到驱动进化的那批任务。靠 D_evolve/D_test 切分兜（见 §4.2）。

**杠杆1 的失效条件（诚实标注）**：safe-RTS 省成本依赖"改动局部"。但 self-harness 的很多改动是全局的（换 control loop / compaction / system prompt 核心 / orchestration），几乎影响每个任务 → 安全的 A(e)≈全集 → partial 复评退化成全量，**不省**。因此杠杆1 收益按改动类型高度异质：局部改动省得多；全局改动基本不省。**设计上用一个 affected-set 大小估计门控**：估计 |A(e)| 小才启用 partial，估计为全局就退回全量。

**防线一 · 冻结归因器（评估器与被评估进化体隔离）**：Attr-fwd 与 Attr-bwd 都是 LLM，但**不进进化回路、不自我修改**，接口与 schema 提前固定。
- 目的1（防篡改）：不冻结的话进化体可能 hack 归因器给自己放水（benchmark-hacking 文献里"评估者信任被评估者"是根漏洞）。
- 目的2（可校准，更关键）：冻结 → 归因器的 recall 是平稳函数，audit 校准一次可跨代外推偏差估计；若归因器自己进化，偏差界是移动靶。
- **schema 必须锚在 task-side 不锚在 harness-side**：harness 会长出新组件，若 schema 按"哪个组件受影响"描述，冻结的归因器会逐代变盲（coverage staleness）；按"哪些任务/任务族/行为契约被触及"描述则一直有效。
- 诚实 nuance：冻结让归因器作为映射平稳，但 Proposer 探索新改动类型使输入分布漂移，realized recall 仍可能降；这由 audit 监测，不能假设掉。

**防线二 · 周期 audit（兜住残余 C2）**：冻结归因器挡不住 C2（C2 与冻不冻无关，根源是缓存盲区）。每 K 个节点做一次全量 audit，直接估偏差与漂移。这不是锦上添花，是抵消"优化器驱动漂移"的承重结构（对标 surrogate-assisted EA 的 model management）。

**目标函数：decision-consistency（保序），不是 pointwise 无偏**。搜索只消费比较（谁更好、退到哪），不消费绝对分。故只需保证 partial 诱导的决策与 full 一致，这比无偏弱、可达、且是搜索真正需要的。三种决策粒度不同，分别度量：

| 决策 | 本质 | 一致性度量 |
|---|---|---|
| D-accept | Δ 分数符号 | 符号一致率 |
| D-select | 候选排序 | top-weighted τ（主）+ 标准 τ（辅，可比）+ top-1 一致 |
| D-rollback | 祖先里 argmax | 落点一致率（构造设置里有 oracle） |

**三层度量结构**：
1. **margin-aware 决策翻转率（主，便宜、常测）**：只在 `|Δ_full|>ε` 的决策上统计翻转，按 margin 分箱，避免把噪声级翻转算成 partial 的错。
2. **top-weighted τ（早警，比翻转更敏感）**：优化器钻盲区时会先压小候选分差、后改变 top-1；τ 在 top-1 翻转之前就下降，是先行信号。标准 τ 附带汇报以保可比性。
3. **反事实 regret（贵、偶尔，双用途）**：仅在 audit 决策点 partial 与 full 选择不同（flip）时触发——开一条短分叉（步长 h≪全 rollout）走 full 会选的分支，`regret = perf(full 分支) − perf(partial 分支)`。用途①：用 (flip, regret) 对估 `P(regret>0 | flip)`，标定"翻转率是否 regret 的可信代理"，之后放心只跑便宜的翻转率；用途②：累加 regret 直接进权衡表，量化"用 partial 而非 full 的净性能代价"。反事实分叉的额外算力计入 Ours 总成本，不藏。

**自指混淆（必写 limitation）**：partial 驱动了搜索轨迹，事后 audit 到翻转时已走在 partial 路径上，一致性是在被污染轨迹上测的。反事实 regret 测的是"相对 full 的实际损失"，绕开自指——这是它不可省的原因。

**度量的可证伪落点**：把翻转率 / τ / regret 都画成"代数"的函数。平稳=健康；**单调恶化 = C2 兑现**（优化器钻盲区），看 audit+回退能否压回噪声带。KILL：在合理 K 下，margin>ε 的翻转率仍高或累计 regret 显著 → 砍杠杆1（partial 复评退回全量），只留杠杆2（回退剪枝）。

---

## 4. 最小实验设计（证伪 headline 的最短路径）

### 4.1 核心对照

固定 model / 数据划分（D_evolve、D_test 见 §4.2）/ mutation 提议器，只换"失败后怎么办"这一个策略：

- **B0 无回退**：失败即停或贪心续（对照下限）。
- **B1 盲回退-1**：固定退到上一版（Hermes/ratchet 类）。
- **B2 DGM 式重选 parent**：不回退，从 archive 按 score+novelty 采一个祖先重新长。
- **B3 keep/revert ratchet**：二选一门控（L4 类）。
- **Ours**：诊断式回退（A+B），再加 C。
  - ablation：Ours\A（回退点随机/按分数，不用 attribution）、Ours\B（有 attribution 但只退一版）、Ours\C（回退后不带分支教训）。

### 4.2 数据设置：公开 benchmark 做 main result + 公开任务上受控注入做诊断

不自造任务数据集（会被 argue 挑分布）。分两个用途，用途不同、数据来源不同：

**用途 A · main result（方法在真实分布上有效）——用公开集。**
在 Terminal-Bench / SWE-bench(-Verified) 上按任务序喂进进化回路，比较 Ours vs B0–B3。任务分布公开、不可被质疑挑数据。

**用途 B · 诊断（机制本身正确）——公开任务 + 受控注入缺陷。**
"回退点正确率""污染抑制""regret"这些指标需要 ground-truth 理想落点 / 已知缺陷边，而真实进化里没人知道理想落点。故取公开集真实任务，在谱系里**人为注入一个已知坏改动 S**（如改坏 compaction 阈值、禁用某 tool、往 system prompt 塞干扰），S 已知 → oracle 落点可算。任务全来自公开集，缺陷受控。定位为诊断性受控探针，不是 main result。

典型注入形态（缺陷延迟暴露 + 早期改动是后续增益前提，最考验智能回退）：
```text
gen1: 改动 P (有效, 是后续 Q/R 前提)
gen2: 改动 Q (依赖 P, 有效)
gen3: 注入 S (只在任务族 T 上暴露的缺陷, 此时 T 未出现)
gen4: 改动 R (依赖 P, 有效, 分数继续涨)
gen5: 任务族 T 出现 -> 崩
```
oracle 落点 = 退到 gen2/gen4 之间、剔除 S、保留 P/Q/R。盲回退-1 退到 gen4（仍带 S 或丢 R）；DGM 重选最高分 parent 可能挑含 S 的 gen4 或丢掉 P 依赖链；Ours 应 attribute 到 S、退到 S 之前、带"R 有效"credit 重进化。这是最便宜的 kill test：若此设置下 Ours 都不能比盲回退更常退到 oracle 落点，方法核心即证伪。

**数据泄露三防线（写死，全部强制）**：
1. **D_evolve / D_test 切分**：D_test 全程不进任何评测 / 回退 / attribution 决策，只在最后跑一次报成绩。防"进化过拟合到评测集"（C3）。
2. **S 只依赖 harness**：注入缺陷只允许看 harness、改 harness，**不允许**看 D_test 的任务或答案，否则 S 编码测试信息、oracle 落点循环论证。
3. **评测环境隔离**：agent 不可写测试 / 评测文件，防 SWE-bench conftest 类污染与 reward hacking（近期审计已证 SWE-bench Verified 可被 10 行 conftest 改动刷满）。若进化"发现"评测捷径导致分数虚高，main result 作废——故隔离是须先搭好的基础设施。

对照序列（无延迟缺陷、单调上升）验证 Ours 在不需要智能回退时不吃亏（不引入额外开销/退化）。

### 4.3 指标

标准（pi evals 原生）：任务成功率、总 token / input token、est. cost、model turns。

方向专属（需自建打点）：
- **逃逸代价**：从进入坏区到恢复到崩溃前最好分，所花的 rollout 次数 / token。核心证据。
- **到目标的总评测成本 C_total**：达到同一目标分数所消耗的总评测量（节点数 M × 每节点复评量），对照 DGM 式重选。第三条 claim 核心证据；主看杠杆2（M 下降），杠杆1（c_node 下降）分改动类型报告。
- **决策一致性（partial vs full）**：margin-aware 翻转率（主）+ top-weighted τ 及标准 τ（早警/可比）+ 反事实 regret（偶尔，见 §3.5）。衡量杠杆1 降成本是否以决策质量为代价。
- **回退点正确率**：选中回退点与 oracle 落点在谱系上的边距（仅受控注入设置可算）。
- **污染抑制**：回退后重进化复现已知毒改动 S 的比例（越低越好）。
- **attribution 准确率**：前向（A(e) 对受影响任务的 recall）与后向（罪魁边定位）分别报告——两者要求不同（recall≈1 vs argmax），不可合并。

### 4.4 评测规模

先用 pi evals 长程/序列任务做全部快速迭代与消融（成本可控）；SWE-bench(Verified 子集) 只用于最终 headline 表，控成本。谱系代数控制在几十代量级（harness 层每节点要跑一批任务，比任务轨迹层贵）。

---

## 5. 风险与规避

- **Attribution 不准 = 命门**：退错地方会比盲回退更差。规避：(a) hash/依赖式的"硬信号"（哪条边改了哪个组件、哪个任务受影响）作为 sound 下界，taxonomy+LLM 诊断作为软信号叠加；(b) 冻结归因器 + 周期 audit 兜住漂移（见 §3.5 两条防线）；(c) 把 attribution 准确率（前向 recall / 后向定位）当独立指标，敏感性分析。
- **成本**：谱系层评测贵。规避：partial 复评 + 小任务集迭代 + SWE-bench 只跑最终表。
- **baseline 必须打赢"重选 parent"**：靠 §4.2 的延迟缺陷序列凸显价值；若在这类序列上仍不敌 DGM 式重选，claim 不成立，需如实报告。
- **过拟合到构造序列**：除受控注入设置外，需在 held-out 任务序列（D_test）上复现优势。
- **与 MARS 混淆**：写作中显式切割"进化谱系层 vs 任务轨迹层"，并把 MARS 列为方法灵感来源而非同类。
- **评估器隔离（设计原则）**：Attr-fwd / Attr-bwd 冻结、不进进化回路、schema 锚 task-side；否则进化体可 hack 归因器，且偏差界变移动靶（见 §3.5）。

---

## 6. 关键参考

- DGM: Darwin Gödel Machine, ICLR 2026 (arXiv:2505.22954) — archive/tree、重选 parent、无回退。
- HyperAgents / DGM-H (arXiv:2603.19461) — QD parent selection、stepping stones。
- MARS (arXiv:2607.29055) — 任务轨迹层的 Rollback/Guided Repair/Continuation + failure taxonomy（机制灵感）。
- Safe Harness Self-Evolution (arXiv:2609.08175) — 单线更新的理论界（理论动机）。
- When Self-Evolution Backfires / VaG (arXiv:2608.05810) — 污染不可逆、pre-commit gate（污染抑制对照）。
- Self-Harness (arXiv:2606.09498)、Ouroboros (arXiv:2608.08311)、HarnessDev (arXiv:2609.01437)、SoL-Pi (NVlabs, pi-based 效率自进化) — harness 自进化大盘，划清"加 vs 退"的差异。
- 综述: Self-Evolving Coding Agents (arXiv:2608.03392)；awesome list: github.com/zhouhao1024/Awesome-Self-Evolving-Coding-Agents。

## 7. pi 落地 hook（备忘，实现阶段用）

- 谱系树：复用 session tree / fork / branch summary；或 extension 内维护 EvoTree 索引，节点 patch = extension 版本 diff。
- 版本切换：`/reload` + resources_discover 切 harness 版本。
- 评测：`packages/evals/src/pi-harness.ts` 的 `createPiCodingAgentHarness`（已按 task 起隔离 session、记 token/cost/tool trace）+ `evalHarnessTable`。
- 状态持久化：`appendEntry`（CustomEntry 不进 LLM 上下文）存 EvoTree/branch_stats。
- 不碰 core 主循环 / provider，保 no-fork、归因干净。

## 8. 命题：partial 复评的 decision-consistency 与成本上界（证明草稿）

目标：在理想假设下证明 partial 复评（杠杆1）不改变搜索决策、且严格降成本；真实不完美的差距靠 §3.5 的度量与 §4 的实验兜底。这是附录级 formalization，非严格定理。

**记号（沿用 §3.4/§3.5）**：谱系树节点 = harness 版本；边 e = 一次改动。评测子集 `𝒯`（评一个版本实际跑的那批任务），`|𝒯|=B̄`（同 §3.4，非全 benchmark）。任务 t 上版本 v 的（去噪期望）分数 `f_t(v)`，版本总分 `F(v)=Σ_{t∈𝒯} f_t(v)`。父版本 `v_p`、改动 e 得子版本 `v_c`。受影响集 `A(e)={t∈𝒯 : f_t(v_c) ≠ f_t(v_p)}`。归因器给出估计 `Â(e)`。full 复评：对所有 t∈𝒯 重算 `f_t(v_c)`；partial 复评：只对 `t∈Â(e)` 重算，其余取缓存 `f_t(v_p)`，得估计分 `F̂(v_c)=Σ_{t∈Â(e)} f_t(v_c) + Σ_{t∈𝒯∖Â(e)} f_t(v_p)`。

**假设**：
- **(A1) 局部性 / 安全覆盖**：`Â(e) ⊇ A(e)`（归因器不漏任何真正受影响任务；即前向 recall=1）。
- **(A2) 未受影响任务分数不变**：对 `t∉A(e)`，`f_t(v_c)=f_t(v_p)`（缓存分数对该子代仍有效）。
- **(A3) 确定性 / 去噪**：`f_t(·)` 视为去噪期望值（多 seed 平均后噪声可忽略；否则命题按期望成立，方差项单列）。

**命题 1（无偏，pointwise）**：在 (A1)(A2)(A3) 下，`F̂(v_c)=F(v_c)`。
*证明草稿*：拆两部分。`t∈Â(e)`：partial 直接重算，等于 full。`t∉Â(e)`：由 (A1) `Â(e)⊇A(e)` 得 `t∉A(e)`，再由 (A2) `f_t(v_c)=f_t(v_p)`，缓存值即真值。两部分逐项等于 `F(v_c)`，求和相等。∎

**推论 1（decision-consistency）**：任何只依赖版本分数比较的决策——D-accept（`sign(F(v_c)−F(v_p))`）、D-select（对兄弟集按 F 排序）、D-rollback（祖先里 `argmax F`）——在 partial 与 full 下结果**完全一致**。（由命题1，被比较的分数逐个相等，故任意比较/排序/argmax 不变。）这说明理想假设下 partial 复评是搜索决策的充分统计量，"决策一致"是无偏的免费推论，无需退而求其次。

**命题 2（成本上界）**：设每任务评测单价为 1，audit 每 K 个节点做一次全量。到达同一目标分数需评测 M 个节点时，
```
C_partial ≤ Σ_{i=1}^{M} |Â(e_i)| + (M/K)·B̄
C_DGM-full = M·B̄     (每节点固定子集 B̄, 从零新跑)
```
当平均 `|Â(e)| = ρ·B̄`（ρ = 平均受影响比例）时，`C_partial ≈ (ρ + 1/K)·M·B̄`，相对 full 的省幅因子 ≈ `ρ + 1/K`。局部改动 ρ≪1 → 大幅省；全局改动 ρ→1 → 不省（退化成 full + audit 开销，故 §3.5 的门控在 ρ 估计大时直接走 full，避免 1/K 的额外 audit 浪费）。*注*：此处只算杠杆1；杠杆2（回退剪枝降 M）与之相乘，是独立且鲁棒的省幅来源。

**假设失效时会怎样（连接 §3.5 的度量，防审稿人"理想假设太强"）**：
- **(A1) 破**（recall<1，漏评受影响任务）→ 命题1 变有偏：`F̂−F = Σ_{t∈A(e)∖Â(e)} (f_t(v_p)−f_t(v_c))`。偏差符号可正可负；正偏（高估子代）正是 C2 被优化器利用的方向。→ 由 margin-aware 翻转率 / top-weighted τ 监测，audit 估计其量级。
- **(A2) 破**（改动有全局副作用但归因器判为局部）→ 等价于 (A1) 破，同上。
- **(A3) 破**（评测有噪声）→ 命题1 按期望成立，翻转由噪声与偏差共同驱动；靠 `|Δ_full|>ε` 的 margin 过滤把噪声级翻转排除，多 seed 压方差。

**可证伪落点**：命题给的是"假设成立则无损省成本"的上界；真实中假设部分破。§4.3 的决策一致性三层度量就是测"破得有多严重、audit 能否兜住"。若在合理 K 下 margin>ε 翻转率仍高或累计 regret 显著（(A1)/(A2) 破得太厉害）→ 杠杆1 不成立，退回只保杠杆2。

## 9. Future work（备忘）

- **模型能力 vs 累计 regret**：强模型单次有害 flip 幅度可能更大（决策更 critical），但其前向 recall 更高、自我纠偏更强可能压低 flip 频率与净 regret，净效应非平凡。可换 base model 跑多轮完整进化验证，并据此让 audit 周期 K 随模型能力自适应。成本高，暂不做，仅此备忘。
