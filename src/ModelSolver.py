from __future__ import annotations

import itertools
import math
import os
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

ROOT = str(Path.cwd())
if ROOT not in sys.path:
    sys.path.append(ROOT)

os.environ.setdefault("LOG_NAME", "model_solver")

from utils.log_util import logger


EPSILON = 1e-9


# =========================
# 通用抽象（不依赖具体求解器）
# =========================
@dataclass
class Variable:
    name: str
    lb: float = 0.0
    ub: float = float("inf")
    vtype: str = "C"  # C: continuous, I: integer, B: binary
    step: Optional[float] = None
    description: str = ""
    # search_lb/search_ub 仅供参考后端枚举候选解使用，不属于数学模型本身的硬约束。
    search_lb: Optional[float] = None
    search_ub: Optional[float] = None


@dataclass
class Constraint:
    name: str
    expr: Dict[str, float]  # 线性表达式: dict[var_name] = coeff
    sense: str  # "<=", "==", ">="
    rhs: float
    description: str = ""


@dataclass
class Objective:
    name: str
    sense: str  # "min" / "max"
    expr: Dict[str, float] = field(default_factory=dict)
    quadratic_expr: Dict[Tuple[str, str], float] = field(default_factory=dict)
    # nonlinear_expr 用于承接 SciPy 这类通用非线性目标，输入为变量名到取值的映射。
    nonlinear_expr: Optional[Callable[[Dict[str, float]], float]] = None
    constant: float = 0.0
    weight: float = 1.0
    description: str = ""


@dataclass
class OptimizationModel:
    name: str
    # problem_type 用于标记模型类别，例如 LP、IP、MIP、MOIP、QP、MIQP、NLP。
    # 当前参考后端不会依据该字段切换算法，但会保留该语义供业务层和后续真实求解器适配使用。
    problem_type: str = ""
    variables: List[Variable] = field(default_factory=list)
    constraints: List[Constraint] = field(default_factory=list)
    objective: Optional[Objective] = None
    objectives: List[Objective] = field(default_factory=list)
    description: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_variable(self, variable: Variable) -> None:
        self.variables.append(variable)

    def add_constraint(self, constraint: Constraint) -> None:
        self.constraints.append(constraint)

    def add_objective(self, objective: Objective) -> None:
        self.objectives.append(objective)
        if self.objective is None:
            self.objective = objective

    def active_objectives(self) -> List[Objective]:
        # 多目标模型优先返回 objectives；单目标模型兼容旧字段 objective。
        if self.objectives:
            return self.objectives
        return [self.objective] if self.objective else []


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
    objective_breakdown: Dict[str, float] = field(default_factory=dict)


@dataclass
class FileSolveRequest:
    path: str
    expect_infeasibility_analysis: bool = True
    description: str = ""


@dataclass
class ModelDiagnostic:
    status: str
    summary: str
    conflicting_constraints: List[str] = field(default_factory=list)
    suggested_actions: List[str] = field(default_factory=list)


@dataclass
class BackendProfile:
    key: str
    display_name: str
    family: str
    supports_file_model: bool = False
    supports_diagnostics: bool = False
    notes: str = ""


# =========================
# 后端注册表
# =========================
# 这里统一维护“后端名称 -> 后端能力”的映射。
# 当前实现仍然通过参考后端执行，但会保留原始脚本所属库的语义标签。
BACKEND_PROFILES: Dict[str, BackendProfile] = {
    "reference": BackendProfile("reference", "Reference", "enumeration", True, True, "Built-in teaching backend."),
    "gurobi": BackendProfile("gurobi", "GUROBI", "commercial_lp_mip", True, True, "Gurobi-style workflow placeholder."),
    "docplex": BackendProfile("docplex", "DOCPLEX", "commercial_lp_mip", True, False, "Docplex/CPLEX style workflow placeholder."),
    "cplex": BackendProfile("cplex", "CPLEX", "commercial_lp_mip", True, True, "CPLEX backend alias."),
    "ortools": BackendProfile("ortools", "ORTOOLS", "open_source_lp_mip", False, False, "OR-Tools style workflow placeholder."),
    "pyomo": BackendProfile("pyomo", "PYOMO", "modeling_layer", True, False, "Pyomo modeling-layer workflow placeholder."),
    "scipy": BackendProfile("scipy", "SCIPY", "numeric_optimization", False, False, "SciPy optimization workflow placeholder."),
    "scip": BackendProfile("scip", "SCIP", "open_source_lp_mip", True, True, "SCIP backend alias."),
}


