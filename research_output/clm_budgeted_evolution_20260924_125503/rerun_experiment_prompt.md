# 实验重跑任务：DGM-200 三臂对比（同仓库约束 + held-out 干净评测）

## 0. 任务目标

在冻结的 DGM-200 清单（200 道 SWE-bench Verified 任务）上重跑三个 arm，产出可直接 head-to-head 对比的 accuracy / token / 时间数据。核心改进点：**进化过程限定在同一 GitHub 仓库内**，且 **held-out 测试集不参与任何进化/反馈**。

## 1. 三个 Arm 的定义与协议

### Arm P1：原版 Pi one-shot（不进化基线）

- 固定的 Pi harness，不做任何 mutation / 进化 / 反馈修复。
- 对每道题独立跑一次，提交一次 patch，官方评测器打一次分。
- **不接收任何官方评测反馈**。
- 用途：严格可比的 one-shot 基线。

### Arm DGM：DGM-style 进化（archive + parent selection，无回退）

- 仅在 **D_evolve = 60 题**（small 10 + medium 50）上进化：
  - 产生 mutation 候选 → 在 D_evolve 上评测 → 按分数选 parent → 写入 archive。
  - archive 只增不删，按分数重选 parent。
  - **不使用 RF-CLM 回退**。
- 进化结束后，取 archive 中 best checkpoint，在 **D_test = 140 题**（big stage）上做 **一次 one-shot 评测**。
- **D_test 的 140 题在进化全程对 agent 完全隐藏**，不参与任何 mutation / parent selection / 回退决策。
- 最终分数 = best checkpoint 在 D_test 上的 one-shot solve rate。

### Arm P2：RF-CLM 动态回退进化（同仓库约束）

- 进化机制同 DGM-style，但加入 **RF-CLM 动态回退**：
  - 进化失败时，用 repair-first causal-slice 定位最小充分移除集，回退到最早移除点之前并重放后续有效改动。
- **同仓库硬约束**：每次 mutation 的 adaptive 采样（selector）只能从与该改动**同一 GitHub 仓库**的任务中选量尺任务。跨仓库提议由仲裁器 fail-closed 拒绝。
  - 已实现：`rollback_mvp/adaptive_eval/selector_agent.py` 的 `_parse_proposals` 和 `_arbitrate` 均校验 `task.repo == change.repo`。
- 同样仅在 D_evolve (60 题) 上进化，D_test (140 题) held-out 只做最终 one-shot 评测。
- 最终分数 = best checkpoint 在 D_test 上的 one-shot solve rate。

## 2. 关键协议红线（不可违反）

1. **D_test 140 题在进化阶段对所有 arm 完全不可见**。selector、parent selection、rollback diagnosis 均不得读取 D_test 的任何信息（pass/fail、test patch、gold patch、评测日志）。
2. **P1 不接收任何反馈**。P1 的 agent 进程不得收到官方评测器的 pass/fail 信号。
3. **DGM 和 P2 的反馈仅限 D_evolve**。最终 D_test 评测是纯 one-shot，不得在 D_test 上做 feedback-repair。
4. **同仓库约束**：P2 的 adaptive selector 只能选与 `change.repo` 相同仓库的任务。代码已硬编码 fail-closed，不要绕过。
5. **三个 arm 使用相同的模型、token 预算、时间预算、系统 prompt、工具集、容器镜像**。唯一差异是进化策略（无进化 / DGM-style / DGM-style + RF-CLM）。
6. **至少 3 个进化种子**（DGM 和 P2），用 paired hierarchical bootstrap 做显著性检验。

## 3. 冻结清单与任务划分

- Manifest: `research_output/clm_budgeted_evolution_20260924_125503/dgm_swebench_verified_200.v1.json`
- sha256: `3fb913fbc73a05c1f7cae3b708c976374632820b58377aab5de08b742f96c967`
- 仓库分布：
  - django/django: 153 题（small 10, medium 25, big 118）
  - sphinx-doc/sphinx: 25 题（medium 25）
  - astropy/astropy: 22 题（big 22）
- D_evolve = small(10) + medium(50) = 60 题
- D_test = big(140) = 140 题

## 4. 运行命令

### 4.1 P1（原版 Pi one-shot）

```bash
python3 rollback_mvp/orchestrate_endpoint_200.py run \
  --manifest research_output/clm_budgeted_evolution_20260924_125503/dgm_swebench_verified_200.v1.json \
  --output research_output/rerun_<date>/p1 \
  --protocol original_only \
  --global-token-cap 80000000 \
  --global-wall-seconds 108000 \
  --max-task-tokens 512000 \
  --agent-timeout-seconds 3600 \
  --execute --confirm-paid-run
```

