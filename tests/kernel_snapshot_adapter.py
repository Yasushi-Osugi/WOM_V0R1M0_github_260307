from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, List, Optional, Tuple


# ============================================================
# Generic helpers for attribute / dict access
# ============================================================

def _get(obj: Any, *names: str, default=None):
    """
    Read from either object attribute or dict key using multiple aliases.
    """
    if obj is None:
        return default

    if isinstance(obj, dict):
        for name in names:
            if name in obj:
                return obj[name]
        return default

    for name in names:
        if hasattr(obj, name):
            return getattr(obj, name)
    return default


def _event_time_bucket(evt: Any) -> Optional[str]:
    return _get(
        evt,
        "time_bucket",
        "event_time_bucket",
        "week",
        "bucket",
        default=None,
    )


def _event_type(evt: Any) -> str:
    return str(
        _get(
            evt,
            "event_type",
            "type",
            default="unknown",
        )
    ).lower()


def _lot_id(evt: Any) -> Optional[str]:
    return _get(evt, "lot_id", "object_id", default=None)


def _product_id(evt: Any, default_product_id: str) -> str:
    return str(_get(evt, "product_id", "sku", default=default_product_id))


def _qty(evt: Any, default: float = 0.0) -> float:
    value = _get(
        evt,
        "quantity_cpu",
        "quantity",
        "qty",
        "demand_qty",
        default=default,
    )
    try:
        return float(value)
    except Exception:
        return float(default)


def _from_node(evt: Any) -> Optional[str]:
    return _get(
        evt,
        "from_node",
        "source_node",
        "origin_node",
        "node_from",
        default=None,
    )


def _to_node(evt: Any) -> Optional[str]:
    return _get(
        evt,
        "to_node",
        "destination_node",
        "dest_node",
        "node_to",
        default=None,
    )


def _market_node(evt: Any) -> Optional[str]:
    return _get(
        evt,
        "market_id",
        "node_id",
        "destination_node",
        "to_node",
        default=None,
    )


def _description(evt: Any) -> str:
    et = _event_type(evt)
    lot = _lot_id(evt)
    src = _from_node(evt)
    dst = _to_node(evt)
    tb = _event_time_bucket(evt)

    if et == "production":
        return f"Production created lot={lot} at {src or dst}"
    if et == "shipment":
        return f"Shipment departed {src} for {dst}"
    if et == "arrival":
        return f"Arrival completed at {dst}"
    if et == "demand":
        return f"Demand generated at { _market_node(evt) } in {tb}"
    if et == "sale":
        return f"Sale executed for lot={lot}"
    return f"{et} event"


def _edge_id(src: Optional[str], dst: Optional[str]) -> str:
    return f"{src}->{dst}"


def _safe_float(x: Any, default: float = 0.0) -> float:
    try:
        return float(x)
    except Exception:
        return default


# ============================================================
# Minimal time bucket helpers
# ============================================================

def advance_time_bucket(time_bucket: str, weeks: int) -> str:
    """
    Fallback implementation if you do not want to import from minimal_kernel.
    Supports format YYYYWww, e.g. 2026W01.
    """
    year = int(time_bucket[:4])
    week = int(time_bucket[5:7])

    for _ in range(max(weeks, 0)):
        week += 1
        if week > 52:
            year += 1
            week = 1

    return f"{year:04d}W{week:02d}"


def sort_time_buckets(time_buckets: List[str]) -> List[str]:
    def key(tb: str):
        return (int(tb[:4]), int(tb[5:7]))
    return sorted(time_buckets, key=key)


def build_dense_time_buckets(event_time_buckets: List[str]) -> List[str]:
    """
    Fill missing weeks between min/max.
    """
    if not event_time_buckets:
        return []

    ordered = sort_time_buckets(list(set(event_time_buckets)))
    start = ordered[0]
    end = ordered[-1]

    result = [start]
    cur = start
    while cur != end:
        cur = advance_time_bucket(cur, 1)
        result.append(cur)
    return result


# ============================================================
# Snapshot Adapter
# ============================================================

