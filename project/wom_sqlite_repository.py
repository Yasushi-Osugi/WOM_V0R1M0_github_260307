from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class LotRecord:
    lot_id: str
    scenario_id: str
    lot_type: Optional[str]
    product_id: str
    origin_node: str
    destination_node: Optional[str]
    final_market_node: Optional[str]
    quantity_cpu: float
    uom: Optional[str]
    created_time_bucket: str
    requested_arrival_time_bucket: Optional[str]
    priority_class: Optional[str]
    service_class: Optional[str]
    routing_group: Optional[str]
    cost_class: Optional[str]
    ownership_node: Optional[str]
    status: Optional[str]
    attributes_json: Optional[str]


@dataclass(frozen=True)
class DemandRecord:
    demand_id: str
    scenario_id: str
    market_id: str
    product_id: str
    time_bucket: str
    quantity_cpu: float
    price: Optional[float]
    channel_id: Optional[str]
    attributes_json: Optional[str]


@dataclass(frozen=True)
class FlowEventRecord:
    flow_id: str
    scenario_id: str
    session_id: Optional[str]
    iteration_no: Optional[int]
    lot_id: str
    event_type: str
    product_id: str
    from_node: Optional[str]
    to_node: Optional[str]
    time_bucket: str
    quantity_cpu: float
    creation_sequence: int
    event_priority: Optional[int] = None
    causal_event_id: Optional[str] = None
    operator_id: Optional[str] = None
    source_type: Optional[str] = None
    status: Optional[str] = None
    metadata_json: Optional[str] = None


@dataclass(frozen=True)
class TrustEventRecord:
    trust_event_id: str
    scenario_id: str
    session_id: Optional[str]
    iteration_no: Optional[int]
    event_type: str
    severity: float
    node_id: Optional[str]
    product_id: Optional[str]
    time_bucket: str
    message: str
    evidence_json: Optional[str] = None


@dataclass(frozen=True)
class OperatorActionRecord:
    operator_id: str
    scenario_id: str
    session_id: Optional[str]
    iteration_no: Optional[int]
    operator_type: str
    target_json: str
    parameters_json: str
    rationale: Optional[str] = None
    selected_flag: int = 1