# =========================
# 策略模式：统一接口
# =========================
class SolverStrategy(ABC):
    @abstractmethod
    def solve(self, model: OptimizationModel, config: SolverConfig) -> SolveResult:
        raise NotImplementedError

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError


# =========================
# 具体策略：参考求解后端
# =========================
# 当前项目还没有真实绑定 gurobi/docplex/ortools/pyomo/scipy 的原生 API，
# 因此这里使用一个“参考求解器”统一承载演示与校验逻辑：
# 1. 二维连续线性模型：优先做顶点枚举；
# 2. 其他模型：使用有限候选集枚举；
# 3. 输出结果中仍保留原始后端语义名称。
class ReferenceSolverStrategy(SolverStrategy):
    def __init__(self, profile: BackendProfile) -> None:
        self.profile = profile

    @property
    def name(self) -> str:
        return self.profile.display_name

    def solve(self, model: OptimizationModel, config: SolverConfig) -> SolveResult:
        logger.info("[%s] solving model %s (type=%s)", self.name, model.name, model.problem_type or "UNSPECIFIED")
        objectives = model.active_objectives()
        if not objectives:
            raise ValueError("Model objective is not defined.")

        best_point: Optional[Dict[str, float]] = None
        best_value: Optional[float] = None
        best_breakdown: Dict[str, float] = {}

        for candidate in self._candidate_points(model):
            if not self._is_feasible(model, candidate):
                continue
            aggregate_value, breakdown = self._evaluate_objectives(model, candidate)
            if best_value is None or aggregate_value < best_value - EPSILON:
                best_point = candidate
                best_value = aggregate_value
                best_breakdown = breakdown

        if best_point is None:
            return SolveResult(
                status="INFEASIBLE",
                message=f"No feasible candidate found by {self.name} backend.",
                solver_name=self.name,
            )

        primary_name = objectives[0].name
        return SolveResult(
            status="OPTIMAL",
            objective_value=best_breakdown.get(primary_name, best_value),
            variable_values={k: round(v, 6) for k, v in best_point.items()},
            message=f"Solved by {self.name} backend over the shared abstraction.",
            solver_name=self.name,
            objective_breakdown={k: round(v, 6) for k, v in best_breakdown.items()},
        )

    def _candidate_points(self, model: OptimizationModel) -> Iterable[Dict[str, float]]:
        if self._can_use_vertex_enumeration(model):
            yield from self._vertex_candidates(model)
            return
        yield from self._enumeration_candidates(model)

    def _can_use_vertex_enumeration(self, model: OptimizationModel) -> bool:
        objectives = model.active_objectives()
        if len(objectives) != 1 or len(model.variables) != 2:
            return False
        if any(variable.vtype != "C" for variable in model.variables):
            return False
        return not objectives[0].quadratic_expr and objectives[0].nonlinear_expr is None

    def _vertex_candidates(self, model: OptimizationModel) -> Iterable[Dict[str, float]]:
        x_var, y_var = model.variables
        boundaries = []
        for constraint in model.constraints:
            boundaries.append((constraint.expr.get(x_var.name, 0.0), constraint.expr.get(y_var.name, 0.0), constraint.rhs))
        if not math.isinf(x_var.lb):
            boundaries.append((1.0, 0.0, x_var.lb))
        if not math.isinf(x_var.ub):
            boundaries.append((1.0, 0.0, x_var.ub))
        if not math.isinf(y_var.lb):
            boundaries.append((0.0, 1.0, y_var.lb))
        if not math.isinf(y_var.ub):
            boundaries.append((0.0, 1.0, y_var.ub))

        seen = set()
        for first_index in range(len(boundaries)):
            for second_index in range(first_index + 1, len(boundaries)):
                point = self._solve_two_by_two(
                    boundaries[first_index],
                    boundaries[second_index],
                    x_var.name,
                    y_var.name,
                )
                if point is None:
                    continue
                key = tuple(round(point[name], 8) for name in (x_var.name, y_var.name))
                if key in seen:
                    continue
                seen.add(key)
                yield point

    def _solve_two_by_two(
        self,
        row_a: Tuple[float, float, float],
        row_b: Tuple[float, float, float],
        x_name: str,
        y_name: str,
    ) -> Optional[Dict[str, float]]:
        a1, b1, c1 = row_a
        a2, b2, c2 = row_b
        determinant = a1 * b2 - a2 * b1
        if abs(determinant) <= EPSILON:
            return None
        return {
            x_name: (c1 * b2 - c2 * b1) / determinant,
            y_name: (a1 * c2 - a2 * c1) / determinant,
        }

    def _enumeration_candidates(self, model: OptimizationModel) -> Iterable[Dict[str, float]]:
        variable_domains = [(variable.name, self._build_domain(variable)) for variable in model.variables]
        names = [item[0] for item in variable_domains]
        domains = [item[1] for item in variable_domains]
        for values in itertools.product(*domains):
            yield {name: float(value) for name, value in zip(names, values)}

    def _build_domain(self, variable: Variable) -> List[float]:
        # 如果模型本身没有有限上界，则允许单独配置 search_ub 作为参考后端的搜索范围。
        lower = variable.search_lb if variable.search_lb is not None else variable.lb
        upper = variable.search_ub if variable.search_ub is not None else variable.ub
        if math.isinf(lower) or math.isinf(upper):
            raise ValueError(f"Variable {variable.name} requires finite search bounds for reference solving.")
        if variable.vtype == "B":
            return [0.0, 1.0]
        step = variable.step if variable.step is not None else (1.0 if variable.vtype == "I" else 0.5)
        count = int(round((upper - lower) / step))
        values = [lower + step * index for index in range(count + 1)]
        if values[-1] < upper - EPSILON:
            values.append(upper)
        return [round(value, 10) for value in values]

    def _is_feasible(self, model: OptimizationModel, candidate: Dict[str, float]) -> bool:
        for variable in model.variables:
            value = candidate[variable.name]
            if value < variable.lb - EPSILON or value > variable.ub + EPSILON:
                return False
            if variable.vtype in {"I", "B"} and abs(value - round(value)) > EPSILON:
                return False
        for constraint in model.constraints:
            lhs = sum(coef * candidate[name] for name, coef in constraint.expr.items())
            if constraint.sense == "<=" and lhs > constraint.rhs + EPSILON:
                return False
            if constraint.sense == ">=" and lhs < constraint.rhs - EPSILON:
                return False
            if constraint.sense == "==" and abs(lhs - constraint.rhs) > EPSILON:
                return False
        return True

    def _evaluate_objectives(self, model: OptimizationModel, candidate: Dict[str, float]) -> Tuple[float, Dict[str, float]]:
        breakdown: Dict[str, float] = {}
        aggregate_value = 0.0
        for objective in model.active_objectives():
            objective_value = self._evaluate_objective(objective, candidate)
            breakdown[objective.name] = objective_value
            signed_value = objective_value if objective.sense == "min" else -objective_value
            aggregate_value += objective.weight * signed_value
        return aggregate_value, breakdown

    def _evaluate_objective(self, objective: Objective, candidate: Dict[str, float]) -> float:
        total = objective.constant
        total += sum(coef * candidate[name] for name, coef in objective.expr.items())
        for (left_name, right_name), coef in objective.quadratic_expr.items():
            total += coef * candidate[left_name] * candidate[right_name]
        if objective.nonlinear_expr is not None:
            total += objective.nonlinear_expr(candidate)
        return total


