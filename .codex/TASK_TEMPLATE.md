# TASK TEMPLATE

用于在本仓库中向 Codex 提交任务。建议每次新任务复制后填写。

```text
【任务标题】
一句话描述任务。

【任务目标】
明确本次要达到的结果。

【修改范围】
- 允许修改：
- 禁止修改：

【输入信息】
- 相关目录/文件：
- 参考脚本/文档：
- 依赖与环境约束：

【实现约束】
- 是否需要兼容旧接口：
- 是否允许新增目录或文件：
- 命名规范要求：

【验收标准】
1. 
2. 
3. 

【验证要求】
- 需要执行的命令：
- 关键输出期望：

【发布要求】
- 仅修改（不提交） / 提交不推送 / push code
```

## 快速示例

```text
【任务标题】
统一 mixed integer 示例到 ModelSolver 抽象

【任务目标】
将 src/mix_integer_programming 下脚本统一为 build_model + run_example_model 入口

【修改范围】
- 允许修改：src/mix_integer_programming, src/ModelSolver.py, 对应 README
- 禁止修改：其他项目目录

【验收标准】
1. 每个脚本都包含 problem_type
2. README 包含目标函数与约束公式
3. py_compile 和至少 1 个脚本运行通过

【发布要求】
提交不推送
```
