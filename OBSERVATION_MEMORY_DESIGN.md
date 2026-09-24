# Lifecycle-Aware Observation Memory for Long-Horizon Coding Agents

Design doc. 目标：在 pi harness 上做一个不 fork core 的研究 extension，支撑一篇投学术会议的技术报告 + 开源高星仓库。

本文用 pi 里真实存在的 hook 和文件锚点来落地设计，不写实现代码，先对齐。

---

## 1. 问题定义

Coding agent 在长程任务里会积累大量 observation：文件读取、shell 输出、测试结果、编译错误、agent 中间结论。这些 observation 有两个特点：

1. 量大。原文全留会撑爆上下文，token 成本和延迟都不可控。
2. 生命周期特殊。一个 observation 可能随后就失效了。典型例子：

```text
turn 3: read foo.py  (lines 20-80)   -> observation A
turn 7: edit foo.py                   -> A 里的内容已经 stale
turn 9: 模型需要 foo.py 的信息
```

普通 vector RAG 会把 A 检索出来，导致模型基于过期内容做决策，产生错误动作。这个失效问题在普通文档 RAG 里不存在，是 coding agent 独有的。

### pi 现状（已核对代码）

- pi 没有任何 observation archive / paging / recall 存储。大 tool 输出只是就地截断（默认 50KB / 2000 行，见 `packages/coding-agent/src/core/tools/truncate.ts`）。
- 默认 compaction 是"保留最近 20k token + 把更早的 turn 做 summary"（`packages/coding-agent/src/core/compaction/compaction.ts`，`keepRecentTokens=20000`）。它解决的是上下文溢出，不是语义检索，也不管失效。
- 全仓库无 SWE-bench 或任何外部 coding benchmark 接线（`swe-bench|swebench` 全仓零命中）。现有 evals 都是 pi 行为对比。

所以"从 raw trajectory 构建可检索、可失效、可回溯原文的 observation memory"这块在 pi 里是空白，贡献点成立。

---

## 2. 研究 gap 与核心 claim

对比现有机制：

| 机制 | 解决的问题 | 是否处理失效 |
|---|---|---|
| pi 默认截断 | 单条输出太大 | 否 |
| pi 默认 summarization compaction | 上下文溢出 | 否 |
| SoL-Pi ObservationPack | 旧 observation 重复 replay 太贵 | 否 |
| SoL-Pi EPR | 第一次读巨大 log 太贵 | 否 |
| 普通 vector RAG over trajectory | 历史太多不知道看哪个 | 否 |
| 本工作 | 历史太多 + 部分已失效 | 是 |

核心 claim（论文 headline，窄且可证伪）：

> Coding agent 的 observation memory 必须给每条记忆打 **validity（是否仍然成立）** 分，而不只是语义相似度。加入 validity 后，能在更低 token 成本下降低"因过期记忆导致的任务失败"。

可证伪点：如果 validity 因子对 stale-memory retrieval rate 和 wrong-memory-induced failures 没有可测的改善，claim 就被推翻。这比"我们的 MRR 涨了 2%"更有 systems paper 味道。

---

## 3. 系统架构：一个系统，三个开关

三个候选方向不是三选一，而是同一个系统的三个可拆解因子。全开是 full method，逐个关掉就是 ablation。这样保证 attribution 干净。

```text
                        Raw observation (tool_result)
                                 │
              ┌──────────────────┼──────────────────┐
              │                                      │
              ▼                                      ▼
      ┌───────────────┐                     ┌────────────────────┐
      │ L2 Raw Archive│  (内容寻址, 不可变)   │ L1 Memory Cards    │
      │ obs://<id>    │◄────── source ptr ───│ fact/error/concl.  │
      │ exact bytes   │                      │ file/symbol        │
      └───────────────┘                      │ validity state     │◄── 因子 C
                                             │ importance         │
                                             └─────────┬──────────┘
                                                       │
                     ┌─────────────────────────────────┤
        因子 B  ──────► validity/staleness 打分         │
                     │  (文件 hash 变化 -> stale)        │
                     │                                  │  retrieve (每 turn)
        因子 A  ──────► task-aware retrieval + rerank    ▼
                     │  (semantic + task + freshness)  ┌────────────────┐
                     └────────────────────────────────►│ L0 Hot Context │
                                                       │ 注入回上下文     │
                                                       └───────┬────────┘
                                                               │ 卡片不够?
                                                               ▼
                                                       obs_recall(handle, span)
                                                               │
                                                               ▼
                                                       从 L2 回原文
```

