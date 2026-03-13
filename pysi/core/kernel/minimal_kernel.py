# pysi/core/kernel/minimal_kernel.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple


EVENT_PRIORITY = {
    "production": 10,
    "shipment": 20,
    "arrival": 30,
    "sale": 40,
    "inventory_adjustment": 50,
}


def advance_time_bucket(time_bucket: str, weeks: int) -> str:
    year = int(time_bucket[:4])
    week = int(time_bucket[4:6])
    for _ in range(max(weeks, 0)):
        week += 1
        if week > 52:
            year += 1
            week = 1
    return f"{year:04d}{week:02d}"


@dataclass(frozen=True)
class Lot:
    lot_id: str
    product_id: str
    origin_node: str
    destination_node: Optional[str]
    quantity_cpu: float
    created_time_bucket: str
    attributes: Optional[dict] = None


@dataclass(frozen=True)
class DemandEvent:
    demand_id: str
    market_id: str
    product_id: str
    time_bucket: str
    quantity_cpu: float
    price: Optional[float] = None
    channel_id: Optional[str] = None
    metadata: Optional[dict] = None


@dataclass(frozen=True)
class FlowEvent:
    # NOTE: `flow_id` is retained for compatibility with earlier minimal kernel versions.
    # The record is still treated as a deterministic event record in execution ordering.
    flow_id: str
    lot_id: str
    event_type: str
    product_id: str
    from_node: Optional[str]
    to_node: Optional[str]
    time_bucket: str
    quantity_cpu: float
    creation_sequence: int
    metadata: Optional[dict] = None


@dataclass(frozen=True)
class TrustEvent:
    trust_event_id: str
    event_type: str
    severity: float
    node_id: Optional[str]
    product_id: Optional[str]
    time_bucket: str
    message: str
    evidence: Optional[dict] = None


@dataclass(frozen=True)
class StateView:
    inventory_by_node_product_time: Dict[Tuple[str, str, str], float]
    demand_by_market_product_time: Dict[Tuple[str, str, str], float]
    supply_by_node_product_time: Dict[Tuple[str, str, str], float]
    backlog_by_market_product_time: Dict[Tuple[str, str, str], float]
    capacity_usage_by_resource_time: Dict[Tuple[str, str], float]
    financial_summary: Optional[dict] = None


@dataclass(frozen=True)
class Operator:
    operator_id: str
    operator_type: str
    target: dict
    parameters: dict
    rationale: Optional[str] = None


@dataclass(frozen=True)
class EvaluationResult:
    total_score: float
    service_level: float
    inventory_penalty: float
    risk_penalty: float
    details: Optional[dict] = None


