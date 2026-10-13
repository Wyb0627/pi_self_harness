# 交接文档 / Onboarding (RF-CLM Evolution-Rollback 研究)

> 目的：在个人 macOS 机器上 `git clone` 本仓库后，让人或 agent 读完本文件即可与公司电脑上的进度**完全对齐**，并能继续开发、复现实验、推进论文。
>
> 最后更新：2026-10-13。对齐提交：见 `git log -1`（交接时的 HEAD）。

---

## 0. ⚠️ 必读：先处理两件事

### 0.1 公司 API 密钥已泄露到公开 git 历史（安全）

本仓库 (`Wyb0627/pi_self_harness`) 是 **public**。以下已推送到 `origin/main` 的历史提交内嵌了公司 aicolate/tiktok-row 网关的明文 `secret_id`/`secret_key`：

- `222280c07` → `rollback_mvp/config.py` 旧版本（硬编码 key）
- `86c546fe7` → `rollback_mvp/__pycache__/config.cpython-313.pyc`（key 编译进字节码）

当前 HEAD 的 [config.py](rollback_mvp/config.py) 已改为纯环境变量读取、无密钥。但历史仍公开可见。

**行动项（仓库外，必须人工完成）：**
1. **立即到网关控制台吊销/轮换**这两组泄露的 `secret_id`/`secret_key`。这是唯一彻底止血手段。
2. 如需清除历史：用 `git filter-repo` 或 GitHub 的敏感数据移除流程重写并 force-push，再让所有协作者重新 clone。本仓库**从不**自动 force-push 或改写公开历史。
3. 本地 `llm_api_samples/`（被 gitignore）也含明文 key，**不要**提交。调用模式见 §5.3 的脱敏示例。

### 0.2 两份大数据不在 git 里，还机前必须手动迁移

| 路径 | 大小 | 为什么重要 | 怎么办 |
| --- | --- | --- | --- |
| `DGM_results/` | 6.9 GB | 所有**离线 replay 实验**的唯一数据源（DGM 释放的真实进化树 + 每任务分数） | 还机前**拷到个人存储**；或从 DGM 开源项目重新获取（§4.1） |
| `datasets/SWE-bench/` | 80 MB | SWE-bench 评测代码与冻结 revision | 可从源头按 pin 的 revision 重拉（§4.2），非必须拷贝 |

另见 [MIGRATION.md](MIGRATION.md)（更细的迁移清单）。

---

## 1. 项目一句话

现有 harness 自进化把进化史当成"只增 archive + 按分数重选 parent"，**回退是缺失的一等操作**。本研究把进化谱系建成可回放的 patch lineage，用"软诊断 + 主动反事实 replay"直接定位**一最小充分移除集**，回退到最早致因 patch 之前再重放独立增益。最终算法是 **Repair-First CLM (RF-CLM)**。定位：pi harness 上不 fork core 的研究 extension，支撑一篇技术报告 + 开源仓库。

完整方向、与 DGM/MARS/Safe-Harness 的对照、防审稿人论证、可证伪 claim、实验设计，全部在 [EVOLUTION_ROLLBACK_DIRECTION.md](EVOLUTION_ROLLBACK_DIRECTION.md)。**这是研究的权威文档，先读它。**

---

## 2. 当前进度快照

### 2.1 已完成

- **DGM-200 基准（主结果）**：200/200 任务跑完。
  - P1（原版 Pi 单次提交）：**100/200 = 50.0%**，70.725M reported tokens，直接执行 8.75h。
  - P2（Pi + RF-CLM 一轮官方反馈恢复）：**139/200 = 69.5%**，76.639M tokens，累计直接执行 13.57h。
  - 配对增益 +39 任务 / +19.5pp，bootstrap 95% CI [+14.0, +25.0]pp，无 P1→P2 回归。
  - **纪律约束**：P2 用了隐藏官方评测反馈，是**恢复上界**，不是标准单提交 SWE-bench 分数，**不得**直接宣称优于 DGM 50%。
  - 结果与审计：[dgm200_performance_comparison.md](research_output/clm_budgeted_evolution_20260924_125503/dgm200_performance_comparison.md)、[summary.json](research_output/clm_budgeted_evolution_20260924_125503/dgm200_run/summary.json)、[预注册](research_output/clm_budgeted_evolution_20260924_125503/dgm200_preregistration.md)。