def build_snapshots_from_kernel_events(
    events: List[Any],
    node_master: Dict[str, Dict[str, Any]],
    edge_master: List[Dict[str, Any]],
    default_product_id: str = "SKU_A",
) -> Tuple[Dict[str, dict], List[str]]:
    """
    Convert minimal_kernel v1.0 style events into visualizer snapshots.

    Assumptions for v1.0:
    - demand exists
    - sale may be implicit
    - arrival/shipment/production are explicit
    - explicit SaleEvent may or may not exist

    Parameters
    ----------
    events:
        Event list from kernel replay or kernel output.
    node_master:
        Example:
        {
            "FACTORY_A": {"type": "factory", "x": 0.0, "y": 0.8, "overflow_threshold": 450},
            "DC_TOKYO": {"type": "dc", "x": 5.0, "y": 0.0, "overflow_threshold": 350},
            "MARKET_TOKYO": {"type": "market", "x": 10.0, "y": 0.8, "overflow_threshold": 100},
        }
    edge_master:
        Example:
        [
            {"from_node": "FACTORY_A", "to_node": "DC_TOKYO", "capacity": 300, "lead_time_weeks": 1},
            {"from_node": "DC_TOKYO", "to_node": "MARKET_TOKYO", "capacity": 250, "lead_time_weeks": 1},
        ]

    Returns
    -------
    snapshots, time_buckets
        snapshots has the same shape as build_mock_snapshots() in your visualizer.
    """
    if not events:
        return {}, []

    # --------------------------------------------------------
    # 0. Normalize masters
    # --------------------------------------------------------
    edge_master_by_id: Dict[str, Dict[str, Any]] = {}
    for e in edge_master:
        src = e["from_node"]
        dst = e["to_node"]
        edge_master_by_id[_edge_id(src, dst)] = dict(e)

    # --------------------------------------------------------
    # 1. Normalize and sort events
    # --------------------------------------------------------
    normalized_events = []
    for evt in events:
        tb = _event_time_bucket(evt)
        if tb is None:
            continue

        et = _event_type(evt)
        normalized_events.append(
            {
                "raw": evt,
                "time_bucket": tb,
                "event_type": et,
                "lot_id": _lot_id(evt),
                "product_id": _product_id(evt, default_product_id),
                "qty": _qty(evt, 0.0),
                "from_node": _from_node(evt),
                "to_node": _to_node(evt),
                "market_node": _market_node(evt),
                "description": _description(evt),
            }
        )

    normalized_events.sort(key=lambda x: (x["time_bucket"], x["event_type"], x["lot_id"] or ""))

    event_time_buckets = [e["time_bucket"] for e in normalized_events]
    time_buckets = build_dense_time_buckets(event_time_buckets)

    events_by_tb: Dict[str, List[dict]] = {tb: [] for tb in time_buckets}
    for evt in normalized_events:
        events_by_tb[evt["time_bucket"]].append(evt)

    # --------------------------------------------------------
    # 2. Runtime state
    # --------------------------------------------------------
    current_inventory: Dict[Tuple[str, str], float] = {}
    current_backlog: Dict[Tuple[str, str], float] = {}

    lot_states: Dict[str, Dict[str, Any]] = {}

    # weekly metrics for PSI
    weekly_demand: Dict[Tuple[str, str, str], float] = {}
    weekly_shipment: Dict[Tuple[str, str, str], float] = {}
    weekly_arrival: Dict[Tuple[str, str, str], float] = {}
    weekly_sales: Dict[Tuple[str, str, str], float] = {}
    weekly_inventory: Dict[Tuple[str, str, str], float] = {}
    weekly_backlog: Dict[Tuple[str, str, str], float] = {}

    # weekly edge flow
    weekly_edge_flow: Dict[Tuple[str, str], float] = {}

    # state history by week
    state_history: Dict[str, Dict[str, Any]] = {}

    # --------------------------------------------------------
    # 3. Replay by time bucket
    # --------------------------------------------------------
    for tb in time_buckets:
        # weekly event log rows
        event_rows = []

        # clear weekly flow for current tb
        for edge_id in edge_master_by_id.keys():
            weekly_edge_flow[(tb, edge_id)] = 0.0

        # --------------------------------------------
        # 3-1. Apply explicit events
        # --------------------------------------------
        for evt in events_by_tb.get(tb, []):
            et = evt["event_type"]
            lot_id = evt["lot_id"]
            product_id = evt["product_id"]
            qty = evt["qty"]
            src = evt["from_node"]
            dst = evt["to_node"]
            market_node = evt["market_node"]

            # Event log row
            event_rows.append(
                EventRowViewModel(
                    time_bucket=tb,
                    event_type=et,
                    object_id=lot_id or "",
                    node_id=dst or src or market_node,
                    description=evt["description"],
                )
            )

            # ----------------------------
            # production
            # ----------------------------
            if et == "production":
                if lot_id is None:
                    continue

                origin = src or dst
                if origin is None:
                    continue

                lot_states[lot_id] = {
                    "lot_id": lot_id,
                    "product_id": product_id,
                    "quantity_cpu": qty,
                    "status": "at_node",
                    "current_node": origin,
                    "current_edge": None,
                    "created_time_bucket": tb,
                    "last_shipment_time_bucket": None,
                    "last_arrival_time_bucket": tb,
                    "age_weeks": 0,
                    "linked_demand_id": None,
                }

                current_inventory[(origin, product_id)] = current_inventory.get((origin, product_id), 0.0) + qty

            # ----------------------------
            # shipment
            # ----------------------------
            elif et == "shipment":
                if lot_id is None:
                    continue

                if lot_id not in lot_states:
                    # if kernel emits shipment before explicit production in replay feed,
                    # create a fallback lot state.
                    lot_states[lot_id] = {
                        "lot_id": lot_id,
                        "product_id": product_id,
                        "quantity_cpu": qty,
                        "status": "at_node",
                        "current_node": src,
                        "current_edge": None,
                        "created_time_bucket": tb,
                        "last_shipment_time_bucket": None,
                        "last_arrival_time_bucket": None,
                        "age_weeks": 0,
                        "linked_demand_id": None,
                    }

                lot = lot_states[lot_id]
                move_qty = lot["quantity_cpu"] if lot["quantity_cpu"] > 0 else qty

                if src is not None:
                    current_inventory[(src, product_id)] = current_inventory.get((src, product_id), 0.0) - move_qty

                edge_id = _edge_id(src, dst)
                lot["status"] = "in_transit"
                lot["current_node"] = None
                lot["current_edge"] = edge_id
                lot["last_shipment_time_bucket"] = tb

                weekly_shipment[(src or "", product_id, tb)] = weekly_shipment.get((src or "", product_id, tb), 0.0) + move_qty
                weekly_edge_flow[(tb, edge_id)] = weekly_edge_flow.get((tb, edge_id), 0.0) + move_qty

            # ----------------------------
            # arrival
            # ----------------------------
            elif et == "arrival":
                if lot_id is None or dst is None:
                    continue

                if lot_id not in lot_states:
                    lot_states[lot_id] = {
                        "lot_id": lot_id,
                        "product_id": product_id,
                        "quantity_cpu": qty,
                        "status": "at_node",
                        "current_node": dst,
                        "current_edge": None,
                        "created_time_bucket": tb,
                        "last_shipment_time_bucket": None,
                        "last_arrival_time_bucket": tb,
                        "age_weeks": 0,
                        "linked_demand_id": None,
                    }

                lot = lot_states[lot_id]
                move_qty = lot["quantity_cpu"] if lot["quantity_cpu"] > 0 else qty

                lot["status"] = "at_node"
                lot["current_node"] = dst
                lot["current_edge"] = None
                lot["last_arrival_time_bucket"] = tb

                current_inventory[(dst, product_id)] = current_inventory.get((dst, product_id), 0.0) + move_qty
                weekly_arrival[(dst, product_id, tb)] = weekly_arrival.get((dst, product_id, tb), 0.0) + move_qty

            # ----------------------------
            # demand (explicit in v1.0)
            # ----------------------------
            elif et == "demand":
                demand_node = market_node or dst or src
                if demand_node is None:
                    continue

                weekly_demand[(demand_node, product_id, tb)] = weekly_demand.get((demand_node, product_id, tb), 0.0) + qty
                current_backlog[(demand_node, product_id)] = current_backlog.get((demand_node, product_id), 0.0) + qty

            # ----------------------------
            # explicit sale (if v1.1-ish events are mixed in)
            # ----------------------------
            elif et == "sale":
                sale_node = market_node or dst or src
                if sale_node is None:
                    continue

                available = current_inventory.get((sale_node, product_id), 0.0)
                sold = min(available, qty)

                current_inventory[(sale_node, product_id)] = available - sold
                current_backlog[(sale_node, product_id)] = max(
                    current_backlog.get((sale_node, product_id), 0.0) - sold,
                    0.0,
                )
                weekly_sales[(sale_node, product_id, tb)] = weekly_sales.get((sale_node, product_id, tb), 0.0) + sold

        # --------------------------------------------
        # 3-2. Implicit sales for v1.0
        # --------------------------------------------
        for node_id, node_info in node_master.items():
            if node_info.get("type") != "market":
                continue

            product_id = default_product_id
            backlog = current_backlog.get((node_id, product_id), 0.0)
            available = current_inventory.get((node_id, product_id), 0.0)

            if backlog <= 0.0 or available <= 0.0:
                continue

            sold = min(backlog, available)

            current_inventory[(node_id, product_id)] = available - sold
            current_backlog[(node_id, product_id)] = backlog - sold
            weekly_sales[(node_id, product_id, tb)] = weekly_sales.get((node_id, product_id, tb), 0.0) + sold

            event_rows.append(
                EventRowViewModel(
                    time_bucket=tb,
                    event_type="sale",
                    object_id=f"IMPLICIT_SALE_{node_id}_{tb}",
                    node_id=node_id,
                    description=f"Implicit sale at {node_id}: sold={sold:.1f}",
                )
            )

        # --------------------------------------------
        # 3-3. Update lot ages
        # --------------------------------------------
        tb_index = time_buckets.index(tb)
        for lot in lot_states.values():
            created_tb = lot["created_time_bucket"]
            created_idx = time_buckets.index(created_tb) if created_tb in time_buckets else tb_index
            lot["age_weeks"] = max(tb_index - created_idx, 0)

        # --------------------------------------------
        # 3-4. Persist inventory/backlog time series
        # --------------------------------------------
        for node_id in node_master.keys():
            product_id = default_product_id
            weekly_inventory[(node_id, product_id, tb)] = current_inventory.get((node_id, product_id), 0.0)
            weekly_backlog[(node_id, product_id, tb)] = current_backlog.get((node_id, product_id), 0.0)

        # --------------------------------------------
        # 3-5. Save state history
        # --------------------------------------------
        state_history[tb] = {
            "inventory": deepcopy(current_inventory),
            "backlog": deepcopy(current_backlog),
            "lots": deepcopy(lot_states),
            "events": event_rows,
        }

    # --------------------------------------------------------
    # 4. Build PSI view models
    # --------------------------------------------------------
    psi_by_node_product_global: Dict[Tuple[str, str], PSIViewModel] = {}

    for node_id, node_info in node_master.items():
        product_id = default_product_id

        psi_by_node_product_global[(node_id, product_id)] = PSIViewModel(
            node_id=node_id,
            product_id=product_id,
            weeks=time_buckets,
            demand=[weekly_demand.get((node_id, product_id, tb), 0.0) for tb in time_buckets],
            shipment=[weekly_shipment.get((node_id, product_id, tb), 0.0) for tb in time_buckets],
            arrival=[weekly_arrival.get((node_id, product_id, tb), 0.0) for tb in time_buckets],
            sales=[weekly_sales.get((node_id, product_id, tb), 0.0) for tb in time_buckets],
            inventory=[weekly_inventory.get((node_id, product_id, tb), 0.0) for tb in time_buckets],
            backlog=[weekly_backlog.get((node_id, product_id, tb), 0.0) for tb in time_buckets],
        )

    # --------------------------------------------------------
    # 5. Build snapshots in visualizer schema
    # --------------------------------------------------------
    snapshots: Dict[str, dict] = {}

    for tb in time_buckets:
        inv_state = state_history[tb]["inventory"]
        backlog_state = state_history[tb]["backlog"]
        lot_state = state_history[tb]["lots"]
        event_rows = state_history[tb]["events"]

        # nodes
        node_vms = []
        for node_id, node_info in node_master.items():
            product_id = default_product_id
            inv = inv_state.get((node_id, product_id), 0.0)
            backlog = backlog_state.get((node_id, product_id), 0.0)

            overflow_threshold = _safe_float(node_info.get("overflow_threshold", 999999.0), 999999.0)
            sales_qty = weekly_sales.get((node_id, product_id, tb), 0.0)

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

        # edges
        edge_vms = []
        for edge_id, edge_info in edge_master_by_id.items():
            src = edge_info["from_node"]
            dst = edge_info["to_node"]
            cap = _safe_float(edge_info.get("capacity", 0.0), 0.0)
            flow = weekly_edge_flow.get((tb, edge_id), 0.0)
            congestion_ratio = (flow / cap) if cap > 0 else 0.0

            edge_vms.append(
                EdgeViewModel(
                    edge_id=edge_id,
                    from_node=src,
                    to_node=dst,
                    capacity=cap,
                    flow_qty=flow,
                    congestion_ratio=congestion_ratio,
                )
            )

        # lots
        lot_vms = []
        for lot_id, lot in lot_state.items():
            current_edge = lot.get("current_edge")
            current_node = lot.get("current_node")
            product_id = lot.get("product_id", default_product_id)

            progress = 0.0
            if current_edge is not None:
                edge_info = edge_master_by_id.get(current_edge, {})
                lead_time = int(edge_info.get("lead_time_weeks", 1))
                last_ship_tb = lot.get("last_shipment_time_bucket")
                if last_ship_tb and last_ship_tb in time_buckets:
                    elapsed = time_buckets.index(tb) - time_buckets.index(last_ship_tb)
                else:
                    elapsed = 0

                progress = min(max((elapsed + 0.35) / max(lead_time, 1), 0.05), 0.95)

            lot_vms.append(
                LotViewModel(
                    lot_id=lot_id,
                    product_id=product_id,
                    quantity_cpu=_safe_float(lot.get("quantity_cpu", 0.0)),
                    status=lot.get("status", "unknown"),
                    current_node=current_node,
                    current_edge=current_edge,
                    progress=progress,
                    age_weeks=int(lot.get("age_weeks", 0)),
                    linked_demand_id=lot.get("linked_demand_id"),
                )
            )

        inventory_total = sum(n.inventory_qty for n in node_vms)
        sales_total = sum(n.sales_qty for n in node_vms)
        backlog_total = sum(backlog_state.get((node_id, default_product_id), 0.0) for node_id in node_master.keys())

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