class FlowEngine:
    def run_flow(self, flow_events: List[FlowEvent], demand_events: List[DemandEvent]) -> StateView:
        ordered_events = sorted(
            flow_events,
            key=lambda e: (e.time_bucket, EVENT_PRIORITY.get(e.event_type, 999), e.creation_sequence, e.flow_id),
        )
        demand_ordered = sorted(demand_events, key=lambda d: (d.time_bucket, d.market_id, d.product_id, d.demand_id))

        demand: Dict[Tuple[str, str, str], float] = {}
        supply: Dict[Tuple[str, str, str], float] = {}
        backlog: Dict[Tuple[str, str, str], float] = {}
        capacity_usage: Dict[Tuple[str, str], float] = {}
        inventory_snapshot: Dict[Tuple[str, str, str], float] = {}
        current_inventory: Dict[Tuple[str, str], float] = {}

        events_by_time: Dict[str, List[FlowEvent]] = {}
        for evt in ordered_events:
            events_by_time.setdefault(evt.time_bucket, []).append(evt)

        demands_by_time: Dict[str, List[DemandEvent]] = {}
        for d in demand_ordered:
            demands_by_time.setdefault(d.time_bucket, []).append(d)

        time_buckets = sorted(set(events_by_time.keys()) | set(demands_by_time.keys()))

        for bucket in time_buckets:
            bucket_events = sorted(
                events_by_time.get(bucket, []),
                key=lambda e: (EVENT_PRIORITY.get(e.event_type, 999), e.creation_sequence, e.flow_id),
            )

            touched: Set[Tuple[str, str]] = set()

            for evt in bucket_events:
                if evt.event_type == "production":
                    node = evt.to_node or evt.from_node
                    if node is None:
                        continue
                    nkey = (node, evt.product_id)
                    current_inventory[nkey] = current_inventory.get(nkey, 0.0) + evt.quantity_cpu
                    c_key = (node, bucket)
                    capacity_usage[c_key] = capacity_usage.get(c_key, 0.0) + evt.quantity_cpu
                    touched.add(nkey)

                elif evt.event_type == "shipment":
                    if evt.from_node is None:
                        continue
                    nkey = (evt.from_node, evt.product_id)
                    current_inventory[nkey] = current_inventory.get(nkey, 0.0) - evt.quantity_cpu
                    touched.add(nkey)

                elif evt.event_type in {"arrival", "inventory_adjustment"}:
                    node = evt.to_node or evt.from_node
                    if node is None:
                        continue
                    nkey = (node, evt.product_id)
                    current_inventory[nkey] = current_inventory.get(nkey, 0.0) + evt.quantity_cpu
                    if evt.event_type == "arrival":
                        s_key = (node, evt.product_id, bucket)
                        supply[s_key] = supply.get(s_key, 0.0) + evt.quantity_cpu
                    touched.add(nkey)

                elif evt.event_type == "sale":
                    node = evt.from_node or evt.to_node
                    if node is None:
                        continue
                    nkey = (node, evt.product_id)
                    current_inventory[nkey] = current_inventory.get(nkey, 0.0) - evt.quantity_cpu
                    touched.add(nkey)

            for d in demands_by_time.get(bucket, []):
                d_key = (d.market_id, d.product_id, bucket)
                demand[d_key] = demand.get(d_key, 0.0) + d.quantity_cpu

                market_key = (d.market_id, d.product_id)
                available = max(current_inventory.get(market_key, 0.0), 0.0)
                sold = min(available, d.quantity_cpu)
                current_inventory[market_key] = current_inventory.get(market_key, 0.0) - sold
                backlog[d_key] = d.quantity_cpu - sold
                touched.add(market_key)

            for node, product in sorted(touched):
                snapshot_key = (node, product, bucket)
                inventory_snapshot[snapshot_key] = current_inventory.get((node, product), 0.0)

        return StateView(
            inventory_by_node_product_time=inventory_snapshot,
            demand_by_market_product_time=demand,
            supply_by_node_product_time=supply,
            backlog_by_market_product_time=backlog,
            capacity_usage_by_resource_time=capacity_usage,
            financial_summary=None,
        )

    def detect_trust_events(self, state: StateView, capacity_limit: float = 100.0) -> List[TrustEvent]:
        trust_events: List[TrustEvent] = []

        for (node, product, time_bucket), backlog in sorted(state.backlog_by_market_product_time.items()):
            if backlog > 0:
                trust_events.append(
                    TrustEvent(
                        trust_event_id=f"te-stockout-{node}-{product}-{time_bucket}",
                        event_type="E_STOCKOUT_RISK",
                        severity=backlog,
                        node_id=node,
                        product_id=product,
                        time_bucket=time_bucket,
                        message=f"Backlog {backlog:.2f} detected",
                        evidence={"backlog": backlog},
                    )
                )

        for (node, time_bucket), usage in sorted(state.capacity_usage_by_resource_time.items()):
            overload = usage - capacity_limit
            if overload > 0:
                trust_events.append(
                    TrustEvent(
                        trust_event_id=f"te-capacity-{node}-{time_bucket}",
                        event_type="E_CAPACITY_OVERLOAD",
                        severity=overload,
                        node_id=node,
                        product_id=None,
                        time_bucket=time_bucket,
                        message=f"Capacity overload {overload:.2f} detected",
                        evidence={"usage": usage, "capacity_limit": capacity_limit},
                    )
                )

        return trust_events


class Evaluator:
    def evaluate_state(self, state: StateView) -> EvaluationResult:
        total_demand = sum(state.demand_by_market_product_time.values())
        total_backlog = sum(state.backlog_by_market_product_time.values())
        total_inventory = sum(abs(v) for v in state.inventory_by_node_product_time.values())
        service_level = 1.0 if total_demand == 0 else max((total_demand - total_backlog) / total_demand, 0.0)
        inventory_penalty = total_inventory * 0.001
        risk_penalty = total_backlog * 0.01
        total_score = service_level - inventory_penalty - risk_penalty
        return EvaluationResult(
            total_score=total_score,
            service_level=service_level,
            inventory_penalty=inventory_penalty,
            risk_penalty=risk_penalty,
            details={"total_demand": total_demand, "total_backlog": total_backlog},
        )


