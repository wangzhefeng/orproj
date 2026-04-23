# CLAUDE.md

本文件为 Claude Code 专属补充配置。**主规范为 [AGENTS.md](AGENTS.md)**，冲突时以 AGENTS.md 为准。

## 任务启动时必读文件

复杂任务前，至少读：

- `README.md` — 项目整体概览
- `AGENTS.md` — 完整工作约定与编码规范
- `src/ModelSolver.py` — 统一模型接口（改任何模型前必读）
- 对应子目录的 `README.md`（如 `src/linear_programming/README.md`）

## 项目结构速查

```
src/
├── ModelSolver.py                  # 统一模型接口（核心抽象）
├── linear_programming/             # LP
├── integer_programming/            # IP
├── mix_integer_programming/        # MIP / MILP / MIQP / MINLP
├── quadratic_programming/          # QP
├── nonlinear_programming/          # NLP
├── multi_objective_optimizaion/    # 多目标规划
├── dynamic_programming/            # 动态规划
├── path_planning/                  # 路径规划
├── heuristic_algorithms/           # 进化/启发式算法
└── todo/                           # 待实现
.codex/
├── TASK_TEMPLATE.md                # 任务需求模板
├── REVIEW_CHECKLIST.md             # 交付自检清单
└── RUNBOOK.md                      # 常用执行命令
```

## 验证命令（改完主动运行）

```bash
# 语法检查
python -m py_compile <file.py>

# 运行单个优化脚本
python src/<module>/<script>.py

# 批量语法检查
find src -name "*.py" | xargs python -m py_compile
```

## 优化模型关键约定

- 所有模型通过 `OptimizationModel` 描述，统一走 `src/ModelSolver.py` 接口
- `problem_type` 必须标注：`LP` / `IP` / `MIP` / `QP` / `MIQP` / `NLP` / `MOIP`
- 变量边界：`lb/ub` 是数学约束，`search_lb/search_ub` 仅供搜索参考，不得混用

## Claude Code 特定行为

- 无用户明确要求时，不提交、不推送、不开 PR
- 大改动前先 Plan Mode 给方案，确认后再动手
- 删文件、改目录结构、修改公共接口前必须停下来问用户
