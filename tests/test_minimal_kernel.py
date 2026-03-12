# tests/test_minimal_kernel.py
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pysi.core.kernel.minimal_kernel import DemandEvent, Lot, PlanningKernel


def _sample_inputs():
    lots = [Lot("lot-1", "P1", "factory_A", "market_TYO", 70.0, "202601")]
    demands = [DemandEvent("d-1", "market_TYO", "P1", "202601", 100.0)]
    return lots, demands


def test_flow_simulation_determinism():
    lots, demands = _sample_inputs()
    kernel = PlanningKernel()
    r1 = kernel.run(lots, demands, max_iterations=2)
    r2 = kernel.run(lots, demands, max_iterations=2)
    assert r1["final_evaluation"] == r2["final_evaluation"]
    assert r1["flow_events"] == r2["flow_events"]


def test_state_derivation_backlog_and_supply():
    lots, demands = _sample_inputs()
    kernel = PlanningKernel()
    result = kernel.run(lots, demands, max_iterations=1)
    state = result["final_state"]
    key = ("market_TYO", "P1", "202601")
    assert state.supply_by_node_product_time[key] == 70.0
    assert state.backlog_by_market_product_time[key] == 30.0


def test_trust_event_detection_occurs_on_backlog():
    lots, demands = _sample_inputs()
    kernel = PlanningKernel()
    result = kernel.run(lots, demands, max_iterations=1)
    trust_events = result["final_trust_events"]
    assert len(trust_events) == 1
    assert trust_events[0].event_type == "E_STOCKOUT_RISK"


def test_resolver_operator_application_reduces_backlog():
    lots, demands = _sample_inputs()
    kernel = PlanningKernel()
    result = kernel.run(lots, demands, max_iterations=3)
    final_state = result["final_state"]
    key = ("market_TYO", "P1", "202601")
    assert final_state.backlog_by_market_product_time[key] == 0.0
    assert len(result["selected_operators"]) >= 1
