# RUNBOOK

本文件汇总本仓库中 Codex 常用执行与验证命令。

## 1. 建立上下文

```powershell
rg --files src
rg -n "OptimizationModel\(|problem_type|run_example_model" src
Get-ChildItem src -Directory
```

## 2. 语法检查

```powershell
$env:UV_CACHE_DIR='.uv-cache'; uv run python -m py_compile src\ModelSolver.py
$env:UV_CACHE_DIR='.uv-cache'; uv run python -m py_compile src\linear_programming\product_mix_problem.py
```

可按任务范围替换为对应脚本。

## 3. 运行验证

```powershell
$env:UV_CACHE_DIR='.uv-cache'; uv run python src\linear_programming\product_mix_problem.py
$env:UV_CACHE_DIR='.uv-cache'; uv run python src\mix_integer_programming\capital_budgeting_problem.py
$env:UV_CACHE_DIR='.uv-cache'; uv run python src\nonlinear_programming\bounded_surface_optimization_problem.py
```

## 4. 变更审阅

```powershell
git status --short
git diff -- src\ModelSolver.py
git diff --stat
```

## 5. 提交与推送

```powershell
git add -A
git commit -m "<clear summary>"
```

仅当用户明确要求 `push code` 时执行：

```powershell
git push -u origin main
```

## 6. 常见问题

- 终端显示中文乱码：先用 Python 按 UTF-8 读取文件确认真实内容，不以终端显示作为唯一依据。
- 参考后端枚举报边界错误：检查是否错误使用了 `ub`，应区分真实边界 `lb/ub` 与搜索边界 `search_lb/search_ub`。
