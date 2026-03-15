# pysi/visualization/snapshot_adapter.py

from __future__ import annotations

from copy import deepcopy
from typing import Dict, List, Optional, Tuple, Any

from pysi.core.kernel.minimal_kernel import (
    DemandEvent,
    FlowEvent,
    StateView,
    advance_time_bucket,
)

from visualization.viewmodels import (
    NodeViewModel,
    EdgeViewModel,
    LotViewModel,
    PSIViewModel,
    EventRowViewModel,
)


def _edge_id(src: Optional[str], dst: Optional[str]) -> str:
    return f"{src}->{dst}"


def _safe_float(x: Any, default: float = 0.0) -> float:
    try:
        return float(x)
    except Exception:
        return default


def sort_time_buckets(time_buckets: List[str]) -> List[str]:
    def key(tb: str):
        return (int(tb[:4]), int(tb[4:6]))
    return sorted(time_buckets, key=key)


def build_dense_time_buckets(time_buckets: List[str]) -> List[str]:
    if not time_buckets:
        return []

    ordered = sort_time_buckets(list(set(time_buckets)))
    start = ordered[0]
    end = ordered[-1]

    result = [start]
    cur = start
    while cur != end:
        cur = advance_time_bucket(cur, 1)
        result.append(cur)
    return result


def _build_event_rows_for_bucket(
    tb: str,
    flow_events_by_tb: Dict[str, List[FlowEvent]],
    demand_events_by_tb: Dict[str, List[DemandEvent]],
    state: StateView,
) -> List[EventRowViewModel]:
    rows: List[EventRowViewModel] = []

    for evt in flow_events_by_tb.get(tb, []):
        if evt.event_type == "production":
            desc = f"Production created lot={evt.lot_id} at {evt.to_node or evt.from_node}"
        elif evt.event_type == "shipment":
            desc = f"Shipment departed {evt.from_node} for {evt.to_node}"
        elif evt.event_type == "arrival":
            desc = f"Arrival completed at {evt.to_node}"
        elif evt.event_type == "sale":
            desc = f"Sale executed for lot={evt.lot_id}"
        elif evt.event_type == "inventory_adjustment":
            desc = f"Inventory adjusted at {evt.to_node or evt.from_node}"
        else:
            desc = f"{evt.event_type} event"

        rows.append(
            EventRowViewModel(
                time_bucket=tb,
                event_type=evt.event_type,
                object_id=evt.lot_id,
                node_id=evt.to_node or evt.from_node,
                description=desc,
            )
        )

    for d in demand_events_by_tb.get(tb, []):
        demand_key = (d.market_id, d.product_id, d.time_bucket)
        backlog = state.backlog_by_market_product_time.get(demand_key, 0.0)
        sold = max(d.quantity_cpu - backlog, 0.0)

        rows.append(
            EventRowViewModel(
                time_bucket=tb,
                event_type="demand",
                object_id=d.demand_id,
                node_id=d.market_id,
                description=f"Demand generated at {d.market_id}: qty={d.quantity_cpu:.1f}",
            )
        )

        if sold > 0:
            rows.append(
                EventRowViewModel(
                    time_bucket=tb,
                    event_type="sale",
                    object_id=d.demand_id,
                    node_id=d.market_id,
                    description=f"Implicit sale at {d.market_id}: sold={sold:.1f}",
                )
            )

    return rows


