# 自进化 Self-Harness 补充分析

配套文档：`OBSERVATION_MEMORY_DESIGN.md`（A/B/C 记忆系统）。本文分析在 pi 上做"自进化 self-harness"的可行层级、与 A/B/C 的结合点、以及每层的工程量与风险。目的是帮你在"作为 A/B/C 升级 / 独立自进化主题"之间做决定。写完供选型，不含实现代码。

---

## 0. pi 已具备的自进化原语（已核对）

pi 自我定位就是 "self extensible coding agent"（README）。自进化需要的底层原语已经存在：

- skills / extensions 都是磁盘普通文件，启动时从 `~/.pi/agent/skills`、`.pi/skills`、`.pi/extensions` 发现（`packages/coding-agent/docs/skills.md`）。skills 走渐进式披露：平时只有 description 进 system prompt，匹配到才加载全文。
- eval harness 已有 `reload` 原语（`packages/evals/src/pi-harness.ts:212`，input 类型 `packages/evals/src/pi-harness.ts:29` 支持 prompt/reload 序列编排）。
- `packages/evals/src/extensions.eval.ts:98-111` 本身就是一条完整自著循环测试：prompt 让 agent 写一个带 `hello` 工具的 extension -> `reload` -> 再调用该工具。也就是"agent 写出新能力 -> 重载 -> 立即可用"这条闭环 pi 已跑通且有测试。

结论：自进化不是从零造框架，而是给"写文件 + reload"这条已有闭环，接上"从经验学 -> 度量 -> 保留或回滚"的反馈回路。

---

## 1. 四个自进化层级

"self-evolving" 容易变成没有度量支撑的口号，审稿人对此警惕。把它拆成可证伪的四层：

```text
L1  记忆级：累积/蒸馏 episodic memory                  <- A/B/C 本身已覆盖
L2  程序级：从重复经验写出可复用 skill                  <- 新意所在
L3  harness 级：agent 改自己的 extension(工具/检索/compaction 策略)
L4  参数级：用反馈信号调 retrieval 权重 α..λ、失效阈值等
```

L1 已由 A/B/C 覆盖，不再展开。下面逐层分析 L2-L4。

---

## 2. L2 程序级自进化：经验 -> skill

### 机制

```text
执行多个同类任务
   -> A/B/C 记忆里出现重复模式(同串操作/同类结论反复出现)
   -> 触发蒸馏：把该模式写成 .pi/skills/<name>/SKILL.md
   -> reload -> 该 skill 进入 system prompt 的 description 列表
   -> 后续匹配任务自动加载并复用
```

### 落地 hook

- 写文件：普通 fs 写到 `.pi/skills/`。
- 生效：`resources_discover` 返回额外 skill 路径，或直接 reload。
- 触发时机：`agent_settled`（一次任务彻底结束）里检测重复模式。
- 持久化候选/统计：`pi.appendEntry(customType, data)`，不进 LLM 上下文。

### 与 A/B/C 结合

因子 C 的分层是关键：L1 卡片是"具体一次执行"，反复出现的 L1 卡片模式就是 skill 的原料。因子 A 的检索用来判断"当前任务是否命中已有 skill 覆盖的模式"，避免重复学。

### 工程量 / 风险

- 工程量：中。难点在"重复模式检测"和"什么时候值得固化"，不是写文件本身。
- 风险：skill 越积越多、互相冲突、过拟合 eval 集。这正是需要因子 B 当 gate 的地方（见第 5 节）。

---

## 3. L3 harness 级自进化：agent 改自己的 extension

### 机制

agent 把高频操作封装成一个新 tool，或调整自己的检索/compaction 策略代码，写成 extension，reload 生效。

```text
反复手动执行 "grep X -> 读文件 -> 定位符号"
   -> 蒸馏成一个 find_symbol 工具的 extension
   -> pi.registerTool 注册, reload
   -> 后续一步到位
```

### 落地 hook

- `pi.registerTool(ToolDefinition)`（`packages/coding-agent/src/core/extensions/types.ts` registerTool），已被 `extensions.eval.ts` 证明可用。
- 动态注册示例：`packages/coding-agent/examples/extensions/dynamic-tools.ts`。

### 工程量 / 风险

- 工程量：中高。agent 生成的 extension 代码要能通过 `npm run check`、不炸主循环。需要沙箱/校验层。
- 风险：安全与稳定性。agent 写的代码直接进自己的运行时，坏代码可能让 harness 崩。建议加：生成后先在隔离 session 校验、失败即回滚。
- 边界：只让它改"工具/策略"类 extension，绝不碰 core 主循环（见第 6 节）。

---

## 4. L4 参数级自进化：反馈驱动调参

### 机制

不改代码，只调 A/B/C 内部的可调参数：

```text
Score(m,q) = α·Semantic + β·Task + γ·Importance
           + δ·Freshness + ε·Evidence - λ·TokenCost
```

以及失效阈值、逐出阈值、生命周期经验值。用任务反馈信号（成功率、token、stale 命中）做在线或离线调整。

### 落地

- 参数存在 extension 内部状态，`appendEntry` 持久化，`session_start` 恢复。
- 反馈信号来自 eval harness 的 usage（token/cost）和你自建的 stale-retrieval 打点。

### 工程量 / 风险

- 工程量：低到中。最容易做，但单独发论文分量不足，更适合当一个 ablation 轴或 self-evolution 的一个维度。
- 风险：调参易过拟合到 eval 集，必须 held-out 验证。

---

## 5. 关键洞察：validity 从 observation 推广到 learned artifact

这是把 A/B/C 和自进化真正缝合起来、且别人没做的点。

