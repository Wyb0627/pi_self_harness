# Diagnosis-Guided Rollback for Self-Evolving Harnesses

本文件记录我们想做的研究方向、与最相关三篇工作的逐点对照、防审稿人弹药、problem statement，以及在 pi 上可跑的最小实验设计。定位：在 pi harness 上做一个不 fork core 的研究 extension，支撑一篇技术报告 + 开源仓库。写完供对齐，不含实现代码。

配套：`SELF_EVOLUTION_ANALYSIS.md`（早期分层设想，仅参考）、`OBSERVATION_MEMORY_DESIGN.md`（记忆系统，仅参考）。本方向已收窄，不再沿用那两份文档的框架。

---

## 0. 一句话方向（headline）

> 现有 harness 自进化把进化史当成"只增 archive + 按分数重选 parent"，**回退是缺失的一等操作**。我们把进化谱系建成可回放的 patch lineage：LLM 和依赖关系只产生软候选，**可执行反事实 replay 直接定位一最小充分移除集**；系统回退到最早移除 patch 之前，再重放与移除集不依赖的后续有效改动。完整致因 family 只在解释确有价值时追加恢复，不再作为默认必付成本。

可证伪 claim：这种"软诊断 + 主动反事实验证 + rollback-and-replay"，在相同评测预算下，比 DGM 式"重选 parent"、固定"回退一版 / keep-revert"、以及线性祖先扫描，**更准确识别交互性根因，并在满足成本门控时减少 replay**。若真实失败上无法保持修复成功率，或总 replay 成本不低于基线，claim 被推翻。

**成本边界**：低成本不是无条件保证。当前实验只支持两个门控后的快路径：(a) 谱系足够深时才启用概率二分；(b) 候选 slice 覆盖不超过 30% 的边、且审计 recall 至少 95% 时，才用 sliced ddmin。其他情况回退到 full ddmin，以准确性优先。详见 §3.4 与 §4.2。

**DGM released-data 最新结论（E8）**：在 12 条确定性抽样的单调延迟回归上，CLM 借可执行验证达到 12/12 修复，但 DeepSeek 先验 top-1 仅 4/12，平均 evaluator probes 为 1.5000，高于线性扫描的 1.0833，故预注册的"精准且低成本"联合假设已在成本项上被否决。该离线 replay 不能生成 CLM 改变 parent 后的反事实 agent，因此不能据此声称超过 DGM 的 fixed-D60 50.00% 端点；DGM initial agent 也不是当前 TypeScript Pi，公开数据中没有可比的原版 Pi predictions。当前结论是 **REVISE，不是 GO**。

---

## 1. 问题定义

Harness 自进化本质是一个无梯度搜索：提出对 harness 的改动（prompt / tool / 检索 / compaction / 控制策略）→ 在任务集上评测 → 保留有用的 → 继续。这条搜索路径天然是一棵树：一次改动是一个节点，改动叠改动形成谱系。

真实进化里失败不可避免，且有两个特点让"回退"变成核心而非边角：

1. **缺陷延迟暴露**：某个早期改动引入的问题，可能要到很多代之后、在特定任务上才崩。此时"退一版"退不到病灶，"退到当前最高分节点"可能恰好丢掉了后续所有有效增益所依赖的那个前提改动。
2. **失败分支不是垃圾**：从回退点到崩溃点这一整段 trajectory，包含"哪些改动其实有效、哪个是毒、什么组合导致回归"的信息。丢掉它等于每次失败都从零重来。

### 1.1 核心失败模式：毒性前提（toxic stepping stone），不只是显性 bug

回退要解决的失败，有强弱两个层次，第一版聚焦更本质的强版：

- **弱版（显性回归）**：某改动本身带 bug，只是当时评测没测出来，后代在特定任务上崩。判据是"某祖先自己对不对"。
- **强版（毒性前提）**：`initial→A→B→C→D`，**C 在它自己的评测上真通过、C 本身也没 bug**，但 B→C 这一步引入了某种结构性约束/方向，使得**任何基于 C 的后续改动要么容易错、要么要付很高代价才对**。C 是"能过评测、但走不远"的死胡同前提。此时正确决策是：**即使 C 通过，也不该在 C 上继续长，应退到 B 换方向。** 判据不是"C 自己对不对"，而是"以 C 为根的整棵子树的下游产出率/成本"。

