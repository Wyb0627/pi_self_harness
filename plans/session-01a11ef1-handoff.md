# Resume Handoff: Dynamic Evaluation Sampling Research

## Read This First

This is a replacement for the failed Codex session `01a11ef1-2206-7112-a225-39150e60c738`. Do not resume, fork, or continue that thread. Read this handoff before inspecting the detailed archive. The full visible archive is `plans/session-01a11ef1-full-archive.md`; open only a specific needed section, never ingest it wholesale.

## Current Task

Continue the research/design work for a dynamic evaluation sampler that decides per-evolution test subsets and affects rollback decisions for the DGM-style coding-agent evolution project in this repository.

## User Decisions Already Made

- Match DGM's evolution scope: evolve the coding-agent harness, including its prompts, tools, utilities, and workflow rather than only task patches.
- Retain DGM's fixed 200-task evaluation set as the final/global audit anchor.
- Investigate a locally deployed Qwen 0.6B embedding model versus grep/keyword matching for retrieval; do not silently substitute a fallback if the requested embedding route is unavailable.
- Before implementation, verify that the existing codebase and engineering architecture can support the proposed design. Then write the design document and provide a directly copyable implementation prompt for a new Codex session.

## Immediate Resume Point

The prior session was checking whether the current codebase supports the agreed dynamic-evaluation design and was expected to produce the design document plus a concrete implementation prompt. Re-establish the repository state yourself, then continue from that point. Preserve the distinction between local mutation-impact/rollback evaluation and the fixed 200-task global audit score.

## Failure Context

- Failed thread: `01a11ef1-2206-7112-a225-39150e60c738`
- Follow-on thread: `01a11fd1-a9d6-7491-9a75-92f9914a2932`
- Error: `stream disconnected before completion: idle timeout waiting for SSE`
- The prior context grew to approximately 349k input tokens. Keep new requests compact and read archive material selectively.

## Runtime Context Limit

- The replacement session must start after Codex Desktop reloads its configuration.
- The current configured window is 640k tokens, with automatic compaction triggered at 544k tokens (85% of the window).
- Do not load the full archive as one request. The compaction trigger is a guardrail, not a strict cap for one oversized tool result or user message.

## Latest User Messages

### 2026-10-09T07:56:35.949Z

继续任务

### 2026-10-09T08:07:47.821Z

继续任务

### 2026-10-09T08:39:01.983Z

继续任务

### 2026-10-09T08:40:27.114Z

1. 对于进化范围，dgm是如何规定的？我觉得我们可以和他保持一致
2. 我们仍然采用 DGM 固定的 200 题
3. 我们可以本地部署一个qwen3-0.6b embedding模型（我记得本地有mlx，运行指令即可部署），或者直接使用grep关键词匹配呢？类似早起claude code这样？在我们场景下会靠谱吗？

该方案在你创建完文档后，我会去交由codex实现。你给我一个直接可以复制给他的启动prompt。


## Last Assistant Message

### 2026-10-09T06:58:47.616Z

DGM 的范围我已经核对清楚：它不是只进化 prompt，而是允许修改 coding-agent 自身代码，包括主循环、工具、utils、依赖和自测；但 archive、parent selection、benchmark evaluator 等外层进化控制逻辑保持固定。若我们严格对齐，就应采用相同边界：**候选 Pi agent 代码仓可变，动态采样器、配对执行器、回退裁决器和 grader 不可变**，且候选 agent 整个进程必须在容器内运行。

关于检索，我倾向于本地 embedding + lexical hybrid，而不是纯 grep。接下来我会核实 Qwen3-Embedding-0.6B 的官方用法和本机 MLX 环境，再据此冻结设计并落盘。

## Evidence and Archive

- Full visible transcript and retained tool results: `plans/session-01a11ef1-full-archive.md`
- Original Codex rollout source files and checksums: see the archive manifest.
- Relevant project inputs mentioned in the session: `paper_ref/DGM.pdf` and `research_output/clm_budgeted_evolution_20260924_125503/`.