### 4.2 DGM-style 进化

```bash
python3 rollback_mvp/run_dgm_pi_evolution.py search \
  --run-id dgm-rerun-<seed> \
  --output research_output/rerun_<date>/dgm_seed<seed> \
  --manifest research_output/clm_budgeted_evolution_20260924_125503/dgm_swebench_verified_200.v1.json \
  --seed <seed> \
  --proposal-slots 80 \
  --proposals-per-wave 2
```

进化完成后，取 best checkpoint 在 D_test 上 one-shot 评测：

```bash
python3 rollback_mvp/orchestrate_endpoint_200.py run \
  --manifest <evolve_manifest_path> \
  --output research_output/rerun_<date>/dgm_seed<seed>/test \
  --protocol original_only \
  --execute --confirm-paid-run
```

### 4.3 P2（RF-CLM + 同仓库约束）

同 DGM 的进化命令，但启用 RF-CLM rollback 模块。adaptive selector 的同仓库约束已在代码中硬编码，无需额外 flag。

```bash
python3 rollback_mvp/run_dgm_pi_evolution.py search \
  --run-id rfclm-rerun-<seed> \
  --output research_output/rerun_<date>/p2_seed<seed> \
  --manifest research_output/clm_budgeted_evolution_20260924_125503/dgm_swebench_verified_200.v1.json \
  --seed <seed> \
  --proposal-slots 80 \
  --proposals-per-wave 2 \
  --enable-rf-clm
```

同样在 D_test 上 one-shot 评测。

## 5. 必须收集的指标（每个 arm × 每个 seed）

### 在 D_test (140 题 held-out) 上：

| 指标 | 说明 |
|---|---|
| resolved / total | 解出数 / 140 |
| solve rate | 百分比 + Wilson 95% CI |
| reported tokens | input + output + cache-read + cache-write |
| 直接执行时间 | agent 时间 + 官方评测器时间（秒） |
| 进化成本（仅 DGM/P2） | 进化阶段总 tokens、总 wall-clock、probe 调用次数 |

### 配对比较（P2 vs DGM，P2 vs P1，DGM vs P1）：

- paired task difference
- paired bootstrap 95% CI（10000 resamples）
- McNemar exact p-value
- P2-only solves / DGM-only solves / P1-only solves

## 6. 输出结构

```
research_output/rerun_<date>/
├── p1/
│   └── summary.json          # P1 在 200 题上的 one-shot 结果
├── dgm_seed1/
│   ├── evolve/               # 进化轨迹、archive、checkpoints
│   └── test/summary.json     # best checkpoint 在 D_test 上的结果
├── dgm_seed2/ ...
├── dgm_seed3/ ...
├── p2_seed1/ ...
├── p2_seed2/ ...
├── p2_seed3/ ...
└── comparison.md             # 三臂 head-to-head 对比表 + 统计检验
```

## 7. 注意事项

- 之前的 P2 69.5% 结果**不可用于本次对比**——那次在 D_test 上做了 feedback-repair，违反了 held-out 协议。本次必须重跑。
- P1 之前的 50.0% (100/200) 结果可复用作为 P1 基线（因为它本来就是 one-shot，协议一致），但建议重跑以保证同环境同模型。
- 同仓库约束的代码改动已在 `rollback_mvp/adaptive_eval/` 中（`CandidateChangeCard.repo` 字段 + `_parse_proposals` / `_arbitrate` 的 fail-closed 校验）。运行前确认 `python3 -m unittest rollback_mvp.adaptive_eval.test_selector rollback_mvp.adaptive_eval.test_controller` 通过。
- 进化预算：参考之前 DGM 论文的 ~$22k / 2 周，但本次用相同模型和预算上限，做公平对比。

## 8. 完成标准

- [ ] P1 在 200 题上 one-shot 完成，产出 summary.json
- [ ] DGM 3 个 seed 完成进化 + D_test one-shot 评测
- [ ] P2 3 个 seed 完成进化（RF-CLM + 同仓库约束）+ D_test one-shot 评测
- [ ] 产出 comparison.md，包含三臂在 D_test 上的 accuracy / tokens / 时间对比表 + 配对统计检验
- [ ] 所有 held-out 140 题在进化阶段未被访问（可通过日志审计验证）