强版之所以是主战场，且被现有系统系统性漏掉，有两个机制性理由：

1. **分级评测 = 结构性盲区，不是全量测试**。DGM 每个新 agent 只在 10→60→(晋级才)200 的子集上评测；绝大多数节点从未跑过全量。所以"在被评的子集上通过、实则是差前提"不是罕见，是结构性普遍。这与 §3.5 的 C2（优化器钻缓存/评测盲区）是同一机制。
2. **点式分数无法表示交互原因**。一个失败可能要求多个历史 patch 同时存在；此时"第一个显性失败版本"、"单边嫌疑最高"和"最早潜伏前提"是三个不同对象。DGM 的 parent selection 只看 score+novelty，不构造可执行反事实，也不返回致因集合。我们原先用 DGM 释放树声称 11 个分叉中有 4 个贪心/子树最优分歧，但审计发现该统计混用了 10/60/200 任务的 raw accuracy；统一到每个分叉的共同任务集并使用 set-valued oracle 后，**严格分歧只剩 1/11**。因此旧的 4/11 不能作为真实证据，DGM 树只保留作单调性和浅路径成本分析。

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

最终候选方法暂名 **Causal Lineage Minimization (CLM)**。三个部件对应三条可消融的因子，全开是 full method，逐个关掉即 ablation。

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
     因子A ─────────► Candidate Prior + Dependency Slice
                    │  (只排序/缩小候选，不作最终裁决)
                    ▼
     因子B ─────────► Active Counterfactual Replay
                    │  (singleton → ddmin；必要时 full fallback)
                    ▼
     因子C ─────────► Rollback-and-Replay Plan
                       (退到最早致因边之前，重放独立的后续增益)