def _build_lot_states_by_bucket(
    flow_events: List[FlowEvent],
    edge_master_by_id: Dict[str, Dict[str, Any]],
    time_buckets: List[str],
) -> Dict[str, Dict[str, dict]]:
    """
    Reconstruct lot positions over time for visualization.

    Returns:
        lot_states_by_tb[tb][lot_id] = {
            ...
        }
    """
    lot_states: Dict[str, dict] = {}
    by_tb: Dict[str, List[FlowEvent]] = {}
    for evt in flow_events:
        by_tb.setdefault(evt.time_bucket, []).append(evt)

    lot_states_by_tb: Dict[str, Dict[str, dict]] = {}

    for tb in time_buckets:
        for evt in sorted(
            by_tb.get(tb, []),
            key=lambda e: (e.time_bucket, e.creation_sequence, e.flow_id),
        ):
            if evt.event_type == "production":
                origin = evt.to_node or evt.from_node
                if origin is None:
                    continue

                lot_states[evt.lot_id] = {
                    "lot_id": evt.lot_id,
                    "product_id": evt.product_id,
                    "quantity_cpu": evt.quantity_cpu,
                    "status": "at_node",
                    "current_node": origin,
                    "current_edge": None,
                    "created_time_bucket": tb,
                    "last_shipment_time_bucket": None,
                    "last_arrival_time_bucket": tb,
                    "age_weeks": 0,
                    "linked_demand_id": None,
                }

            elif evt.event_type == "shipment":
                if evt.lot_id not in lot_states:
                    lot_states[evt.lot_id] = {
                        "lot_id": evt.lot_id,
                        "product_id": evt.product_id,
                        "quantity_cpu": evt.quantity_cpu,
                        "status": "at_node",
                        "current_node": evt.from_node,
                        "current_edge": None,
                        "created_time_bucket": tb,
                        "last_shipment_time_bucket": None,
                        "last_arrival_time_bucket": None,
                        "age_weeks": 0,
                        "linked_demand_id": None,
                    }

                edge_id = _edge_id(evt.from_node, evt.to_node)
                lot_states[evt.lot_id]["status"] = "in_transit"
                lot_states[evt.lot_id]["current_node"] = None
                lot_states[evt.lot_id]["current_edge"] = edge_id
                lot_states[evt.lot_id]["last_shipment_time_bucket"] = tb

            elif evt.event_type in {"arrival", "inventory_adjustment"}:
                if evt.lot_id not in lot_states:
                    lot_states[evt.lot_id] = {
                        "lot_id": evt.lot_id,
                        "product_id": evt.product_id,
                        "quantity_cpu": evt.quantity_cpu,
                        "status": "at_node",
                        "current_node": evt.to_node or evt.from_node,
                        "current_edge": None,
                        "created_time_bucket": tb,
                        "last_shipment_time_bucket": None,
                        "last_arrival_time_bucket": tb,
                        "age_weeks": 0,
                        "linked_demand_id": None,
                    }

                node = evt.to_node or evt.from_node
                lot_states[evt.lot_id]["status"] = "at_node"
                lot_states[evt.lot_id]["current_node"] = node
                lot_states[evt.lot_id]["current_edge"] = None
                lot_states[evt.lot_id]["last_arrival_time_bucket"] = tb

            elif evt.event_type == "sale":
                if evt.lot_id in lot_states:
                    lot_states[evt.lot_id]["status"] = "sold"
                    lot_states[evt.lot_id]["current_node"] = evt.from_node or evt.to_node
                    lot_states[evt.lot_id]["current_edge"] = None

        tb_idx = time_buckets.index(tb)
        snapshot = deepcopy(lot_states)

        for lot in snapshot.values():
            created_tb = lot["created_time_bucket"]
            created_idx = time_buckets.index(created_tb) if created_tb in time_buckets else tb_idx
            lot["age_weeks"] = max(tb_idx - created_idx, 0)

            if lot["current_edge"] is not None:
                edge_info = edge_master_by_id.get(lot["current_edge"], {})
                lead_time = int(edge_info.get("lead_time_weeks", 1))
                last_ship_tb = lot.get("last_shipment_time_bucket")
                if last_ship_tb and last_ship_tb in time_buckets:
                    elapsed = time_buckets.index(tb) - time_buckets.index(last_ship_tb)
                else:
                    elapsed = 0
                lot["progress"] = min(max((elapsed + 0.35) / max(lead_time, 1), 0.05), 0.95)
            else:
                lot["progress"] = 0.0

        lot_states_by_tb[tb] = snapshot

    return lot_states_by_tb