- **离线 replay 实验链（E1–E11）**：在 DGM 释放树上验证回退决策质量；RF-CLM 在合成 conjunctive/alternative/mixed 失败族上相对旧 failure-first 省 42.86%–49.89% probes，所有配对 bootstrap CI 严格大于 0。详见 [rollback_mvp/README.md](rollback_mvp/README.md) 与方向文档 §4.2。
- **pi 插件原型** [pi-rollback/](pi-rollback/)：证据门控回退，`/rollback checkpoint|diagnose|status|apply`，`apply` 默认 dry-run。
- **自适应评测采样设计** [AGENTIC_ADAPTIVE_EVALUATION_DESIGN.md](AGENTIC_ADAPTIVE_EVALUATION_DESIGN.md) + [rollback_mvp/adaptive_eval/](rollback_mvp/adaptive_eval/)（契约 + fake runtime 已测，真实容器执行待接）。

### 2.2 已撤回 / 已否决（别重走）

- 旧的 "4/11 分叉分歧" 统计（混用了 10/60/200 不同任务子集的 raw accuracy）→ 修正到共同任务集后严格分歧只剩 1/11，只能当个案。
- 静态 LLM 前瞻回退预测（v1/v2 prompt）：无可复现优势，且延迟从 ~2min 涨到 ~42min。**不要**再无界调 prompt。
- E9 branch quarantine、E10 multi-fidelity promotion：均未同时满足 95% recall / 20% saving，已否决。
- CLM monotone-boundary pilot 的成本 kill criterion 已触发（probes 比线性扫描贵），所以未扩三次重复。

### 2.3 待推进

- 真实分布 main result：同模型、同预算下跑**完整进化回路**比较 Ours vs B0–B3（需 Docker + 网关）。离线数据缺 counterfactual children，无法替代。
- 因子 C（回退后再进化）：离线不可验证，需真跑。
- 容器执行后端 [container_runner.py](rollback_mvp/adaptive_eval/container_runner.py) 接真实 Docker（当前 Colima socket 不可用，`DockerCliRuntime` 故意拒绝执行直到配额/代理账本/隔离满足）。
- 论文：草稿素材在 [draft_18f0c29c_folder/](draft_18f0c29c_folder/)，参考文献 [paper_ref/](paper_ref/)。

---

## 3. 环境搭建

机器基线（公司机实测，供对齐）：Node `v26.5.0`（engines 要求 `>=22.19.0`）、npm `11.17.0`、Python `3.13.14`。

```bash
# 1) clone
git clone https://github.com/Wyb0627/pi_self_harness.git
cd pi_self_harness

# 2) Node 依赖（根仓库 + pi 插件，均用 --ignore-scripts，见 AGENTS.md 供应链约束）
npm install --ignore-scripts
( cd pi-rollback && npm install --ignore-scripts )

# 3) Python（研究代码主要用标准库；LLM 路径需要 openai SDK）
python3 -m pip install openai            # rollback_mvp 的 LLM decider 必需
python3 -m pip install swebench          # 仅 build_local_swebench_images.py 构建评测镜像时需要

# 4) Docker/Colima（仅跑 SWE-bench 真实评测/镜像构建时需要；纯离线实验不需要）
```

`rollback_mvp/` 的实验代码除 `openai`（LLM 路径）与 `swebench`（镜像构建路径）外**只用 Python 标准库**（`statistics`/`hashlib`/`concurrent` 等），不需要 numpy/scipy，因此**无 GPU、无重型依赖**也能跑绝大部分实验。

---

## 4. 数据集下载与预处理（准备阶段详细做法）

### 4.1 DGM 释放结果（离线 replay 的核心数据，6.9 GB）

**用途**：E1–E11 全部离线实验、`rollback_mvp/` 里除 DGM200 外的所有 benchmark，都从这里读 DGM 的真实进化树和每任务分数——**零 Docker、零重跑**。

**来源**：DGM 开源项目 `github.com/jennyzzt/dgm`（论文 arXiv:2505.22954，Sakana AI）。实验用的是其 SWE 结果包 `swe_results.zip`。

**期望布局**（代码按此硬路径查找，见 [config.py](rollback_mvp/config.py) `DGM_SWE_ROOT`）：

```
DGM_results/
├── swe_results.zip              # 原始包 (~1.0 GB)
└── swe_results/
    ├── swe_dgm/                 # ← 主数据：完整进化树，每节点含
    │                            #   parent_commit / entry / self_evo.md /
    │                            #   model_patch.diff / predictions/*.md /
    │                            #   overall_performance
    ├── swe_dgm_nodarwin/
    └── swe_dgm_noselfimprove/
```

**预处理**：解压 `swe_results.zip` 到 `DGM_results/swe_results/`，确认 `DGM_results/swe_results/swe_dgm/` 存在即可，无需其它转换。

> **强烈建议**：这 6.9 GB 还机前直接拷到个人存储（整个 `DGM_results/` 目录），比从公开渠道重新下载/解压省事且可保证字节一致。