```

- **因子 A（候选先验）**：用 failure bundle、patch manifest、组件依赖和历史 branch credit 给 lineage edge 排序。LLM 输出是 soft prior；不得据此硬删除候选。
- **因子 B（反事实验证）**：先验证“从完整 lineage 删除最高先验 singleton”能否修复；不能时，在安全 slice 上对**移除集**运行 ddmin，返回一最小充分移除集。slice 的全部移除仍不能修复时立即扩展到 full lineage。探针有噪声时使用奇数次 paired replay 和多数票。
- **因子 C（rollback-and-replay）**：落点为移除集中最早 patch 的父 checkpoint；对其后的 patch 按依赖拓扑重放，只保留不依赖移除集且通过 probe 的增益。完整 dependency-safe replay plan 必须再执行一次验证。`apply` 默认 dry-run，必须经用户确认；不执行 `git reset`。

### 3.1 调度与成本门控

1. 已知 good/bad endpoint 且 lineage 足够深、probe 近似单调时，可先走概率二分快速定位显性边界；浅路径不启用。
2. 始终验证 full failure bundle 能在当前 artifact 上复现；不能复现则 abstain，不给回退方案。
3. 候选 slice 比例 `<=0.30` 且历史审计 recall `>=0.95` 时启用 sliced ddmin；否则直接 full ddmin。
4. sliced 结果必须通过 full-context repair verification；验证失败则 full fallback。
5. selective replay 因依赖/文件重叠额外跳过 patch 后，必须验证最终 plan 对应的精确 active set；失败则 abstain。
6. 默认输出一最小充分移除集、rollback checkpoint、可重放 patch、probe 明细和 fallback/abstain 原因；完整 set-valued causal family 是可选解释模式。

这里的关键变化是：**LLM 负责提出值得测什么，replay 负责决定什么是真的**。这避免了 E0/E1 的静态判断失准，也能表示单边排序无法表达的交互原因。

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

**每节点成本拆解（决定 partial 复评能省多少的前提，读原文核对）**：DGM 每生成一个新 agent，成本 = **提议**（self-modify：o1 诊断 + coding agent 生成一个 diff，Appendix C.3）+ **评测**（staged，§4.2）。两者量级差很大：
- 提议 ≈ **1~2 个任务当量**（agent 跑一遍自己的 repo 出 diff），是小头。
- 评测走**分级**：先 10 个任务过"还能编辑代码"的功能门 → 60（10+50）→ 只有 >40% 且进 archive 前二名才上 200（Appendix E.2）。成本锚点（E.1）：SWE-bench 60 任务 ≈ $350（约 $5.8/任务），整轮 80 代 ≈ $22,000。评测是**绝对大头**。
- 结论：DGM 的成本压倒性地在"对不断生成的新孩子做评测"这一侧。**但注意**：这块**已经被 staging 压过**——多数 agent 只吃到 10 个任务就淘汰，B̄ 本来就不大。

**这对两个杠杆的直接含义（回答"partial 到底能省多少"）**：
- partial 复评（杠杆1）**只砍评测、完全不碰提议**，且攻击的正是 DGM 已用 staging 优化过的那段；再叠加"10 任务功能门是砍不掉的硬地板"+"父代 staged 缓存分本就残缺、可复用的少"，**partial 的边际收益有限，且只对局部改动成立**。所以它是 optional 加成，不是省 token / LLM 调用的主力。
- 真正能大幅省 token / call 的是**减少被评测的节点数 M（杠杆2）**：DGM 的浪费主要来自"不停从坏区/污染子树继续生孩子"，每多长一个注定失败的孩子就要付一整套（提议 + 至少 10 任务门 + 可能 60）。回退剪掉污染子树**同时砍掉提议和评测**，且与改动是否局部无关。**故 token/call 的省钱故事挂在杠杆2，不挂在 partial 复评。**

**统一成本模型**（用它，别用"我的搜索空间比它小"这种硬定理）：

```text
总评测成本 C_total = (被评测的节点数 M) × (每节点评测成本 c_node)
```

术语约定（全文统一）：**B̄ = 双方可比的同一评测子集大小**，即"评一个 harness 版本时跑多少个任务"。DGM 用固定子集（10→50/60→少数晋级到 200，见上），我们的"full 复评"也以同一个子集为基准。**B̄ 不是全 benchmark 任务总数**——若按全集算会高估 DGM 成本，正好犯我们自己立的"别夸大 DGM 成本"的戒。

我们从两个正交杠杆同时压这个乘积（注意：这里的"杠杆1/杠杆2"是**成本杠杆**，与 §3 方法组件的"因子 A/B/C"是两套不同编号，别混）：

- **杠杆1 · 降 c_node（partial 复评）**：DGM 每节点从零跑一批任务，成本 ≈ B̄（已被 staging 压过，见上）。我们借因子 A 的 attribution，只对一次改动 e **影响到的任务子集 A(e)** 复评，其余用缓存分数，c_node 从 B̄ 降到 |A(e)|。**关键限制：这只对"局部改动"成立（|A(e)| ≪ B̄）；对全局改动 |A(e)|≈B̄，几乎不省——详见 §3.5 失效条件。** 且它只砍评测、不碰提议，攻击的又是 staging 已优化过的段，**边际收益有限**，是 optional 加成，不是普遍省。
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

不自造任务数据集（会被 argue 挑分布）。分三个用途，用途不同、数据来源不同：

**用途 C · 第一版 idea 验证（因子 A+B 的决策质量）——离线 replay DGM 释放的真实进化树。**
DGM 开源结果（`DGM_results/swe_results.zip`，本仓库已下载）给出 SWE 上一棵**真实进化树**：约 83 个节点，其中 46 个有非空分数。每节点含 `parent_commit`（父指针→树结构）、`entry`（改动标签）、`self_evo.md`（自我修改完整推理）、`model_patch.diff`（相对父节点改动）、`predictions/*.md`（每任务完整 agent 轨迹=debug 信息）、`overall_performance`（`accuracy_score` + 每任务 `total_resolved_ids`/`total_unresolved_ids`/`total_emptypatch_ids`）。

这批数据让第一版**零 Docker、零重跑、用 DGM literal 树和分数**就能验证回退决策：给回退 LLM 喂（失败任务/差前提 + 沿路各节点 diff/entry/self_evo + 各祖先在相关任务上的对错 + 失败节点轨迹），让它选回退点，再用 DGM 现成分数离线判分，对比 Ours vs 盲回退-1 vs DGM 重选。

**信息隔离原则（第一版的核心方法论，写死）**：决策器与 oracle 用两套不相交的信息，绝不能混。
- **决策器（被测方法 = LLM 自行决策）只看决策时刻已有信息**：当前错误/失败任务、各节点 `model_patch.diff`、`self_evo.md` 推理历史、截至当前的分数。**禁看任何下游子树结果**。它做的是**前瞻判断**"某父节点下面的子树是否有前途"，这与真实部署一致（回退时下游本就还没发生）。方法本身因此天然无幸存者偏差。
- **oracle（判分 gold label）才用真实下游**：从 DGM 已释放的下游结果离线算，不参与决策，只事后判分。用未来信息在这里合法，因为"前提到底好不好"的标准答案只能由"后代实际长成什么样"定义。
- **不能纯用 LLM 当评判**：那是用 LLM 判 LLM、循环论证，无独立 ground truth。离线唯一可得的独立标准答案就是 DGM 真实下游。

- **强版判据（主）**：oracle = 在一个分叉上**子树产出最好的那个兄弟分支**（操作化为 subtree-best：该孩子整棵子树内可达最高分；将来可加"达标成本"作第二维），而非当前分最高的兄弟。该判据必须在同一共同任务集上计算并保留并列集合；修正后 11 个有效分叉中只有 1 个严格分歧，只能作个案，不能支撑统计性 claim。
- **弱版判据（sanity check）**：oracle = 任务 t 最后一次通过的祖先之前的显性回归点。
- **子集不均必须处理**：DGM 分级评测导致节点评测子集不同（10/60/200），任何跨节点比较**只在两节点评测子集的交集上做**，否则"后代没评该任务"会被误判成回归。
- **诚实边界（写死）**：(a) 节点是 DGM 的 coding-agent 代码，不是 pi harness，故这是"回退决策器"验证，不是 pi harness 闭环；pi harness 化是后续步骤。(b) 树浅（83 节点里 53 个叶子），强版信号只够 case study，不足统计显著；要更强统计靠用途 B 的受控注入造密集样本。(c) **因子 C（回退后再进化）离线不可验证**——再进化会产生 DGM 树里不存在的新节点，那需要真跑（Docker），推迟到 main result 阶段。(d) oracle 的 subtree-best 带幸存者偏差（DGM 投喂多的分支更容易长深/长高），故 claim 收窄为"方法能否预测出 DGM 这次真实探索中最终产出更好的分支"，而非"判断前提的先天质量"；深度归一 / 单步增益率作 oracle 的 robustness check（同样只读现成数据，不重跑）。

**历史第一轮离线结果（deepseek-v4-flash，11 个分叉，每分叉 5 次多数票；已撤回）**：
- v1 简短前瞻 prompt：全分叉 hit=0.4545、mean regret=0.0538；4 个关键 disagreement 分叉 hit=0/4、mean regret=0.1363。
- v2 强制逐候选结构化分析（能力、结构约束、通用性、可组合性、下游风险，最后才参考当前分）：全分叉 hit=0.3636、mean regret=0.0797；关键分叉 hit=1/4、mean regret=0.1533。55/55 次返回结构完整，无 JSON/fallback 失败；关键分叉单次投票命中 7/20，但多数票不稳定。运行约 42 分钟，显著慢于 v1 的约 2 分钟。
- **原预注册判据**：v2 预期关键分叉至少 1/4 命中且 regret<greedy 0.1353；原始计算触发了 kill 条件。但后续审计发现 oracle 无效，因此不能把它写成正式证伪。可保留的结论是：现有实验没有显示静态 LLM 预测的优势，且增加了显著延迟，不值得继续无界调 prompt。
- **退化归因**：v2 修对 1 个关键分叉（regret -0.0119），但把两个 v1 已选对的普通分叉改错（regret 分别 +0.0787、+0.1213），另有两个 5 票 plurality 出现 2-2 平票，其中 `initial` 分叉因不稳定 tie-break 新增 +0.0797 regret。结构化 prompt 让解释更完整，却过度奖励"模块化/低耦合/易修复"的改动；这些静态属性未必转化成真实下游产出。

**可信度审计与撤回**：
- 上述 v1/v2 数字把 10/60/200 staged subset 的 raw accuracy 直接跨节点比较，违反本节自己的共同任务集规则；plurality tie 又被插入顺序任意打破。它们只能说明 prompt 行为，**不能作为回退准确率或 DGM 分歧率证据**。
- 修复后，每个分叉只在所有候选共有任务集上重算，oracle/greedy 都允许并列；11 个分叉中严格 `greedy ∩ oracle = ∅` 的仅 **1 个**。旧的 “4/11 (36%)” 已撤回。
- 因此 H1 的可靠结论只保留为：静态 LLM 预测没有显示出可复现优势，且延迟从约 2 分钟增至约 42 分钟；不再报告旧 regret 为方法 headline。

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

**用途 B 第一轮实现与结果（deepseek-v4-flash，positive control）**：
- 数据：12 条人工控制的 harness 历史，其中 10 条是"早期埋入、后代才暴露"的延迟缺陷，2 条是"最新边就是根因"的对照，防止模型靠"固定多退几版"取巧。案例覆盖 compaction 丢契约、跨 repo 缓存污染、retry reset 丢进展、框架专用 validator、并行工具 race、summary 丢 error state、cwd 缓存、静态 tool allowlist、token budget 漏计、deletion patch 误拒、reload schema stale、timeout 单位错误。
- oracle 定义：**最早引入该潜伏条件的边**之父节点；即使该边当时尚未造成失败、后续边才把它接入阻断路径，也按最早埋雷点标注。这与 §1.1 的强版定义一致。
- 条件：`llm-full` 看版本历史 + 当前错误 + reproduction observations + debug evidence；`llm-no-debug` 去掉 debug，其余相同；每案例 5 次。oracle 字段不进 prompt。
- 结果（独立重跑，单票）：盲退一版 exact/clears=0.1667/0.1667；最高分祖先=0.1667/0.1667；`llm-no-debug`=0.9500/0.9500；`llm-full`=1.0000/1.0000，且 culprit-edge attribution=1.0000。
- 结果（案例 plurality，平票算 abstain）：`llm-no-debug` exact/clears=0.9167/0.9167；`llm-full`=1.0000/1.0000；两者均无平票。
- **撤回过度解读**：case id、错误文本和 debug 直接暴露了机制，五票也共享同一 prompt/data、并非独立样本。该 1.0 只能证明代码链路和输出 schema 可工作，**不能证明 LLM attribution 在真实失败上准确**，也不能成为 headline。

**第二轮主动 replay 结果（E3-E7）**：
- 数据审计发现原 parser 漏掉 evaluator `error_ids`，旧的 245/226/92.24% 与 99.18%/8.1% 统计全部撤回。修正后共有 69 条去重的 start-pass/end-fail episode（9 tasks、22 leaves），其中 56 条单调、13 条非单调。全 69 条上，线性扫描 exact=1.0000、平均 1.4783 probes；二分 exact=0.9710、平均 1.7246 probes，在 13 条非单调 episode 上 exact=0.8462。二分在这棵浅树上不仅不省，反而更贵。
- 合成交互原因（1-3 edges）上，full ddmin clean exact=1.000；sliced ddmin clean exact=1.000、noise 5%/10% exact=0.967。但 40% slice 的平均调用节省只有约 11%-14%，通用 `>=20%` 成本 claim 被证伪。
- prior-first singleton 在 5%/10% noise 下分别省约 24.6%/20.6%，clean 仅约 19%，仍不足以支持无条件 claim。
- sensitivity 显示仅当 slice `<=30%` 且 cause recall `>=95%` 时，safety fallback 后 exact 保持 1.0 且 clean calls 可省约 26%-37%。这成为插件的硬门控；门控外走 full ddmin。

**E8 · DGM released-data CLM 对照**：
- 统一到 initial 节点的 canonical 60 tasks 后，released endpoints 为：initial DGM agent 12/60=20.00%，full DGM best 30/60=50.00%，no-open-ended 14/60=23.33%，no-self-improve 23/60=38.33%（raw 23/59=38.98%，缺失 task 按失败计）。
- 修正后的 41 条 monotone delayed episode 全量离线基线：no-rollback=0、rollback-1=0、score-only DGM proxy=0.1951 repair/exact；linear=1.0000 at 1.0244 probes；binary=1.0000 at 1.3659 probes。
- 注意选择效应：no-rollback=0 由“当前失败”定义保证，rollback-1=0 由“延迟回归且前一 scored state 已失败”的筛选保证；二者只是构造检查，不能当作广义性能优势。
- 预注册 12-episode DeepSeek pilot 只覆盖 4 个 unique tasks / 10 个 leaves：CLM repair/exact=1.0000，但 DeepSeek top-1=4/12、fallback=3/12、平均 probes=1.5000；同样本 linear 为 1.0833。12 次调用报告 52,754 input tokens、181,072 output tokens、767.291 秒。
- **判决：成本 kill criterion 触发，不扩三次重复。** 这只测试 CLM 的 monotone-boundary fast path，不覆盖 interaction ddmin、selective replay 或回退后的反事实进化。CLM 可说打赢了这些筛选 recovery episode 上的 no-rollback、rollback-1 和 score-only proxy；不能说打赢 DGM 的 fixed-D60 50% 最终任务分数，更不能把 no-rollback proxy 冒充原版 Pi。

**第三轮目标重构与结果（E9-E11）**：
- E9 branch quarantine：保守规则在 full DGM 上保留 0.5000 但节省 0%；激进规则节省 86.28% 却把最好端点降到 0.2833。原因是退化叶子无后续成本可剪，而过早剪枝会杀掉真实 stepping stone。该方向否决。
- E10 multi-fidelity promotion：官方固定 split 上 stability gate 以 520 vs 660 task evaluations 保留 0.5000；但 5,000 个无结果依赖的 task rotations 上 best-node recall=0.8946、仅省 6.58%。该方向不满足 95% recall / 20% saving 联合标准。
- E11 **Repair-First CLM（最终算法核心）**：优化目标从“完整恢复 failure-inducing family”改为“直接找一最小充分移除集”。对完整 lineage 删除候选并验证 repair；单边不够时才对 removal set 做 ddmin。这样 conjunctive failure 中删去任一必要 patch 即可停止，不再为解释完整 cause family 付费；alternative causes 则由验证强制联合删除。
- 在 balanced conjunctive/alternative/mixed synthetic families 上，repair-first 相对旧 failure-first 路径减少 42.86%-49.89% probes；clean repair/minimal/optimal=1.000/1.000/1.000，5% noise repair=0.9733（旧方法 0.9833），10% noise repair=0.9700（旧方法 0.9767），均在预注册 2-point non-inferiority margin 内。所有 paired bootstrap 95% call-reduction CI 都严格大于 0；无先验、误导先验和 DGM-like depth 3-6 均通过。
- 插件额外验证 dependency-safe selective replay 的**精确最终 active set**；若因为依赖或文件冲突多跳过 patch 后失败，则 abstain。
- **结论边界**：E11 首次同时通过合成精度和成本门槛，但尚未证明 fixed-D60/200 端点超过 DGM 或原版 Pi。公开 DGM 日志缺 counterfactual children，公开 runner 又缺实际使用过的 140-task promotion 路径；主张升级仍需同模型、同预算的新 evolution runs。

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

- 谱系树：用 CustomEntry 持久化 checkpoint manifest，并把 session entry id 作为对话状态锚点；patch artifact 独立存储，不能假设 `/tree` 会恢复文件。
- 版本切换：恢复受控 artifact 后 `navigateTree` + `reload`；不自动修改 Git 历史。
- 评测：`packages/evals/src/pi-harness.ts` 的 `createPiCodingAgentHarness`（已按 task 起隔离 session、记 token/cost/tool trace）+ `evalHarnessTable`。
- 状态持久化：`appendEntry`（CustomEntry 不进 LLM 上下文）存 EvoTree/branch_stats。
- 命令面：`/rollback checkpoint`、`/rollback diagnose`、`/rollback apply`、`/rollback status`。外部 probe command 通过 manifest 配置；`apply` 必须确认且默认 dry-run。
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
