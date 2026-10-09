# 迁移说明（2026-10-09）

本仓库已提交可复现研究所需要的代码、文档、冻结清单与运行证据。下列体积大或
与机器绑定的数据不在 Git 中，换电脑时需要单独拷贝或重建。

## 已提交

- `rollback_mvp/`：离线回滚实验、DGM200 编排与评测脚本、单元测试。
- `pi-rollback/`：rollback 插件源码与实验记录。
- `research_output/`：预注册、报告、探索日志、冻结的 200 任务清单与校验和；
  `dgm200_run/` 中已完成的 trajectory、预测、官方评测结果与汇总。
- `draft_18f0c29c_folder/`、`paper_ref/`：论文草稿素材与 DGM 论文。

`dgm200_run` 目前仍在继续运行与写入，汇总仍为 `complete: false`。Git 中保存的是
提交时点（2026-10-09 15:31 左右）的工作快照；之后的 trace 与结果需要再次提交。
该快照不包含：

- `tasks/*/workspace/` 与 `invalid_attempts/*/workspace/` 的完整任务仓库；
  对应补丁、轨迹与评测结果已提交；
- `build_wheelhouse/` 中本机构建的 arm64 wheels；
- 全局忽略的 `*.log`；评测输出摘要仍保留在 `test_output.txt`、`report.json`
  与 `evaluation.json`。

## 需要手动迁移

| 路径 | 大小 | 处理方式 |
| --- | --- | --- |
| `DGM_results/` | 6.9 GB | 必须拷贝。离线 replay 需要 `swe_results/swe_dgm`；zip/tar 与同名解压目录预计重复，确认后可只留一种。 |
| `datasets/SWE-bench/` | 80 MB | 可按 `dgm200_run/run_config.json` 记录的 revision 从官方仓库重新克隆。 |
| 根目录与 `pi-rollback/` 的 `node_modules/` | 791 MB | 在新机执行 `npm install --ignore-scripts` 重建。 |
| `dgm200_run/build_wheelhouse/` | 42 MB | 可选；仅新机同为 macOS arm64 且需要复用 astropy wheels 时拷贝。 |
| `dgm200_run/**/*.log` | 14 MB | 可选；全局 `*.log` 已忽略，如需要完整 debug 证据请单独拷贝。 |
| Docker 任务镜像 | GB 级 | 不在 Git；在新机重建，或用 `docker save` / `docker load` 迁移。 |
| `llm_api_samples/` | 40 KB | 当前被忽略；如仍需要这些调用样例，单独拷贝。 |

## 新机恢复

1. `git clone` 本仓库；确认分支与提交号。
2. 在仓库根目录和 `pi-rollback/` 分别执行 `npm install --ignore-scripts`。
3. 按 `rollback_mvp/README.md` 安装 Python 依赖。运行 LLM 或评测路径前设置
   `ROLLBACK_LLM_API_KEY`、`ROLLBACK_ENDPOINT_API_KEY`，不要把 key 写入仓库；
   `pi_home/*/auth.json` 是运行态文件，pi 会在缺失时自动创建空文件。
4. 把 `DGM_results/` 放回仓库根目录，并把 SWE-bench 克隆到
   `datasets/SWE-bench/`。
5. 数据 revision 与实验协议以 `dgm200_preregistration.md` 和
   `dgm200_run/run_config.json` 为准。