# =========================
# 工厂模式：根据配置创建策略
# =========================
class SolverFactory:
    @classmethod
    def profile(cls, solver_name: str) -> BackendProfile:
        key = solver_name.strip().lower()
        if key not in BACKEND_PROFILES:
            raise ValueError(f"Unsupported solver: {solver_name}")
        return BACKEND_PROFILES[key]

    @classmethod
    def create(cls, solver_name: str) -> SolverStrategy:
        return ReferenceSolverStrategy(cls.profile(solver_name))


# =========================
# 统一入口：业务层调用
# =========================
class SolverEngine:
    def __init__(self, strategy: SolverStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: SolverStrategy) -> None:
        self.strategy = strategy

    def solve(self, model: OptimizationModel, config: SolverConfig) -> SolveResult:
        logger.info("[Engine] use solver = %s, problem_type = %s", self.strategy.name, model.problem_type or "UNSPECIFIED")
        result = self.strategy.solve(model, config)
        logger.info("[Engine] status = %s, objective = %s", result.status, result.objective_value)
        return result

    def diagnose(self, model: OptimizationModel, result: SolveResult) -> ModelDiagnostic:
        if result.status != "INFEASIBLE":
            return ModelDiagnostic(status=result.status, summary="Model solved without infeasibility.")

        conflicting_constraints: List[str] = []
        for first_index in range(len(model.constraints)):
            for second_index in range(first_index + 1, len(model.constraints)):
                first = model.constraints[first_index]
                second = model.constraints[second_index]
                # 当前只做最基础的显式矛盾检查：同一左侧表达式同时出现 >= 和 <= 且右侧冲突。
                if first.expr == second.expr:
                    if first.sense == ">=" and second.sense == "<=" and first.rhs > second.rhs + EPSILON:
                        conflicting_constraints.extend([first.name, second.name])
                    if first.sense == "<=" and second.sense == ">=" and second.rhs > first.rhs + EPSILON:
                        conflicting_constraints.extend([first.name, second.name])

        conflicting_constraints = sorted(set(conflicting_constraints))
        summary = "Detected infeasibility but no minimal conflict could be isolated."
        if conflicting_constraints:
            summary = f"Potentially conflicting constraints: {', '.join(conflicting_constraints)}."
        return ModelDiagnostic(
            status="INFEASIBLE",
            summary=summary,
            conflicting_constraints=conflicting_constraints,
            suggested_actions=[
                "Check contradictory upper/lower bounds.",
                "Check duplicated constraints with inconsistent right-hand sides.",
                "Relax one tight constraint and re-solve.",
            ],
        )

    def solve_with_diagnostics(self, model: OptimizationModel, config: SolverConfig) -> Tuple[SolveResult, ModelDiagnostic]:
        result = self.solve(model, config)
        return result, self.diagnose(model, result)