三个因子：

- **因子 A（检索质量）**：task-aware 检索 + source-bound evidence，对标 ObservationPack 的确定性 head/tail。
- **因子 B（有效性/失效）**：validity/staleness 打分 + 文件 hash 失效。coding agent 独有，是 headline claim。
- **因子 C（多级结构）**：L0 hot / L1 cards / L2 archive + 回原文 rehydration。

---

## 4. 组件到 pi hook 的映射（已核对）

每个组件都落在 pi 公开 extension API 的真实 hook 上，不 fork core。

| 组件 | pi hook / API | 文件锚点 | 作用 |
|---|---|---|---|
| L2 归档 + L1 卡片蒸馏 | `tool_result` (can modify) | `packages/coding-agent/src/core/extensions/runner.ts` `emitToolResult`；事件定义 `types.ts` 附近 `tool_result` | 每条 observation 进上下文前，原文写 archive，上下文里换成压缩卡片 |
| 回原文工具 obs_recall | `pi.registerTool(ToolDefinition)` | `packages/coding-agent/src/core/extensions/types.ts` `registerTool` / `defineTool` | 模型主动按 handle+span 取回精确原文 |
| 检索注入（因子 A） | `context` (can modify messages) | `packages/coding-agent/src/core/sdk.ts` `transformContext` -> `runner.ts` `emitContext` | 每个 turn 前把 task 相关卡片注入回上下文 |
| 有效性失效（因子 B） | `tool_result` 里自建逻辑 | 同上 | 对 read/edit 抓路径+内容 hash，edit 后把旧 read 卡片标 stale |
| 替换 compaction（因子 C） | `session_before_compact` | `packages/coding-agent/examples/extensions/custom-compaction.ts`（完整可跑示例） | 旧 turn 逐出成 L1 卡片而非纯 summary |
| 跨会话状态持久化 | `pi.appendEntry(customType, data)` | `packages/coding-agent/src/core/session-manager.ts` `appendCustomEntry`（CustomEntry 不进 LLM 上下文） | archive 索引落 session JSONL |
| 会话恢复时重建索引 | `session_start` + `ctx.sessionManager.getBranch()` | `packages/coding-agent/examples/extensions/tools.ts` 的 restore 模式 | resume/fork 时扫 branch 重建内存索引 |
| 上下文用量观测 | `ctx.getContextUsage()` | `agent-session.ts` `getContextUsage`（返回 tokens/contextWindow/percent） | 决定何时触发逐出 |

关键机制细节（来自代码勘查）：

- `context` handler 收到的是全部 `AgentMessage[]` 的 `structuredClone`，可返回替换后的 messages。这是注入/删除/重写历史的通用入口。
- `tool_result` handler 可返回 `{ content?, details?, isError?, usage? }`，替换后的 content 才是真正进上下文的东西。`details` 会被持久化且在 fork/branch 导航后仍存活，适合存 archive handle。
- `session_before_compact` 可返回 `{ cancel: true }` 或 `{ compaction: { summary, firstKeptEntryId, tokensBefore, usage?, details? } }` 完全替换默认 summary。

---

## 5. 数据结构

### L2 Archive（不可变、内容寻址）

```text
obs://<sha256-prefix>
  ├── raw bytes (完整原文)
  ├── meta: { toolName, args, timestamp, turnIndex, sessionId }
  └── span index: 行/字节偏移 -> 便于 paged recall
```

存储放本地文件（`.pi/obs-archive/` 或独立目录），handle 通过 `tool_result` 的 `details` 持久化进 session JSONL。

### L1 Memory Card

```text
MemoryCard {
  id
  kind: fact | error | conclusion | file_read | test_result | compiler_output | architecture
  summary: string            // 蒸馏后的短文本
  entities: { files[], symbols[], errorCodes[] }
  source: obs://<id>:L<start>-L<end>   // source-bound evidence（因子 A）
  validity: {
    state: valid | stale | resolved | unknown   // 因子 B
    boundTo: file(path)@hash
    lastCheckedTurn
  }
  importance: number         // 用于 L0 逐出决策
  createdTurn
}
```