class WOMSQLiteRepository:
    def __init__(self, db_path: str | Path) -> None:
        self.db_path = str(db_path)

    def connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def executescript(self, sql_text: str) -> None:
        with self.connect() as conn:
            conn.executescript(sql_text)
            conn.commit()

    def insert_scenario(
        self,
        scenario_id: str,
        scenario_name: str,
        scenario_type: Optional[str] = None,
        description: Optional[str] = None,
        version_label: Optional[str] = None,
        status: str = "active",
        created_by: Optional[str] = None,
        parent_scenario_id: Optional[str] = None,
    ) -> None:
        now = utc_now_iso()
        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO sc_scenario (
                    scenario_id, scenario_name, scenario_type, parent_scenario_id,
                    description, version_label, status, created_by, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    scenario_id,
                    scenario_name,
                    scenario_type,
                    parent_scenario_id,
                    description,
                    version_label,
                    status,
                    created_by,
                    now,
                    now,
                ),
            )
            conn.commit()

    def insert_lots(self, lots: Iterable[LotRecord]) -> None:
        now = utc_now_iso()
        rows = [
            (
                l.lot_id,
                l.scenario_id,
                l.lot_type,
                l.product_id,
                l.origin_node,
                l.destination_node,
                l.final_market_node,
                l.quantity_cpu,
                l.uom,
                l.created_time_bucket,
                l.requested_arrival_time_bucket,
                l.priority_class,
                l.service_class,
                l.routing_group,
                l.cost_class,
                l.ownership_node,
                l.status,
                l.attributes_json,
                now,
                now,
            )
            for l in lots
        ]
        with self.connect() as conn:
            conn.executemany(
                """
                INSERT INTO sc_lot (
                    lot_id, scenario_id, lot_type, product_id, origin_node, destination_node,
                    final_market_node, quantity_cpu, uom, created_time_bucket,
                    requested_arrival_time_bucket, priority_class, service_class, routing_group,
                    cost_class, ownership_node, status, attributes_json, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                rows,
            )
            conn.commit()

    def insert_demands(self, demands: Iterable[DemandRecord]) -> None:
        now = utc_now_iso()
        rows = [
            (
                d.demand_id,
                d.scenario_id,
                d.market_id,
                d.product_id,
                d.time_bucket,
                d.quantity_cpu,
                d.price,
                d.channel_id,
                d.attributes_json,
                now,
                now,
            )
            for d in demands
        ]
        with self.connect() as conn:
            conn.executemany(
                """
                INSERT INTO sc_demand_event (
                    demand_id, scenario_id, market_id, product_id, time_bucket,
                    quantity_cpu, price, channel_id, attributes_json, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                rows,
            )
            conn.commit()

    def create_session(
        self,
        session_id: str,
        scenario_id: str,
        engine_version: str,
        kernel_version: str,
        status: str = "running",
        initiated_by: Optional[str] = None,
        notes: Optional[str] = None,
        policy_set_id: Optional[str] = None,
        plugin_set_id: Optional[str] = None,
    ) -> None:
        started_at = utc_now_iso()
        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO run_planning_session (
                    session_id, scenario_id, engine_version, kernel_version,
                    policy_set_id, plugin_set_id, started_at, completed_at,
                    status, initiated_by, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    session_id,
                    scenario_id,
                    engine_version,
                    kernel_version,
                    policy_set_id,
                    plugin_set_id,
                    started_at,
                    None,
                    status,
                    initiated_by,
                    notes,
                ),
            )
            conn.commit()

    def complete_session(self, session_id: str, status: str = "completed") -> None:
        completed_at = utc_now_iso()
        with self.connect() as conn:
            conn.execute(
                """
                UPDATE run_planning_session
                   SET status = ?, completed_at = ?
                 WHERE session_id = ?
                """,
                (status, completed_at, session_id),
            )
            conn.commit()

    def insert_flow_events(self, events: Iterable[FlowEventRecord]) -> None:
        now = utc_now_iso()
        rows = [
            (
                e.flow_id,
                e.scenario_id,
                e.session_id,
                e.iteration_no,
                e.lot_id,
                e.event_type,
                e.product_id,
                e.from_node,
                e.to_node,
                e.time_bucket,
                e.quantity_cpu,
                e.creation_sequence,
                e.event_priority,
                e.causal_event_id,
                e.operator_id,
                e.source_type,
                e.status,
                e.metadata_json,
                now,
            )
            for e in events
        ]
        with self.connect() as conn:
            conn.executemany(
                """
                INSERT INTO ev_flow_event (
                    flow_id, scenario_id, session_id, iteration_no, lot_id,
                    event_type, product_id, from_node, to_node, time_bucket,
                    quantity_cpu, creation_sequence, event_priority,
                    causal_event_id, operator_id, source_type, status,
                    metadata_json, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                rows,
            )
            conn.commit()

    def insert_trust_events(self, events: Iterable[TrustEventRecord]) -> None:
        now = utc_now_iso()
        rows = [
            (
                e.trust_event_id,
                e.scenario_id,
                e.session_id,
                e.iteration_no,
                e.event_type,
                e.severity,
                e.node_id,
                e.product_id,
                e.time_bucket,
                e.message,
                e.evidence_json,
                now,
            )
            for e in events
        ]
        with self.connect() as conn:
            conn.executemany(
                """
                INSERT INTO ev_trust_event (
                    trust_event_id, scenario_id, session_id, iteration_no,
                    event_type, severity, node_id, product_id, time_bucket,
                    message, evidence_json, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                rows,
            )
            conn.commit()

    def insert_operator_actions(self, actions: Iterable[OperatorActionRecord]) -> None:
        now = utc_now_iso()
        rows = [
            (
                a.operator_id,
                a.scenario_id,
                a.session_id,
                a.iteration_no,
                a.operator_type,
                a.target_json,
                a.parameters_json,
                a.rationale,
                a.selected_flag,
                now,
            )
            for a in actions
        ]
        with self.connect() as conn:
            conn.executemany(
                """
                INSERT INTO ev_operator_action (
                    operator_id, scenario_id, session_id, iteration_no,
                    operator_type, target_json, parameters_json, rationale,
                    selected_flag, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                rows,
            )
            conn.commit()

    def insert_iteration_history(
        self,
        iteration_history_id: str,
        session_id: str,
        iteration_no: int,
        evaluation_score: Optional[float],
        service_level: Optional[float],
        inventory_penalty: Optional[float],
        risk_penalty: Optional[float],
        selected_operator_id: Optional[str],
        trust_event_count: Optional[int],
        notes: Optional[str],
    ) -> None:
        now = utc_now_iso()
        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO run_iteration_history (
                    iteration_history_id, session_id, iteration_no,
                    evaluation_score, service_level, inventory_penalty,
                    risk_penalty, selected_operator_id, trust_event_count,
                    notes, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    iteration_history_id,
                    session_id,
                    iteration_no,
                    evaluation_score,
                    service_level,
                    inventory_penalty,
                    risk_penalty,
                    selected_operator_id,
                    trust_event_count,
                    notes,
                    now,
                ),
            )
            conn.commit()

    def load_scenario_lots(self, scenario_id: str) -> List[sqlite3.Row]:
        with self.connect() as conn:
            cur = conn.execute(
                """
                SELECT *
                  FROM sc_lot
                 WHERE scenario_id = ?
                 ORDER BY created_time_bucket, lot_id
                """,
                (scenario_id,),
            )
            return cur.fetchall()

    def load_scenario_demands(self, scenario_id: str) -> List[sqlite3.Row]:
        with self.connect() as conn:
            cur = conn.execute(
                """
                SELECT *
                  FROM sc_demand_event
                 WHERE scenario_id = ?
                 ORDER BY time_bucket, market_id, product_id, demand_id
                """,
                (scenario_id,),
            )
            return cur.fetchall()

    def load_flow_events_for_replay(
        self,
        scenario_id: str,
        session_id: Optional[str] = None,
        upto_iteration: Optional[int] = None,
    ) -> List[sqlite3.Row]:
        sql = """
            SELECT *
              FROM ev_flow_event
             WHERE scenario_id = ?
        """
        params: List[Any] = [scenario_id]

        if session_id is not None:
            sql += " AND session_id = ?"
            params.append(session_id)

        if upto_iteration is not None:
            sql += " AND COALESCE(iteration_no, 0) <= ?"
            params.append(upto_iteration)

        sql += """
             ORDER BY
                 time_bucket,
                 COALESCE(event_priority, 999),
                 creation_sequence,
                 flow_id
        """

        with self.connect() as conn:
            cur = conn.execute(sql, params)
            return cur.fetchall()

    def load_trust_events(
        self,
        scenario_id: str,
        session_id: Optional[str] = None,
    ) -> List[sqlite3.Row]:
        sql = """
            SELECT *
              FROM ev_trust_event
             WHERE scenario_id = ?
        """
        params: List[Any] = [scenario_id]

        if session_id is not None:
            sql += " AND session_id = ?"
            params.append(session_id)

        sql += """
             ORDER BY
                 COALESCE(iteration_no, 0),
                 time_bucket,
                 trust_event_id
        """

        with self.connect() as conn:
            cur = conn.execute(sql, params)
            return cur.fetchall()

    def load_operator_actions(
        self,
        scenario_id: str,
        session_id: Optional[str] = None,
    ) -> List[sqlite3.Row]:
        sql = """
            SELECT *
              FROM ev_operator_action
             WHERE scenario_id = ?
        """
        params: List[Any] = [scenario_id]

        if session_id is not None:
            sql += " AND session_id = ?"
            params.append(session_id)

        sql += " ORDER BY COALESCE(iteration_no, 0), created_at, operator_id"

        with self.connect() as conn:
            cur = conn.execute(sql, params)
            return cur.fetchall()

    def get_iteration_history(self, session_id: str) -> List[sqlite3.Row]:
        with self.connect() as conn:
            cur = conn.execute(
                """
                SELECT *
                  FROM run_iteration_history
                 WHERE session_id = ?
                 ORDER BY iteration_no
                """,
                (session_id,),
            )
            return cur.fetchall()

    def fetch_demand_vs_sales(self, scenario_id: str) -> List[sqlite3.Row]:
        with self.connect() as conn:
            cur = conn.execute(
                """
                SELECT
                    d.market_id,
                    d.product_id,
                    d.time_bucket,
                    d.quantity_cpu AS demand_cpu,
                    COALESCE(SUM(s.quantity_cpu), 0) AS sold_cpu,
                    d.quantity_cpu - COALESCE(SUM(s.quantity_cpu), 0) AS backlog_cpu
                FROM sc_demand_event d
                LEFT JOIN ev_sale_event s
                  ON d.scenario_id = s.scenario_id
                 AND d.market_id = s.market_id
                 AND d.product_id = s.product_id
                 AND d.time_bucket = s.time_bucket
                WHERE d.scenario_id = ?
                GROUP BY
                    d.market_id,
                    d.product_id,
                    d.time_bucket,
                    d.quantity_cpu
                ORDER BY
                    d.time_bucket,
                    d.market_id,
                    d.product_id
                """,
                (scenario_id,),
            )
            return cur.fetchall()

    def as_dicts(self, rows: Iterable[sqlite3.Row]) -> List[Dict[str, Any]]:
        return [dict(r) for r in rows]


def json_dumps(data: Dict[str, Any]) -> str:
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))


if __name__ == "__main__":
    repo = WOMSQLiteRepository("wom_demo.sqlite")

    replay_rows = repo.load_flow_events_for_replay(
        scenario_id="sc-demo-phone-jp-v1",
        session_id="sess-demo-001",
    )

    print("=== Replay Events ===")
    for row in replay_rows:
        print(
            row["time_bucket"],
            row["event_type"],
            row["flow_id"],
            row["from_node"],
            "->",
            row["to_node"],
            row["quantity_cpu"],
        )

    print("\n=== Trust Events ===")
    for row in repo.load_trust_events("sc-demo-phone-jp-v1", "sess-demo-001"):
        print(row["iteration_no"], row["event_type"], row["message"])

    print("\n=== Iteration History ===")
    for row in repo.get_iteration_history("sess-demo-001"):
        print(
            row["iteration_no"],
            row["evaluation_score"],
            row["service_level"],
            row["selected_operator_id"],
        )