def format_result(result: SolveResult) -> str:
    lines = [f"solver: {result.solver_name}", f"status: {result.status}", f"objective: {result.objective_value}"]
    if result.objective_breakdown:
        lines.append(f"objectives: {result.objective_breakdown}")
    lines.append(f"variables: {result.variable_values}")
    if result.message:
        lines.append(f"message: {result.message}")
    return "\n".join(lines)


def format_diagnostic(diagnostic: ModelDiagnostic) -> str:
    lines = [f"diagnostic_status: {diagnostic.status}", f"summary: {diagnostic.summary}"]
    if diagnostic.conflicting_constraints:
        lines.append(f"conflicts: {diagnostic.conflicting_constraints}")
    if diagnostic.suggested_actions:
        lines.append(f"actions: {diagnostic.suggested_actions}")
    return "\n".join(lines)


# =========================
# 文件模型工作流
# =========================
# 用于承接原始 gurobi/cplex/scip 这类“读取 LP/MPS 文件并求解”的脚本语义。
def solve_model_file(
    request: FileSolveRequest,
    solver_name: str = "gurobi",
    config: Optional[SolverConfig] = None,
) -> ModelDiagnostic:
    path = Path(request.path)
    profile = SolverFactory.profile(solver_name)
    if not path.exists():
        return ModelDiagnostic(
            status="FILE_NOT_FOUND",
            summary=f"Model file not found: {path}",
            suggested_actions=["Check the file path.", "Export the LP/MPS model before solving."],
        )
    return ModelDiagnostic(
        status="NOT_IMPLEMENTED",
        summary=f"{profile.display_name} file-model workflow placeholder for {path.name}.",
        suggested_actions=[
            f"Bind {profile.display_name} file loading into a concrete backend adapter.",
            "Run backend presolve and optimize.",
            "If infeasible, export IIS/conflict information through the backend API.",
        ],
    )


# =========================
# 示例运行入口
# =========================
def run_example_model(
    build_model: Callable[[], OptimizationModel],
    solver_name: str,
    config: Optional[SolverConfig] = None,
    diagnostics: bool = False,
) -> None:
    config = config or SolverConfig()
    engine = SolverEngine(SolverFactory.create(solver_name))
    model = build_model()
    if diagnostics:
        result, diagnostic = engine.solve_with_diagnostics(model, config)
        print(format_result(result))
        print(format_diagnostic(diagnostic))
        return
    result = engine.solve(model, config)
    print(format_result(result))


# =========================
# 示例
# =========================
def build_toy_model() -> OptimizationModel:
    model = OptimizationModel(name="toy_mip", problem_type="MIP", description="Small mixed-integer planning model.")
    model.add_variable(Variable("x", lb=0, vtype="I", search_ub=6))
    model.add_variable(Variable("y", lb=0, vtype="I", search_ub=6))

    # x + 2y <= 14
    model.add_constraint(Constraint(name="c1", expr={"x": 1, "y": 2}, sense="<=", rhs=14))

    # 3x - y >= 0
    model.add_constraint(Constraint(name="c2", expr={"x": 3, "y": -1}, sense=">=", rhs=0))

    # max 5x + 4y
    model.add_objective(Objective(name="profit", sense="max", expr={"x": 5, "y": 4}))
    return model


if __name__ == "__main__":
    run_example_model(build_toy_model, solver_name="reference")