### 检索索引

lexical（BM25/ripgrep）+ embedding + entity 倒排（file/symbol）+ 时间关系。第一版可只做 lexical + embedding，entity 索引作为增量。

---

## 6. 因子 B：有效性 / 失效机制（headline）

这是唯一 coding-agent 独有、普通 RAG 没有的点，是论文核心。

失效来源与规则（第一版）：

```text
read foo.py -> 卡片 C 记录 file(foo.py)@hash=abc
edit/write foo.py -> hash 变 def
  -> 扫描所有 boundTo=file(foo.py) 的卡片
  -> state: valid -> stale
```

检索排序不再是单纯 `similarity(query, card)`，而是 utility：

```text
Score(m, q) =
    α · Semantic(m, q)
  + β · Task(m, q)          // 与当前 subtask/goal 的关联
  + γ · Importance(m)
  + δ · Freshness(m)        // validity 派生
  + ε · Evidence(m)         // source 是否可回溯
  - λ · TokenCost(m)
```

stale 卡片强降权（δ 生效）。若模型仍需要，走 obs_recall 回原文重新确认，而不是直接信旧卡片。

不同 observation 的默认生命周期先给经验值，后续可学：

```text
test failure        -> 中等，修复相关文件后转 resolved
source-code read    -> 文件被 edit 后立即 stale
compiler error      -> 依赖修复后 resolved
architecture 结论    -> 长寿命，默认 valid
```

---

## 7. 因子 A：检索与注入

- 检索时机：`context` hook，每个 turn 前。
- 输入：当前 goal / 最近 user 意图 / 最近若干 turn 作为 query。
- 输出：top-k 卡片，按 Score 排序，拼成一段结构化 context 注入。
- source-bound：每张卡片带 `obs://` 指针，模型可 obs_recall 回原文，避免"卡片说了但不敢信"。

对标 SoL-Pi ObservationPack：它是确定性 head/tail 投影（前 2048 字节 + 后 1536 字节），中间信息模型看不到就不会 recall。因子 A 用语义检索定位中间的关键行，补上这个盲区。

---

## 8. 因子 C：多级结构与逐出

- L0 Hot：最近 observation 原文驻留（沿用 pi 默认最近窗口思路）。
- 逐出：`session_before_compact` 触发时，把要逐出的 turn 蒸馏成 L1 卡片（而非整体 summary），原文进 L2。
- L2：不可变原文，只能通过 obs_recall 精确回取。

与默认 compaction 的差别：默认是"summary 替换整段历史"，信息有损且不可回溯；这里逐出后仍有 L1 卡片可检索、L2 原文可回取。

---

## 9. Baseline ladder

```text
B0  Pi vanilla（无任何 memory 干预）
B1  Pi + 默认截断
B2  Pi + 默认 summarization compaction
B3  Pi + vector RAG over trajectory（无 validity）   ← 因子 B 的对照
B4  Pi + SoL-Pi ObservationPack                      ← 因子 A 的对照
B5  Pi + SoL-Pi EPR
Ours-full  A+B+C 全开
  ablation: Ours\A, Ours\B, Ours\C                   ← 逐因子消融
```

B3 会在 stale 指标上明显吃亏，这是因子 B 说服力的直接来源。

---

## 10. 指标

标准指标（pi evals 已原生输出，见 `packages/evals/src/pi-harness.ts` 的 usage）：

- Task success rate
- Total tokens / Input tokens
- Est. cost (USD)
- Model turns / latency

Memory 专属指标（baseline 刷不出来，需自建打点）：

- **Stale-memory retrieval rate**：检索结果中 state=stale 的占比
- **Wrong-memory-induced failures**：可归因于过期记忆的失败任务数
- Rehydration rate：obs_recall 触发频率
- Retrieval precision / Evidence recall

---

## 11. Eval 计划（Both）

- 快速迭代：pi 自带 evals。`evalHarnessTable({ baseline, candidate })` + `--repetitions 5` 直接产出 pass rate / tokens / latency / cost 的 lift 报告（`packages/evals/README.md`）。
  - 缺口：现有任务偏短，显不出 memory 价值。需新写长程任务：强迫多次回看旧 observation、中途 edit 使旧 read 失效的场景。
