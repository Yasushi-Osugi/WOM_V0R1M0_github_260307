from __future__ import annotations

import argparse
import json
import sqlite3
from dataclasses import asdict
from pathlib import Path
from typing import Dict, List, Optional, Set

from minimal_kernel import (
    DemandEvent,
    FlowEvent,
    Lot,
    Operator,
    PlanningKernel,
    TrustEvent,
)
from wom_sqlite_repository import (
    FlowEventRecord,
    OperatorActionRecord,
    TrustEventRecord,
    WOMSQLiteRepository,
    json_dumps,
)


def row_to_lot(row: sqlite3.Row) -> Lot:
    return Lot(
        lot_id=row["lot_id"],
        product_id=row["product_id"],
        origin_node=row["origin_node"],
        destination_node=row["destination_node"],
        quantity_cpu=float(row["quantity_cpu"]),
        created_time_bucket=row["created_time_bucket"],
        attributes=json.loads(row["attributes_json"]) if row["attributes_json"] else None,
    )


def row_to_demand(row: sqlite3.Row) -> DemandEvent:
    return DemandEvent(
        demand_id=row["demand_id"],
        market_id=row["market_id"],
        product_id=row["product_id"],
        time_bucket=row["time_bucket"],
        quantity_cpu=float(row["quantity_cpu"]),
        price=row["price"],
        channel_id=row["channel_id"],
        metadata=json.loads(row["attributes_json"]) if row["attributes_json"] else None,
    )


def flow_event_to_record(
    event: FlowEvent,
    scenario_id: str,
    session_id: str,
    iteration_no: int,
) -> FlowEventRecord:
    return FlowEventRecord(
        flow_id=event.flow_id,
        scenario_id=scenario_id,
        session_id=session_id,
        iteration_no=iteration_no,
        lot_id=event.lot_id,
        event_type=event.event_type,
        product_id=event.product_id,
        from_node=event.from_node,
        to_node=event.to_node,
        time_bucket=event.time_bucket,
        quantity_cpu=float(event.quantity_cpu),
        creation_sequence=int(event.creation_sequence),
        event_priority=None,
        causal_event_id=None,
        operator_id=(event.metadata or {}).get("operator_id") if event.metadata else None,
        source_type=(event.metadata or {}).get("source") if event.metadata else None,
        status="planned",
        metadata_json=json_dumps(event.metadata) if event.metadata else None,
    )


def trust_event_to_record(
    event: TrustEvent,
    scenario_id: str,
    session_id: str,
    iteration_no: int,
) -> TrustEventRecord:
    return TrustEventRecord(
        trust_event_id=event.trust_event_id,
        scenario_id=scenario_id,
        session_id=session_id,
        iteration_no=iteration_no,
        event_type=event.event_type,
        severity=float(event.severity),
        node_id=event.node_id,
        product_id=event.product_id,
        time_bucket=event.time_bucket,
        message=event.message,
        evidence_json=json_dumps(event.evidence) if event.evidence else None,
    )


def operator_to_record(
    operator: Operator,
    scenario_id: str,
    session_id: str,
    iteration_no: int,
) -> OperatorActionRecord:
    return OperatorActionRecord(
        operator_id=operator.operator_id,
        scenario_id=scenario_id,
        session_id=session_id,
        iteration_no=iteration_no,
        operator_type=operator.operator_type,
        target_json=json_dumps(operator.target),
        parameters_json=json_dumps(operator.parameters),
        rationale=operator.rationale,
        selected_flag=1,
    )


def infer_network_context(lots: List[Lot]) -> tuple[Set[str], Dict[str, str]]:
    production_nodes: Set[str] = set()
    upstream_by_node: Dict[str, str] = {}

    for lot in lots:
        production_nodes.add(lot.origin_node)
        if lot.destination_node:
            upstream_by_node.setdefault(lot.destination_node, lot.origin_node)

    return production_nodes, upstream_by_node


def save_kernel_result(
    repo: WOMSQLiteRepository,
    scenario_id: str,
    session_id: str,
    result: dict,
) -> None:
    history = result["history"]
    selected_operators: List[Operator] = result["selected_operators"]
    final_flow_events: List[FlowEvent] = result["flow_events"]

    # 1) Save iteration history rows
    for i, hist in enumerate(history):
        evaluation = hist["evaluation"]
        trust_events = hist["trust_events"]

        selected_operator_id: Optional[str] = None
        if i < len(selected_operators):
            selected_operator_id = selected_operators[i].operator_id

        repo.insert_iteration_history(
            iteration_history_id=f"iterhist-{session_id}-{i}",
            session_id=session_id,
            iteration_no=i,
            evaluation_score=float(evaluation.total_score),
            service_level=float(evaluation.service_level),
            inventory_penalty=float(evaluation.inventory_penalty),
            risk_penalty=float(evaluation.risk_penalty),
            selected_operator_id=selected_operator_id,
            trust_event_count=len(trust_events),
            notes=f"Iteration {i}",
        )

        trust_records = [
            trust_event_to_record(te, scenario_id=scenario_id, session_id=session_id, iteration_no=i)
            for te in trust_events
        ]
        if trust_records:
            repo.insert_trust_events(trust_records)

    # 2) Save selected operators
    if selected_operators:
        operator_records = [
            operator_to_record(op, scenario_id=scenario_id, session_id=session_id, iteration_no=i)
            for i, op in enumerate(selected_operators)
        ]
        repo.insert_operator_actions(operator_records)

    # 3) Save final flow events
    #    For simplicity: persist all final flow events as the final iteration number
    final_iteration_no = max(len(history) - 1, 0)
    flow_records = [
        flow_event_to_record(
            event=evt,
            scenario_id=scenario_id,
            session_id=session_id,
            iteration_no=final_iteration_no,
        )
        for evt in final_flow_events
    ]
    if flow_records:
        repo.insert_flow_events(flow_records)