### 4.2 SWE-bench Verified（DGM-200 冻结清单的来源）

研究**不**自造数据集。200 题取自 DGM 用过的 SWE-bench Verified 子集，并用 pin 的 revision 冻结成清单。

**固定版本（写死，复现必须一致）：**
- SWE-bench 仓库 git revision：`dc4c087c2b9e4cefebf2e3d201d27e362d899e0f`
- HF 数据集 `princeton-nlp/SWE-bench_Verified` revision：`c104f840cc67f8b6eec6f759ebc8b2693d585d4a`
- DGM source commit：`682eb38a3eb232f4396924cacd0a083bf1444cf8`

```bash
# 评测代码（可选，仅真实评测/镜像构建需要）
git clone https://github.com/princeton-nlp/SWE-bench.git datasets/SWE-bench
git -C datasets/SWE-bench checkout dc4c087c2b9e4cefebf2e3d201d27e362d899e0f
```

**冻结清单本身已在 git 里**，无需重新生成：
- [dgm_swebench_verified_200.v1.json](research_output/clm_budgeted_evolution_20260924_125503/dgm_swebench_verified_200.v1.json)
- SHA-256 `3fb913fbc73a05c1f7cae3b708c976374632820b58377aab5de08b742f96c967`
- 有序 ID 列表 SHA-256 `421c950302366954005dab020cdc89ca0d6ae1f0423e2b662637f7790a31d0d7`
- 分区：`small=10`、`medium=50`、`big=140`，互不相交。

**重新冻结（仅当需要重建）**：`python3 rollback_mvp/freeze_dgm200_manifest.py`（会从 HF datasets-server 按上面 revision 拉取，并校验 revision 一致）。

**校验清单完整性**：

```bash
cd rollback_mvp
python3 -m adaptive_eval.cli validate-catalogue
# 期望输出 status: valid；会校验 manifest sha / 有序 ID sha / 每行 hash / 153-25-22 分布
```

### 4.3 Astropy/Sphinx 离线 wheelhouse（可选，仅 arm64 复现 DGM200 构建）

`research_output/.../dgm200_run/build_wheelhouse/` 是本机构建的离线 wheels（修复 Sphinx 4.1/4.2/4.3 的依赖冲突，见 [exploration_log.md](research_output/clm_budgeted_evolution_20260924_125503/exploration_log.md) E15/E16）。仅当你在 macOS arm64 上重跑 DGM200 的受影响任务时才需要；每个 wheel 都有 SHA-256 manifest 校验。个人机如非 arm64 可忽略。

---

## 5. 密钥与环境变量

### 5.1 契约

| 环境变量 | 用途 | 必需性 |
| --- | --- | --- |
| `ROLLBACK_LLM_API_KEY` | `rollback_mvp` LLM decider（deepseek-v4-flash）鉴权 | 跑任何 `--llm` 实验必需 |
| `ROLLBACK_LLM_MODEL` | 默认 `byteplus/deepseek-v4-flash-ga` | 可选，覆盖模型 |
| `ROLLBACK_LLM_BASE_URL` | 默认 aicolate 网关 | 可选，换 endpoint |
| `ROLLBACK_ENDPOINT_API_KEY` | DGM200 orchestrator / endpoint runner 鉴权 | 跑 DGM200 真实评测必需 |

**绝不**把 key 写进仓库。`research_output/**/pi_home/*/auth.json` 是运行态文件，缺失时 pi 会自动建空文件。

### 5.2 ⚠️ 离职后 deepseek-v4-flash 网关不可用

当前所有 LLM 实验走的是**公司内部免费** aicolate 网关。离职/还机后你个人机上**没有**这个网关的有效 key。继续跑 `--llm` 实验前，需把上面两个 key 换成你个人可用的 OpenAI 兼容 endpoint（设置 `ROLLBACK_LLM_BASE_URL` + `ROLLBACK_LLM_MODEL` + key）。**所有 `--offline` 实验不需要任何 key，可直接跑。**

### 5.3 调用模式（脱敏，替代不上传的 llm_api_samples/）

OpenAI 兼容 chat completions（设置好 env 后）：

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["ROLLBACK_LLM_API_KEY"],
    base_url=os.environ.get("ROLLBACK_LLM_BASE_URL",
                            "https://<your-openai-compatible-endpoint>/v1"),
)
resp = client.chat.completions.create(
    model=os.environ.get("ROLLBACK_LLM_MODEL", "byteplus/deepseek-v4-flash-ga"),
    messages=[{"role": "user", "content": "ping"}],
    max_tokens=4096,
)
print(resp.choices[0].message.content)
```

研究代码已封装在 [rollback_mvp/llm_client.py](rollback_mvp/llm_client.py)（`LLMClient.complete_json` / `complete_json_with_telemetry`，带重试与 token 遥测），直接用它即可。

---

## 6. 如何复现 / 运行

### 6.1 纯离线实验（无需 key、无需 Docker、无需 GPU）—— 先跑这些对齐

```bash
cd rollback_mvp