class Resolver:
    def generate_candidates(
        self,
        trust_events: List[TrustEvent],
        production_nodes: Set[str],
        upstream_by_node: Dict[str, str],
        product_origin_node: Dict[str, str],
    ) -> List[Operator]:
        candidates: List[Operator] = []

        for te in sorted(trust_events, key=lambda t: (t.time_bucket, t.event_type, t.node_id or "", t.trust_event_id)):
            if te.event_type != "E_STOCKOUT_RISK":
                continue

            stockout_node = te.node_id or ""
            if stockout_node in production_nodes:
                source_node = stockout_node
            else:
                source_node = upstream_by_node.get(stockout_node, product_origin_node.get(te.product_id or "", stockout_node))

            candidates.append(
                Operator(
                    operator_id=f"op-prod-{te.trust_event_id}",
                    operator_type="add_production",
                    target={"source_node": source_node, "destination_node": stockout_node, "product": te.product_id, "time_bucket": te.time_bucket},
                    parameters={"quantity_cpu": te.severity},
                    rationale="Resolve stockout via production at production-capable upstream node",
                )
            )
        return candidates

    def apply_operator(self, flow_events: List[FlowEvent], operator: Operator, lead_time_weeks: int) -> List[FlowEvent]:
        new_events = list(flow_events)
        qty = float(operator.parameters["quantity_cpu"])
        seq = 0 if not new_events else max(e.creation_sequence for e in new_events) + 1

        if operator.operator_type == "add_production":
            source_node = operator.target["source_node"]
            dest_node = operator.target["destination_node"]
            product = operator.target["product"]
            t0 = operator.target["time_bucket"]
            t1 = advance_time_bucket(t0, lead_time_weeks)

            new_events.extend(
                [
                    FlowEvent(
                        flow_id=f"f-{operator.operator_id}-prod",
                        lot_id=f"lot-{operator.operator_id}",
                        event_type="production",
                        product_id=product,
                        from_node=source_node,
                        to_node=source_node,
                        time_bucket=t0,
                        quantity_cpu=qty,
                        creation_sequence=seq,
                        metadata={"operator_id": operator.operator_id},
                    ),
                    FlowEvent(
                        flow_id=f"f-{operator.operator_id}-ship",
                        lot_id=f"lot-{operator.operator_id}",
                        event_type="shipment",
                        product_id=product,
                        from_node=source_node,
                        to_node=dest_node,
                        time_bucket=t0,
                        quantity_cpu=qty,
                        creation_sequence=seq + 1,
                        metadata={"operator_id": operator.operator_id},
                    ),
                    FlowEvent(
                        flow_id=f"f-{operator.operator_id}-arr",
                        lot_id=f"lot-{operator.operator_id}",
                        event_type="arrival",
                        product_id=product,
                        from_node=source_node,
                        to_node=dest_node,
                        time_bucket=t1,
                        quantity_cpu=qty,
                        creation_sequence=seq + 2,
                        metadata={"operator_id": operator.operator_id},
                    ),
                ]
            )
        return new_events


