from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from utils.log_util import logger


# =========================
# 通用抽象（不依赖具体求解器）
# =========================
@dataclass
class Variable:
    name: str
    lb: float = 0.0
    ub: float = float("inf")
    vtype: str = "C"  # C: continuous, I: integer, B: binary


@dataclass
class Constraint:
    name: str
    expr: Dict[str, float]  # 线性表达式: dict[var_name] = coeff
    sense: str  # "<=", "==", ">="
    rhs: float


@dataclass
class Objective:
    sense: str  # "min" / "max"
    expr: Dict[str, float]
    constant: float = 0.0


@dataclass
class OptimizationModel:
    name: str
    variables: List[Variable] = field(default_factory=list)
    constraints: List[Constraint] = field(default_factory=list)
    objective: Optional[Objective] = None


@dataclass
class SolverConfig:
    time_limit_sec: float = 60.0
    mip_gap: float = 1e-4
    threads: int = 1
    output_log: bool = True
    backend_params: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SolveResult:
    status: str
    objective_value: Optional[float] = None
    variable_values: Dict[str, float] = field(default_factory=dict)
    message: str = ""
    solver_name: str = ""


# =========================
# 策略模式：统一接口
# =========================
class SolverStrategy(ABC):
    @abstractmethod
    def solve(self, model: OptimizationModel, config: SolverConfig) -> SolveResult:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass


# =========================
# 具体策略：不同求解器实现
# =========================
class GurobiStrategy(SolverStrategy):
    @property
    def name(self) -> str:
        return "Gurobi"

    def solve(self, model: OptimizationModel, config: SolverConfig) -> SolveResult:
        # 真实实现中通常会在这里完成：
        # 1. 创建 Gurobi env/model
        # 2. 映射 time_limit、mip_gap、threads 等参数
        # 3. 添加变量、约束和目标函数
        # 4. 调用 optimize()
        # 5. 把底层结果映射为统一的 SolveResult
        logger.info(f"[{self.name}] build model: {model.name}")
        logger.info(f"[{self.name}] set params: \ntime_limit={config.time_limit_sec}, gap={config.mip_gap}")

        return SolveResult(
            status="OPTIMAL",
            objective_value=123.45,
            variable_values={"x": 2, "y": 6},
            message="Solved by Gurobi (demo)",
            solver_name=self.name,
        )


class CplexStrategy(SolverStrategy):
    @property
    def name(self) -> str:
        return "CPLEX"

    def solve(self, model: OptimizationModel, config: SolverConfig) -> SolveResult:
        # 这里的职责与 GurobiStrategy 相同，只是底层 API 和参数映射不同。
        logger.info(f"[{self.name}] build model: {model.name}")
        logger.info(f"[{self.name}] set params: threads={config.threads}")

        return SolveResult(
            status="OPTIMAL",
            objective_value=124.00,
            variable_values={"x": 2, "y": 6},
            message="Solved by CPLEX (demo)",
            solver_name=self.name,
        )


class ScipStrategy(SolverStrategy):
    @property
    def name(self) -> str:
        return "SCIP"

    def solve(self, model: OptimizationModel, config: SolverConfig) -> SolveResult:
        # 这里演示 backend_params 之类的 solver 特有参数透传能力。
        logger.info(f"[{self.name}] build model: {model.name}")
        logger.info(f"[{self.name}] backend params: {config.backend_params}")

        return SolveResult(
            status="FEASIBLE",
            objective_value=126.80,
            variable_values={"x": 1, "y": 7},
            message="Solved by SCIP (demo)",
            solver_name=self.name,
        )


# =========================
# 工厂模式：根据配置创建策略
# =========================
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


# =========================
# 统一入口：业务层调用
# =========================
class SolverEngine:
    def __init__(self, strategy: SolverStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: SolverStrategy) -> None:
        self.strategy = strategy

    def solve(self, model: OptimizationModel, config: SolverConfig) -> SolveResult:
        # 文中的统一入口可继续承载校验、日志、耗时统计和异常包装。
        logger.info(f"[Engine] use solver = {self.strategy.name}")
        result = self.strategy.solve(model, config)
        logger.info(f"[Engine] status = {result.status}, obj = {result.objective_value}")
        return result


def build_toy_model() -> OptimizationModel:
    model = OptimizationModel(name="toy_mip")

    model.variables.extend(
        [
            Variable("x", lb=0, ub=100, vtype="I"),
            Variable("y", lb=0, ub=100, vtype="I"),
        ]
    )

    # x + 2y <= 14
    model.constraints.append(
        Constraint(name="c1", expr={"x": 1, "y": 2}, sense="<=", rhs=14)
    )

    # 3x - y >= 0
    model.constraints.append(
        Constraint(name="c2", expr={"x": 3, "y": -1}, sense=">=", rhs=0)
    )

    # max 5x + 4y
    model.objective = Objective(sense="max", expr={"x": 5, "y": 4})

    return model




if __name__ == "__main__":
    model = build_toy_model()

    config = SolverConfig(
        time_limit_sec=30,
        mip_gap=1e-4,
        threads=4,
        output_log=True,
        backend_params={"scip/separating/maxrounds": 5},
    )

    # 关键点：只改这里就能切换求解器
    solver_name = "gurobi"  # 改成 "cplex" 或 "scip"
    strategy = SolverFactory.create(solver_name)

    engine = SolverEngine(strategy)
    result = engine.solve(model, config)

    logger.info("\n=== Final Result ===")
    logger.info("solver :", result.solver_name)
    logger.info("status :", result.status)
    logger.info("objective :", result.objective_value)
    logger.info("vars :", result.variable_values)