- Headline 表：SWE-bench（或 SWE-bench Verified 子集）。这块要新接，接入点是 `createPiCodingAgentHarness`（`packages/evals/src/pi-harness.ts:291`），它已按 task 起隔离 AgentSession 并记录 token/cost/tool trace。自定义 `output` + judge 判 patch 是否通过测试。

---

## 12. 仓库结构与开源策略

不 fork pi，做成独立 package，peerDependency 指向 pi。这与 SoL-Pi 自身做法一致，也保证论文 attribution 干净（同一 Pi / model / prompt / tools / benchmark，只换 memory policy）。

```text
observation-memory/
├── src/
│   ├── archive/        # L2 内容寻址存储
│   ├── memory/         # L1 卡片蒸馏
│   ├── index/          # lexical + embedding + entity
│   ├── retrieval/      # 因子 A：Score 排序 + 注入
│   ├── validity/       # 因子 B：hash 失效 + 生命周期
│   ├── rehydration/    # obs_recall 工具
│   ├── compaction/     # 因子 C：逐出为卡片
│   └── extension.ts    # 组装成一个 pi extension
├── eval/
│   ├── pi-evals/       # 长程任务（复用 pi evals harness）
│   ├── swebench/       # SWE-bench 接线
│   └── metrics/        # stale rate 等自建指标
├── baselines/
│   ├── vanilla/
│   ├── vector-rag/
│   └── sol-pi/         # ObservationPack / EPR 作为 baseline
└── package.json        # peerDependency: @earendil-works/pi-*
```

License：pi 是 MIT，本项目也用 MIT，方便别人 fork/extend，利于拿星。

---

## 13. 工作分解与里程碑

- M1 闭环：extension skeleton 跑通 tool_result 归档 + context 注入 + obs_recall。在 pi 交互模式手测能回取原文。
- M2 因子 B：文件 hash 失效 + validity 打分 + stale 降权。加 stale-retrieval 打点。
- M3 因子 A：Score 排序 + task-aware query。
- M4 因子 C：session_before_compact 逐出为卡片。
- M5 Eval：pi evals 长程任务 + SWE-bench 子集接线 + baseline ladder。
- M6 消融 + 写作：跑 A/B/C ablation，出对比表。

建议顺序：M1 -> M2 是最短的"能证明 headline claim"路径；A/C 可并行补。

---

## 14. 风险与规避

- 风险：full multi-level 工程量大，attribution 变糊。
  规避：系统全建，但论文只把因子 B（validity）当唯一新颖 claim，A/C 用 ablation 证明各自边际贡献。即便 reviewer 觉得多级结构不新，validity 仍站得住。
- 风险：SWE-bench 接线和跑分成本高。
  规避：先用 pi evals 长程任务做全部快速迭代和 ablation，SWE-bench 只用于最终 headline 表，跑 Verified 子集控成本。
- 风险：validity 的失效规则太 heuristic，被质疑。
  规避：把 hash-based 失效作为 sound 的下界（文件变了一定重新确认），生命周期经验值作为可调参数并做敏感性分析。
- 风险：obs_recall 依赖模型主动调用，可能不调。
  规避：因子 A 的注入本身带 source 指针作为提示；必要时在 stale 卡片旁显式标注"内容可能过期，需 recall 确认"。

---

## 附：关键代码锚点速查

- 扩展 API 与全部事件/结果类型：`packages/coding-agent/src/core/extensions/types.ts`
- 事件分发与 context 对象：`packages/coding-agent/src/core/extensions/runner.ts`
- tool hook 接线 / compaction 驱动 / 上下文用量：`packages/coding-agent/src/core/agent-session.ts`
- compaction 核心：`packages/coding-agent/src/core/compaction/compaction.ts`
- provider/context hook 接线：`packages/coding-agent/src/core/sdk.ts`
- 事件流程图与 hook 列表：`packages/coding-agent/docs/extensions.md`
- 自定义 compaction 文档：`packages/coding-agent/docs/compaction.md`
- 完整示例：`packages/coding-agent/examples/extensions/{custom-compaction,truncated-tool,dynamic-tools,tools}.ts`
- Eval harness：`packages/evals/src/pi-harness.ts`、`packages/evals/src/vitest-evals/{summary,reporter,harness-table}.ts`
</content>
</invoke>
