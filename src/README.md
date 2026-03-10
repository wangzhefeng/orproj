# 多求解器时代的工程设计

基于公众号文章《多求解器时代的工程设计 Gurobi, CPLEX, SCIP 统一调用方案》的整理稿。

- 来源：[mp.weixin.qq.com/s/9z1TfR0XB58CCRAf-ccPxw](https://mp.weixin.qq.com/s/9z1TfR0XB58CCRAf-ccPxw)
- 作者：王源
- 发布时间：2026-02-27 12:04

## 文章主题

文章讨论的是运筹优化工程里一个很现实的问题：

- 数学模型通常是通用的
- 但不同求解器的 API 差异很大
- 如果业务代码里直接写死某个 solver，后续切换、对比和扩展都会很痛苦

典型反模式如下：

```python
if solver_name == "gurobi":
    # Gurobi API 建模 + 求解
elif solver_name == "cplex":
    # CPLEX API 建模 + 求解
elif solver_name == "scip":
    # SCIP API 建模 + 求解
```

短期这样写能工作，但长期会带来几个典型痛点：

1. 业务代码和求解器 API 强耦合，维护成本高。
2. 切换求解器代价高，不利于做 solver A/B 对比。
3. 新增求解器时，`if-else` 会越来越长。
4. 测试困难，尤其不利于 mock infeasible、time-limit 等状态。

文章给出的核心方案是：用“策略模式（Strategy）+ 工厂模式（Factory）”抽象求解器行为，构建可插拔、可维护、可扩展的统一求解器调用层。

## 1. 策略模式 + 工厂模式简介

### 策略模式

策略模式的核心思想是：把一组可互换的算法或行为封装成独立对象，并通过统一接口对外提供能力。

放到求解器场景里：

- `GurobiStrategy` 封装 Gurobi 的 API 细节
- `CplexStrategy` 封装 CPLEX 的 API 细节
- `ScipStrategy` 封装 SCIP 的 API 细节

这些类都实现同一个接口：

```python
solve(model, config) -> result
```

这样业务层只调用统一的 `solve()`，而不需要感知底层到底是哪家求解器。

### 工厂模式

工厂模式的核心思想是：把对象创建逻辑集中管理，调用方不直接实例化具体类，而是通过工厂获取对象。

放到求解器场景里：

- 输入 `gurobi`，工厂返回 `GurobiStrategy`
- 输入 `cplex`，工厂返回 `CplexStrategy`
- 输入 `scip`，工厂返回 `ScipStrategy`

业务层不再需要自己写大量 `if-else` 来决定创建哪个求解器对象。

### 两种模式组合后的分工

- 策略模式负责“怎么做”
- 工厂模式负责“创建谁来做”

两者组合后，形成了一个清晰架构：不同求解器的差异交给策略类封装，策略对象的选择与创建交给工厂类统一管理。

## 2. 用策略模式抽象不同求解器行为

文章先强调了一点：第一步不是直接写某个 solver 的 API 调用，而是先定义一层和具体求解器无关的统一抽象。

### 2.1 定义通用数据结构

文中给出的抽象包括：

- `Variable`
- `Constraint`
- `Objective`
- `OptimizationModel`
- `SolverConfig`
- `SolveResult`

这些对象的作用是把业务层和求解器层隔开：

- 业务层只依赖统一模型、统一配置、统一结果
- 求解器层负责把统一抽象翻译成具体 solver API

文章特别强调，这一步是整个设计能否长期维护的关键。

### 2.2 定义统一策略接口

在统一抽象之上，再定义统一策略接口 `SolverStrategy`：

```python
class SolverStrategy(ABC):
    @abstractmethod
    def solve(self, model: OptimizationModel, config: SolverConfig) -> SolveResult:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass
```

这意味着不管底层是 Gurobi、CPLEX 还是 SCIP，对外都必须提供一致的 `solve(model, config)` 能力，并返回统一的 `SolveResult`。

### 2.3 把求解器差异封装到各自策略类中

文中的三个具体策略类是：

- `GurobiStrategy`
- `CplexStrategy`
- `ScipStrategy`

文章强调，这里的重点不是类名，而是职责划分。每个策略类都要负责：

- 把通用模型翻译成对应求解器的 API 调用
- 把统一配置映射成对应求解器参数
- 执行求解
- 读取底层状态与解
- 最终映射成统一的 `SolveResult`

也就是说，变化点应当集中在策略类内部，而不是散落在业务层代码里。这样业务层才能真正做到“面向接口编程”。

## 3. 用工厂模式创建不同的求解器对象

有了多个策略类之后，还需要解决“根据配置创建哪个策略对象”的问题。

文章指出：业务层当然可以自己写 `if-else`，但这样会让创建逻辑散落在各处。工厂模式的意义，就是把这部分逻辑集中收敛。

示意代码如下：

```python
class SolverFactory:
    _registry = {
        "gurobi": GurobiStrategy,
        "cplex": CplexStrategy,
        "scip": ScipStrategy,
    }

    @classmethod
    def create(cls, solver_name: str) -> SolverStrategy:
        key = solver_name.strip().lower()
        if key not in cls._registry:
            raise ValueError(f"Unsupported solver: {solver_name}")
        return cls._registry[key]()
```

这样业务层只需要：

```python
strategy = SolverFactory.create("gurobi")
```

工厂模式带来的直接收益是：

- 求解器创建入口统一
- 可用 solver 一目了然
- 新增 solver 时，只需新增策略类并注册到工厂
- 不需要修改每一处涉及求解器选择的业务代码

## 4. 完整调用代码实例展示

文章最后给了一个完整示例，展示业务层如何真正做到“切换求解器不改业务逻辑”。

调用链是：

1. 构造统一模型 `OptimizationModel`
2. 构造统一配置 `SolverConfig`
3. 用 `SolverFactory.create()` 选择具体策略
4. 把策略注入 `SolverEngine`
5. 通过 `engine.solve(model, config)` 获取统一结果

关键点是这里只改一行就可以切换求解器：

```python
solver_name = "gurobi"  # 改成 "cplex" 或 "scip"
strategy = SolverFactory.create(solver_name)
```

文章反复强调，这个示例最想表达的不是“算出什么数值结果”，而是：

- 业务层构造模型的代码不变
- 业务层读取结果的代码不变
- 只通过工厂切换策略对象，就能切换底层求解器

这就是“策略模式 + 工厂模式”在多求解器调用场景里的核心价值。

## 5. 总结

文章总结是：对于运筹优化工程，真正难的往往不只是“把模型写出来”，也不是“设计高效的算法”，而是如何把建模、求解和工程维护这三件事长期协调好。

“策略模式 + 工厂模式”本身并不复杂，但用在“通用求解器调用层”上，可以很好地把：

- 稳定的业务建模逻辑
- 多变的求解器实现细节

清晰地分开。这是一个很值得在团队里推广的工程实践。

## 对应代码

根据文章代码整理后的脚本在这里：

- [ModelSolver.py](/Users/wangzf/projects/orproj/src/ModelSolver.py)

这个脚本保留了文章示例的核心结构：

- 通用模型抽象
- 策略接口
- 三个 solver 策略实现
- 工厂创建逻辑
- `SolverEngine` 统一入口
- 一个可直接运行的 toy model 示例


## 目录补充

- `nonlinear_programming`：用于存放非线性规划问题，例如包含分式目标或其他非线性约束的模型。