普通自进化系统只 learn，不 unlearn，于是 learned artifact 会过期：

```text
学到 skill: "用 pytest -k 跑单测"
   -> 项目换成 unittest / 换了 test runner
   -> 这个 skill 现在是错的, 但系统还在用

缓存结论: "foo 模块用递归下降解析"
   -> 重构后改成状态机
   -> 结论 stale, 误导后续决策
```

因子 B 本来是给 observation 打 validity。把它推广到 artifact：

```text
每个 learned skill/tool/参数 都绑定 validity:
  boundTo: file(path)@hash / env signature / test-runner 指纹
  绑定对象变化 -> artifact 标 stale -> 停用并触发重新学习
```

于是得到一个可证伪的主张：

> Self-evolving agent 不仅要 learn，还要 unlearn / invalidate 过期的自生成能力。带 validity gate 的自进化，在长程 coding 任务上比无 gate 的自进化更稳、更省。

这个 "validity-gated self-evolution" 比"agent 会写 skill"有意思，也贴合你 RAG/memory 背景。

---

## 6. pi 哪些部分适合进化，哪些别碰

| pi 部件 | 适合进化 | 进化方式 | 落地 hook | 层级 |
|---|---|---|---|---|
| Skills | 最适合 | 从重复经验蒸馏 SKILL.md | 写 `.pi/skills/` + resources_discover/reload | L2 |
| Extensions/自定义工具 | 适合 | 写新 tool 封装高频操作 | registerTool + reload | L3 |
| 检索/记忆策略参数 | 适合 | 调 Score 权重/失效阈值 | extension 内部状态 + appendEntry | L4 |
| Compaction 策略 | 适合 | 学什么该逐出/长留 | session_before_compact | L3/L4 |
| System prompt 片段 | 谨慎 | 注入学到的项目约定 | before_agent_start(可改 prompt) | L2/L3 |
| Agent 主循环 / drive loop | 不建议 | core，改了 attribution 糊且违背 no-fork | — | — |
| Provider / model 层 | 不建议 | 与研究无关，变量太多 | — | — |

原则：进化"策略层/能力层"（skills/tools/参数/compaction），不碰"机制层"（主循环/provider）。既保 no-fork 干净归因，也把自进化限制在可度量、可回滚边界内。

---

## 7. 可投稿的组合形态

标题候选：Validity-Gated Self-Evolution for Long-Horizon Coding Agents。

自进化回路：

```text
1. 执行任务, observation 进 A/B/C 记忆(可检索、带 validity)
2. 检测重复模式(同类 task 反复用同一串操作/结论)
3. 蒸馏候选 artifact: skill / tool / 参数
4. reload 后在 held-out 任务上 A/B 度量 lift
5. lift 显著且未失效 -> 保留; 否则回滚
6. 绑定的文件/环境 hash 变化 -> artifact 标 stale -> 重新学习
```

比纯 A/B/C 多两类指标：

- 跨任务迁移：任务序列上，后面的任务是否因前面学到的 artifact 更快/更省 token。这是自进化的核心证据。
- Stale-artifact 触发的失败率：证明 validity gate 防住了过期能力带来的错误。

pi eval harness 支持 task 序列 + reload（`pi-harness.ts:29` input 数组编排 prompt/reload），这套回路能在现有 harness 上跑，无需另造框架。

---

## 8. 三种定位对比

| 定位 | 主 claim | 工作量 | 风险 | 适合场景 |
|---|---|---|---|---|
| A. 作为 A/B/C 升级 | validity-aware observation memory；自进化是扩展章节 | 中 | 低 | 想稳妥出一篇，一条主线 |
| B. 独立自进化主题 | validity-gated self-evolution；A/B/C 降为支撑 | 高 | 中 | 想冲更大故事，愿做 L2/L3 自著回路 + 迁移评测 |
| C. 两篇拆分 | 记忆一篇 + 自进化一篇 | 高 | 中 | 有足够时间和算力 |

我的建议：先按 A 落地（因子 B 是 headline），把自进化的 L4/L2 作为"扩展实验"跑起来。如果迁移指标漂亮，再升级成 B 甚至拆成 C。理由：validity 这个点在两种定位下都是核心，先把它做扎实，进化只是把 validity 从 observation 推广到 artifact，增量清晰、不返工。

---

## 9. 风险与规避

- "自进化"赛道拥挤，纯 demo 多。规避：绑死 validity gate，claim 收窄成"带失效判定的自进化更稳更省"。
- agent 自写代码(L3)的安全与稳定。规避：生成后隔离校验 + 失败回滚，只允许改策略/能力层。
- 过拟合 eval 集。规避：所有"保留 artifact"的决策必须在 held-out 任务上度量。
- 迁移收益难显著。规避：设计任务序列时故意让后续任务复用前面模式，同时放入"环境变化使旧 artifact 失效"的对照任务，凸显 validity gate 价值。

---

## 附：关键锚点

- 自著循环测试：`packages/evals/src/extensions.eval.ts:98-111`
- reload 原语与 input 序列：`packages/evals/src/pi-harness.ts:29,212`
- skills 发现与渐进披露：`packages/coding-agent/docs/skills.md`；源码 `packages/coding-agent/src/core/skills.ts`
- registerTool / 动态工具：`packages/coding-agent/src/core/extensions/types.ts`；`examples/extensions/dynamic-tools.ts`
- compaction 替换：`examples/extensions/custom-compaction.ts`；`session_before_compact`
- 自定义状态持久化：`session-manager.ts` appendCustomEntry（CustomEntry 不进 LLM 上下文）
</content>