# 回退决策器 baseline（greedy/random vs 子树最优 oracle）
python3 run.py --offline

# 受控延迟缺陷 baseline
python3 run_controlled.py --offline

# 修正后的 DGM CLM endpoint/recovery 基准（0 = 全部 episode，不调 LLM）
python3 dgm_clm_benchmark.py --max-episodes 0 --output outputs/dgm_clm_benchmark_offline.json

# Repair-First CLM 合成族基准（纯合成，无 API）
python3 run_repair_first.py
```

把输出和 git 里已提交的 `rollback_mvp/outputs/*.json(l)` 对比，一致即对齐。

### 6.2 LLM 实验（需 §5 的 key）

```bash
cd rollback_mvp
export ROLLBACK_LLM_API_KEY=...        # 个人可用的 OpenAI 兼容 key

python3 run_controlled.py --llm-repeats 5          # 受控诊断，5 票多数
python3 dgm_clm_benchmark.py --llm --max-episodes 12 --llm-repeats 3   # DeepSeek pilot
python3 run.py                                     # 带 LLM decider 的回退选择
```

### 6.3 DGM-200 全量基准（需 Docker + 网关 + 大预算）

入口 [orchestrate_endpoint_200.py](rollback_mvp/orchestrate_endpoint_200.py)。协议：`original_and_feedback`；每任务上限 512k tokens / 3600s；全局 80M tokens / 108000s；任务间 90s 节流。参数见 [run_config.json](research_output/clm_budgeted_evolution_20260924_125503/dgm200_run/run_config.json)。付费执行需命令行显式确认值。**这一步已完成（200/200），除非重跑否则不需要再动。**

### 6.4 pi 插件

```bash
cd pi-rollback
npm test            # node --test
npm run check       # biome + tsc --noEmit
```

---

## 7. 关键文档地图

| 文件 | 内容 |
| --- | --- |
| [EVOLUTION_ROLLBACK_DIRECTION.md](EVOLUTION_ROLLBACK_DIRECTION.md) | **研究权威文档**：方向、related work、问题定义、方法、实验设计、风险、形式化 |
| [METHODS.md](METHODS.md) | 各组件方法摘要 + 关键代码指针 |
| [AGENTIC_ADAPTIVE_EVALUATION_DESIGN.md](AGENTIC_ADAPTIVE_EVALUATION_DESIGN.md) | 自适应评测采样完整契约 |
| [DYNAMIC_SAMPLING_60_140_EXPERIMENT_PROTOCOL.md](DYNAMIC_SAMPLING_60_140_EXPERIMENT_PROTOCOL.md) | 60/140 动态采样协议 |
| [rollback_mvp/README.md](rollback_mvp/README.md) | 离线实验代码说明 + 历史结果表 |
| [research_output/clm_budgeted_evolution_20260924_125503/](research_output/clm_budgeted_evolution_20260924_125503/) | DGM200 预注册、结果、审计、探索日志、冻结清单 |
| [plans/](plans/) | 动态采样方案的设计决策史与完整 session 归档 |
| [MIGRATION.md](MIGRATION.md) | 换机迁移清单 |
| [SELF_EVOLUTION_ANALYSIS.md](SELF_EVOLUTION_ANALYSIS.md) / [OBSERVATION_MEMORY_DESIGN.md](OBSERVATION_MEMORY_DESIGN.md) | 早期设想（仅参考，方向已收窄） |

---

## 8. 对齐检查清单（clone 后按序执行）

1. `git log -1` 确认 HEAD 与交接提交一致。
2. `npm install --ignore-scripts`（根 + `pi-rollback/`）。
3. `python3 -m pip install openai`。
4. 放回 `DGM_results/`（6.9G），确认 `DGM_results/swe_results/swe_dgm/` 存在。
5. `cd rollback_mvp && python3 -m adaptive_eval.cli validate-catalogue` → `status: valid`。
6. 跑 §6.1 的四个 `--offline` 实验，与 `rollback_mvp/outputs/` 已提交结果对比。
7. `cd pi-rollback && npm test` 通过。
8. 读 [EVOLUTION_ROLLBACK_DIRECTION.md](EVOLUTION_ROLLBACK_DIRECTION.md) + [dgm200_performance_comparison.md](research_output/clm_budgeted_evolution_20260924_125503/dgm200_performance_comparison.md) 建立全局认知。

全部通过即与公司电脑进度对齐。