def build_snapshots_from_kernel_result(
    kernel_result: dict,
    demand_events: List[DemandEvent],
    node_master: Dict[str, Dict[str, Any]],
    edge_master: List[Dict[str, Any]],
    default_product_id: str = "P1",
) -> Tuple[Dict[str, dict], List[str]]:
    """
    Build snapshots for Dash visualizer from PlanningKernel.run() result.

    kernel_result keys expected:
      - flow_events
      - final_state
      - history (optional)
    """
    flow_events: List[FlowEvent] = list(kernel_result.get("flow_events", []))
    final_state: StateView = kernel_result["final_state"]

    if not flow_events and not demand_events:
        return {}, []

    edge_master_by_id: Dict[str, Dict[str, Any]] = {}
    for e in edge_master:
        edge_master_by_id[_edge_id(e["from_node"], e["to_node"])] = dict(e)

    event_time_buckets = [e.time_bucket for e in flow_events] + [d.time_bucket for d in demand_events]
    time_buckets = build_dense_time_buckets(event_time_buckets)

    flow_events_by_tb: Dict[str, List[FlowEvent]] = {}
    for evt in flow_events:
        flow_events_by_tb.setdefault(evt.time_bucket, []).append(evt)

    demand_events_by_tb: Dict[str, List[DemandEvent]] = {}
    for d in demand_events:
        demand_events_by_tb.setdefault(d.time_bucket, []).append(d)

    lot_states_by_tb = _build_lot_states_by_bucket(flow_events, edge_master_by_id, time_buckets)

    # PSI series
    psi_by_node_product_global: Dict[Tuple[str, str], PSIViewModel] = {}
    for node_id, node_info in node_master.items():
        product_id = node_info.get("product_id", default_product_id)

        if node_info["type"] == "market":
            demand_series = [
                final_state.demand_by_market_product_time.get((node_id, product_id, tb), 0.0)
                for tb in time_buckets
            ]
            backlog_series = [
                final_state.backlog_by_market_product_time.get((node_id, product_id, tb), 0.0)
                for tb in time_buckets
            ]
            sales_series = [max(d - b, 0.0) for d, b in zip(demand_series, backlog_series)]
        else:
            demand_series = [0.0 for _ in time_buckets]
            backlog_series = [0.0 for _ in time_buckets]
            sales_series = [0.0 for _ in time_buckets]

        shipment_series = []
        arrival_series = []
        inventory_series = []

        for tb in time_buckets:
            shipment_qty = sum(
                evt.quantity_cpu
                for evt in flow_events_by_tb.get(tb, [])
                if evt.event_type == "shipment"
                and evt.from_node == node_id
                and evt.product_id == product_id
            )
            shipment_series.append(shipment_qty)

            arrival_qty = final_state.supply_by_node_product_time.get((node_id, product_id, tb), 0.0)
            arrival_series.append(arrival_qty)

            inventory_qty = final_state.inventory_by_node_product_time.get((node_id, product_id, tb), 0.0)
            inventory_series.append(inventory_qty)

        psi_by_node_product_global[(node_id, product_id)] = PSIViewModel(
            node_id=node_id,
            product_id=product_id,
            weeks=time_buckets,
            demand=demand_series,
            shipment=shipment_series,
            arrival=arrival_series,
            sales=sales_series,
            inventory=inventory_series,
            backlog=backlog_series,
        )

    snapshots: Dict[str, dict] = {}

    for tb in time_buckets:
        node_vms: List[NodeViewModel] = []
        for node_id, node_info in node_master.items():
            product_id = node_info.get("product_id", default_product_id)

            inv = final_state.inventory_by_node_product_time.get((node_id, product_id, tb), 0.0)
            backlog = final_state.backlog_by_market_product_time.get((node_id, product_id, tb), 0.0)
            demand_qty = final_state.demand_by_market_product_time.get((node_id, product_id, tb), 0.0)
            sales_qty = max(demand_qty - backlog, 0.0) if node_info["type"] == "market" else 0.0

            overflow_threshold = _safe_float(node_info.get("overflow_threshold", 999999.0), 999999.0)

            node_vms.append(
                NodeViewModel(
                    node_id=node_id,
                    node_type=node_info["type"],
                    x=_safe_float(node_info.get("x", 0.0)),
                    y=_safe_float(node_info.get("y", 0.0)),
                    inventory_qty=inv,
                    shortage_flag=(backlog > 0.0),
                    overflow_flag=(inv > overflow_threshold),
                    sales_qty=sales_qty,
                )
            )

        edge_vms: List[EdgeViewModel] = []
        for edge_id, edge_info in edge_master_by_id.items():
            src = edge_info["from_node"]
            dst = edge_info["to_node"]
            cap = _safe_float(edge_info.get("capacity", 0.0), 0.0)

            flow_qty = sum(
                evt.quantity_cpu
                for evt in flow_events_by_tb.get(tb, [])
                if evt.event_type == "shipment"
                and evt.from_node == src
                and evt.to_node == dst
            )
            congestion_ratio = (flow_qty / cap) if cap > 0 else 0.0

            edge_vms.append(
                EdgeViewModel(
                    edge_id=edge_id,
                    from_node=src,
                    to_node=dst,
                    capacity=cap,
                    flow_qty=flow_qty,
                    congestion_ratio=congestion_ratio,
                )
            )

        lot_vms: List[LotViewModel] = []
        for lot_id, lot in lot_states_by_tb[tb].items():
            lot_vms.append(
                LotViewModel(
                    lot_id=lot_id,
                    product_id=lot.get("product_id", default_product_id),
                    quantity_cpu=_safe_float(lot.get("quantity_cpu", 0.0)),
                    status=lot.get("status", "unknown"),
                    current_node=lot.get("current_node"),
                    current_edge=lot.get("current_edge"),
                    progress=_safe_float(lot.get("progress", 0.0)),
                    age_weeks=int(lot.get("age_weeks", 0)),
                    linked_demand_id=lot.get("linked_demand_id"),
                )
            )

        event_rows = _build_event_rows_for_bucket(tb, flow_events_by_tb, demand_events_by_tb, final_state)

        inventory_total = sum(n.inventory_qty for n in node_vms)
        sales_total = sum(n.sales_qty for n in node_vms)
        backlog_total = sum(
            final_state.backlog_by_market_product_time.get((node_id, node_info.get("product_id", default_product_id), tb), 0.0)
            for node_id, node_info in node_master.items()
            if node_info["type"] == "market"
        )

        snapshots[tb] = {
            "time_bucket": tb,
            "nodes": node_vms,
            "edges": edge_vms,
            "lots": lot_vms,
            "psi_by_node_product": deepcopy(psi_by_node_product_global),
            "events": event_rows,
            "kpis": {
                "inventory_total": round(inventory_total, 2),
                "sales_total": round(sales_total, 2),
                "backlog_total": round(backlog_total, 2),
            },
        }

    return snapshots, time_buckets