class PlanningKernel:
    def __init__(self) -> None:
        self.flow_engine = FlowEngine()
        self.evaluator = Evaluator()
        self.resolver = Resolver()

    def _lot_to_events(self, lot: Lot, start_seq: int, lead_time_weeks: int) -> List[FlowEvent]:
        source = lot.origin_node
        dest = lot.destination_node or lot.origin_node
        t0 = lot.created_time_bucket
        t1 = advance_time_bucket(t0, lead_time_weeks)
        q = lot.quantity_cpu

        return [
            FlowEvent(
                flow_id=f"f-{lot.lot_id}-prod",
                lot_id=lot.lot_id,
                event_type="production",
                product_id=lot.product_id,
                from_node=source,
                to_node=source,
                time_bucket=t0,
                quantity_cpu=q,
                creation_sequence=start_seq,
                metadata={"source": "initial_lot"},
            ),
            FlowEvent(
                flow_id=f"f-{lot.lot_id}-ship",
                lot_id=lot.lot_id,
                event_type="shipment",
                product_id=lot.product_id,
                from_node=source,
                to_node=dest,
                time_bucket=t0,
                quantity_cpu=q,
                creation_sequence=start_seq + 1,
                metadata={"source": "initial_lot"},
            ),
            FlowEvent(
                flow_id=f"f-{lot.lot_id}-arr",
                lot_id=lot.lot_id,
                event_type="arrival",
                product_id=lot.product_id,
                from_node=source,
                to_node=dest,
                time_bucket=t1,
                quantity_cpu=q,
                creation_sequence=start_seq + 2,
                metadata={"source": "initial_lot"},
            ),
        ]

    def run(
        self,
        lots: List[Lot],
        demand_events: List[DemandEvent],
        initial_flow_events: Optional[List[FlowEvent]] = None,
        max_iterations: int = 3,
        capacity_limit: float = 100.0,
        lead_time_weeks: int = 1,
        production_nodes: Optional[Set[str]] = None,
        upstream_by_node: Optional[Dict[str, str]] = None,
    ) -> dict:
        flow_events = list(initial_flow_events or [])
        next_seq = 0 if not flow_events else max(e.creation_sequence for e in flow_events) + 1

        lot_origin_by_product: Dict[str, str] = {}
        inferred_production_nodes: Set[str] = set()
        inferred_upstream: Dict[str, str] = {}

        for lot in sorted(lots, key=lambda l: (l.created_time_bucket, l.lot_id)):
            lot_events = self._lot_to_events(lot, next_seq, lead_time_weeks=lead_time_weeks)
            flow_events.extend(lot_events)
            next_seq += len(lot_events)

            lot_origin_by_product.setdefault(lot.product_id, lot.origin_node)
            inferred_production_nodes.add(lot.origin_node)
            if lot.destination_node:
                inferred_upstream.setdefault(lot.destination_node, lot.origin_node)

        actual_production_nodes = set(production_nodes or inferred_production_nodes)
        actual_upstream = dict(inferred_upstream)
        actual_upstream.update(upstream_by_node or {})

        history: List[dict] = []
        selected_operators: List[Operator] = []

        for _ in range(max_iterations):
            state = self.flow_engine.run_flow(flow_events, demand_events)
            trust_events = self.flow_engine.detect_trust_events(state, capacity_limit=capacity_limit)
            evaluation = self.evaluator.evaluate_state(state)
            history.append({"state": state, "trust_events": trust_events, "evaluation": evaluation})

            if not trust_events:
                break

            candidates = self.resolver.generate_candidates(
                trust_events=trust_events,
                production_nodes=actual_production_nodes,
                upstream_by_node=actual_upstream,
                product_origin_node=lot_origin_by_product,
            )
            if not candidates:
                break

            chosen = candidates[0]
            selected_operators.append(chosen)
            flow_events = self.resolver.apply_operator(flow_events, chosen, lead_time_weeks=lead_time_weeks)

        return {
            "flow_events": flow_events,
            "final_state": history[-1]["state"],
            "final_trust_events": history[-1]["trust_events"],
            "final_evaluation": history[-1]["evaluation"],
            "selected_operators": selected_operators,
            "history": history,
        }


def _demo() -> None:
    lots = [
        Lot("lot-1", "P1", "factory_A", "market_TYO", 70.0, "202601"),
        Lot("lot-2", "P1", "factory_A", "market_OSA", 20.0, "202601"),
    ]
    demand_events = [
        DemandEvent("d-1", "market_TYO", "P1", "202602", 100.0),
        DemandEvent("d-2", "market_OSA", "P1", "202602", 20.0),
    ]
    result = PlanningKernel().run(
        lots=lots,
        demand_events=demand_events,
        max_iterations=3,
        lead_time_weeks=0,
        production_nodes={"factory_A"},
        upstream_by_node={"market_TYO": "factory_A", "market_OSA": "factory_A"},
    )
    final_eval = result["final_evaluation"]
    print("Final evaluation:")
    print(f"  total_score={final_eval.total_score:.4f}")
    print(f"  service_level={final_eval.service_level:.4f}")
    print(f"  inventory_penalty={final_eval.inventory_penalty:.4f}")
    print(f"  risk_penalty={final_eval.risk_penalty:.4f}")
    print(f"  selected_operators={len(result['selected_operators'])}")


if __name__ == "__main__":
    _demo()