def print_run_summary(result: dict) -> None:
    final_eval = result["final_evaluation"]
    final_trust_events = result["final_trust_events"]
    selected_operators = result["selected_operators"]

    print("=== WOM Kernel DB Runner Summary ===")
    print(f"total_score      : {final_eval.total_score:.4f}")
    print(f"service_level    : {final_eval.service_level:.4f}")
    print(f"inventory_penalty: {final_eval.inventory_penalty:.4f}")
    print(f"risk_penalty     : {final_eval.risk_penalty:.4f}")
    print(f"trust_events     : {len(final_trust_events)}")
    print(f"selected_ops     : {len(selected_operators)}")

    if selected_operators:
        print("\nSelected Operators:")
        for op in selected_operators:
            print(f"  - {op.operator_id} ({op.operator_type})")

    if final_trust_events:
        print("\nFinal Trust Events:")
        for te in final_trust_events:
            print(f"  - {te.trust_event_id}: {te.event_type} / severity={te.severity:.2f}")


def run_kernel_from_db(
    db_path: str,
    scenario_id: str,
    session_id: str,
    engine_version: str = "planning-engine-v0",
    kernel_version: str = "kernel-v1.1",
    max_iterations: int = 3,
    capacity_limit: float = 100.0,
    lead_time_weeks: int = 0,
    initiated_by: str = "kernel_db_runner",
) -> dict:
    repo = WOMSQLiteRepository(db_path)

    lots = [row_to_lot(r) for r in repo.load_scenario_lots(scenario_id)]
    demands = [row_to_demand(r) for r in repo.load_scenario_demands(scenario_id)]

    if not lots:
        raise ValueError(f"No lots found for scenario_id={scenario_id}")
    if not demands:
        raise ValueError(f"No demand events found for scenario_id={scenario_id}")

    production_nodes, upstream_by_node = infer_network_context(lots)

    repo.create_session(
        session_id=session_id,
        scenario_id=scenario_id,
        engine_version=engine_version,
        kernel_version=kernel_version,
        status="running",
        initiated_by=initiated_by,
        notes="Started by kernel_db_runner.py",
    )

    kernel = PlanningKernel()
    result = kernel.run(
        lots=lots,
        demand_events=demands,
        initial_flow_events=None,
        max_iterations=max_iterations,
        capacity_limit=capacity_limit,
        lead_time_weeks=lead_time_weeks,
        production_nodes=production_nodes,
        upstream_by_node=upstream_by_node,
    )

    save_kernel_result(
        repo=repo,
        scenario_id=scenario_id,
        session_id=session_id,
        result=result,
    )

    repo.complete_session(session_id=session_id, status="completed")
    return result


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run WOM PlanningKernel using SQLite scenario inputs.")
    parser.add_argument("--db", required=True, help="Path to SQLite database file")
    parser.add_argument("--scenario_id", required=True, help="Scenario ID")
    parser.add_argument("--session_id", required=True, help="Session ID to create")
    parser.add_argument("--engine_version", default="planning-engine-v0", help="Planning engine version label")
    parser.add_argument("--kernel_version", default="kernel-v1.1", help="Kernel version label")
    parser.add_argument("--max_iterations", type=int, default=3, help="Maximum planning iterations")
    parser.add_argument("--capacity_limit", type=float, default=100.0, help="Capacity limit")
    parser.add_argument("--lead_time_weeks", type=int, default=0, help="Lead time in weeks")
    parser.add_argument("--initiated_by", default="kernel_db_runner", help="Initiator name")
    return parser


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()

    result = run_kernel_from_db(
        db_path=args.db,
        scenario_id=args.scenario_id,
        session_id=args.session_id,
        engine_version=args.engine_version,
        kernel_version=args.kernel_version,
        max_iterations=args.max_iterations,
        capacity_limit=args.capacity_limit,
        lead_time_weeks=args.lead_time_weeks,
        initiated_by=args.initiated_by,
    )

    print_run_summary(result)


if __name__ == "__main__":
    main()