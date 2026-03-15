PRAGMA foreign_keys = ON;

----------------------------------------------------------------
-- 1. Scenario Master
----------------------------------------------------------------

CREATE TABLE IF NOT EXISTS sc_scenario (
    scenario_id           TEXT PRIMARY KEY,
    scenario_name         TEXT NOT NULL,
    scenario_type         TEXT,
    parent_scenario_id    TEXT,
    description           TEXT,
    version_label         TEXT,
    status                TEXT DEFAULT 'active',
    created_by            TEXT,
    created_at            TEXT NOT NULL,
    updated_at            TEXT NOT NULL,
    FOREIGN KEY (parent_scenario_id) REFERENCES sc_scenario (scenario_id)
);

CREATE INDEX IF NOT EXISTS idx_sc_scenario_type
    ON sc_scenario (scenario_type);

CREATE INDEX IF NOT EXISTS idx_sc_scenario_status
    ON sc_scenario (status);

----------------------------------------------------------------
-- 2. Lot Header Persistence
----------------------------------------------------------------

CREATE TABLE IF NOT EXISTS sc_lot (
    lot_id                           TEXT PRIMARY KEY,
    scenario_id                      TEXT NOT NULL,
    lot_type                         TEXT,
    product_id                       TEXT NOT NULL,
    origin_node                      TEXT NOT NULL,
    destination_node                 TEXT,
    final_market_node                TEXT,
    quantity_cpu                     REAL NOT NULL CHECK (quantity_cpu >= 0),
    uom                              TEXT,
    created_time_bucket              TEXT NOT NULL,
    requested_arrival_time_bucket    TEXT,
    priority_class                   TEXT,
    service_class                    TEXT,
    routing_group                    TEXT,
    cost_class                       TEXT,
    ownership_node                   TEXT,
    status                           TEXT,
    attributes_json                  TEXT,
    created_at                       TEXT NOT NULL,
    updated_at                       TEXT NOT NULL,
    FOREIGN KEY (scenario_id) REFERENCES sc_scenario (scenario_id)
);

CREATE INDEX IF NOT EXISTS idx_sc_lot_scenario
    ON sc_lot (scenario_id);

CREATE INDEX IF NOT EXISTS idx_sc_lot_product
    ON sc_lot (product_id);

CREATE INDEX IF NOT EXISTS idx_sc_lot_origin_dest
    ON sc_lot (origin_node, destination_node);

CREATE INDEX IF NOT EXISTS idx_sc_lot_created_bucket
    ON sc_lot (created_time_bucket);

----------------------------------------------------------------
-- 3. Demand Scenario Input
----------------------------------------------------------------

CREATE TABLE IF NOT EXISTS sc_demand_event (
    demand_id              TEXT PRIMARY KEY,
    scenario_id            TEXT NOT NULL,
    market_id              TEXT NOT NULL,
    product_id             TEXT NOT NULL,
    time_bucket            TEXT NOT NULL,
    quantity_cpu           REAL NOT NULL CHECK (quantity_cpu >= 0),
    price                  REAL,
    channel_id             TEXT,
    attributes_json        TEXT,
    created_at             TEXT NOT NULL,
    updated_at             TEXT NOT NULL,
    FOREIGN KEY (scenario_id) REFERENCES sc_scenario (scenario_id)
);

CREATE INDEX IF NOT EXISTS idx_sc_demand_event_scenario_time
    ON sc_demand_event (scenario_id, time_bucket);

CREATE INDEX IF NOT EXISTS idx_sc_demand_event_market_product_time
    ON sc_demand_event (market_id, product_id, time_bucket);

----------------------------------------------------------------
-- 4. Planning Session
----------------------------------------------------------------

CREATE TABLE IF NOT EXISTS run_planning_session (
    session_id             TEXT PRIMARY KEY,
    scenario_id            TEXT NOT NULL,
    engine_version         TEXT,
    kernel_version         TEXT,
    policy_set_id          TEXT,
    plugin_set_id          TEXT,
    started_at             TEXT NOT NULL,
    completed_at           TEXT,
    status                 TEXT NOT NULL,
    initiated_by           TEXT,
    notes                  TEXT,
    FOREIGN KEY (scenario_id) REFERENCES sc_scenario (scenario_id)
);

CREATE INDEX IF NOT EXISTS idx_run_planning_session_scenario
    ON run_planning_session (scenario_id);

CREATE INDEX IF NOT EXISTS idx_run_planning_session_status
    ON run_planning_session (status);

----------------------------------------------------------------
-- 5. Core Event Store
----------------------------------------------------------------

CREATE TABLE IF NOT EXISTS ev_flow_event (
    flow_id                TEXT PRIMARY KEY,
    scenario_id            TEXT NOT NULL,
    session_id             TEXT,
    iteration_no           INTEGER,
    lot_id                 TEXT NOT NULL,
    event_type             TEXT NOT NULL,
    product_id             TEXT NOT NULL,
    from_node              TEXT,
    to_node                TEXT,
    time_bucket            TEXT NOT NULL,
    quantity_cpu           REAL NOT NULL CHECK (quantity_cpu >= 0),
    creation_sequence      INTEGER NOT NULL,
    event_priority         INTEGER,
    causal_event_id        TEXT,
    operator_id            TEXT,
    source_type            TEXT,
    status                 TEXT,
    metadata_json          TEXT,
    created_at             TEXT NOT NULL,
    FOREIGN KEY (scenario_id) REFERENCES sc_scenario (scenario_id),
    FOREIGN KEY (session_id) REFERENCES run_planning_session (session_id),
    FOREIGN KEY (lot_id) REFERENCES sc_lot (lot_id),
    FOREIGN KEY (causal_event_id) REFERENCES ev_flow_event (flow_id),
    CHECK (
        event_type IN (
            'production',
            'shipment',
            'arrival',
            'sale',
            'inventory_adjustment'
        )
    )
);

CREATE INDEX IF NOT EXISTS idx_ev_flow_event_scenario_time
    ON ev_flow_event (scenario_id, time_bucket, creation_sequence, flow_id);

CREATE INDEX IF NOT EXISTS idx_ev_flow_event_session_iteration
    ON ev_flow_event (session_id, iteration_no);

CREATE INDEX IF NOT EXISTS idx_ev_flow_event_lot
    ON ev_flow_event (lot_id);

CREATE INDEX IF NOT EXISTS idx_ev_flow_event_product_time
    ON ev_flow_event (product_id, time_bucket);

CREATE INDEX IF NOT EXISTS idx_ev_flow_event_type_time
    ON ev_flow_event (event_type, time_bucket);

CREATE INDEX IF NOT EXISTS idx_ev_flow_event_operator
    ON ev_flow_event (operator_id);

----------------------------------------------------------------
-- 6. Trust Event Store
----------------------------------------------------------------

CREATE TABLE IF NOT EXISTS ev_trust_event (
    trust_event_id         TEXT PRIMARY KEY,
    scenario_id            TEXT NOT NULL,
    session_id             TEXT,
    iteration_no           INTEGER,
    event_type             TEXT NOT NULL,
    severity               REAL NOT NULL,
    node_id                TEXT,
    product_id             TEXT,
    time_bucket            TEXT NOT NULL,
    message                TEXT NOT NULL,
    evidence_json          TEXT,
    created_at             TEXT NOT NULL,
    FOREIGN KEY (scenario_id) REFERENCES sc_scenario (scenario_id),
    FOREIGN KEY (session_id) REFERENCES run_planning_session (session_id)
);

CREATE INDEX IF NOT EXISTS idx_ev_trust_event_scenario_time
    ON ev_trust_event (scenario_id, time_bucket);

CREATE INDEX IF NOT EXISTS idx_ev_trust_event_session_iteration
    ON ev_trust_event (session_id, iteration_no);

CREATE INDEX IF NOT EXISTS idx_ev_trust_event_type_time
    ON ev_trust_event (event_type, time_bucket);

----------------------------------------------------------------
-- 7. Operator Action Log
----------------------------------------------------------------

CREATE TABLE IF NOT EXISTS ev_operator_action (
    operator_id            TEXT PRIMARY KEY,
    scenario_id            TEXT NOT NULL,
    session_id             TEXT,
    iteration_no           INTEGER,
    operator_type          TEXT NOT NULL,
    target_json            TEXT NOT NULL,
    parameters_json        TEXT NOT NULL,
    rationale              TEXT,
    selected_flag          INTEGER NOT NULL DEFAULT 1 CHECK (selected_flag IN (0, 1)),
    created_at             TEXT NOT NULL,
    FOREIGN KEY (scenario_id) REFERENCES sc_scenario (scenario_id),
    FOREIGN KEY (session_id) REFERENCES run_planning_session (session_id)
);

CREATE INDEX IF NOT EXISTS idx_ev_operator_action_session_iteration
    ON ev_operator_action (session_id, iteration_no);

CREATE INDEX IF NOT EXISTS idx_ev_operator_action_type
    ON ev_operator_action (operator_type);

----------------------------------------------------------------
-- 8. Iteration History
----------------------------------------------------------------

CREATE TABLE IF NOT EXISTS run_iteration_history (
    iteration_history_id   TEXT PRIMARY KEY,
    session_id             TEXT NOT NULL,
    iteration_no           INTEGER NOT NULL,
    evaluation_score       REAL,
    service_level          REAL,
    inventory_penalty      REAL,
    risk_penalty           REAL,
    selected_operator_id   TEXT,
    trust_event_count      INTEGER,
    notes                  TEXT,
    created_at             TEXT NOT NULL,
    FOREIGN KEY (session_id) REFERENCES run_planning_session (session_id),
    FOREIGN KEY (selected_operator_id) REFERENCES ev_operator_action (operator_id),
    UNIQUE (session_id, iteration_no)
);

CREATE INDEX IF NOT EXISTS idx_run_iteration_history_session
    ON run_iteration_history (session_id, iteration_no);

----------------------------------------------------------------
-- 9. Optional Sale Analytics Table
--    Canonical runtime truth remains ev_flow_event(event_type='sale')
----------------------------------------------------------------

CREATE TABLE IF NOT EXISTS ev_sale_event (
    sale_id                TEXT PRIMARY KEY,
    flow_id                TEXT NOT NULL UNIQUE,
    scenario_id            TEXT NOT NULL,
    session_id             TEXT,
    iteration_no           INTEGER,
    market_id              TEXT NOT NULL,
    product_id             TEXT NOT NULL,
    time_bucket            TEXT NOT NULL,
    quantity_cpu           REAL NOT NULL CHECK (quantity_cpu >= 0),
    source_node            TEXT NOT NULL,
    demand_id              TEXT,
    price                  REAL,
    revenue_amount         REAL,
    metadata_json          TEXT,
    created_at             TEXT NOT NULL,
    FOREIGN KEY (flow_id) REFERENCES ev_flow_event (flow_id),
    FOREIGN KEY (scenario_id) REFERENCES sc_scenario (scenario_id),
    FOREIGN KEY (session_id) REFERENCES run_planning_session (session_id),
    FOREIGN KEY (demand_id) REFERENCES sc_demand_event (demand_id)
);

CREATE INDEX IF NOT EXISTS idx_ev_sale_event_scenario_time
    ON ev_sale_event (scenario_id, time_bucket);

CREATE INDEX IF NOT EXISTS idx_ev_sale_event_market_product_time
    ON ev_sale_event (market_id, product_id, time_bucket);

----------------------------------------------------------------
-- 10. Derived Snapshot Tables
--     These are derived caches, not source of truth.
----------------------------------------------------------------

CREATE TABLE IF NOT EXISTS st_inventory_snapshot (
    inventory_snapshot_id  TEXT PRIMARY KEY,
    scenario_id            TEXT NOT NULL,
    session_id             TEXT,
    iteration_no           INTEGER,
    node_id                TEXT NOT NULL,
    product_id             TEXT NOT NULL,
    time_bucket            TEXT NOT NULL,
    inventory_cpu          REAL NOT NULL,
    created_at             TEXT NOT NULL,
    FOREIGN KEY (scenario_id) REFERENCES sc_scenario (scenario_id),
    FOREIGN KEY (session_id) REFERENCES run_planning_session (session_id),
    UNIQUE (scenario_id, session_id, iteration_no, node_id, product_id, time_bucket)
);

CREATE INDEX IF NOT EXISTS idx_st_inventory_snapshot_lookup
    ON st_inventory_snapshot (scenario_id, session_id, iteration_no, node_id, product_id, time_bucket);

CREATE TABLE IF NOT EXISTS st_backlog_snapshot (
    backlog_snapshot_id    TEXT PRIMARY KEY,
    scenario_id            TEXT NOT NULL,
    session_id             TEXT,
    iteration_no           INTEGER,
    market_id              TEXT NOT NULL,
    product_id             TEXT NOT NULL,
    time_bucket            TEXT NOT NULL,
    backlog_cpu            REAL NOT NULL,
    created_at             TEXT NOT NULL,
    FOREIGN KEY (scenario_id) REFERENCES sc_scenario (scenario_id),
    FOREIGN KEY (session_id) REFERENCES run_planning_session (session_id),
    UNIQUE (scenario_id, session_id, iteration_no, market_id, product_id, time_bucket)
);

CREATE INDEX IF NOT EXISTS idx_st_backlog_snapshot_lookup
    ON st_backlog_snapshot (scenario_id, session_id, iteration_no, market_id, product_id, time_bucket);

CREATE TABLE IF NOT EXISTS st_capacity_snapshot (
    capacity_snapshot_id   TEXT PRIMARY KEY,
    scenario_id            TEXT NOT NULL,
    session_id             TEXT,
    iteration_no           INTEGER,
    resource_id            TEXT NOT NULL,
    time_bucket            TEXT NOT NULL,
    capacity_used_cpu      REAL NOT NULL,
    capacity_limit_cpu     REAL,
    created_at             TEXT NOT NULL,
    FOREIGN KEY (scenario_id) REFERENCES sc_scenario (scenario_id),
    FOREIGN KEY (session_id) REFERENCES run_planning_session (session_id),
    UNIQUE (scenario_id, session_id, iteration_no, resource_id, time_bucket)
);

CREATE INDEX IF NOT EXISTS idx_st_capacity_snapshot_lookup
    ON st_capacity_snapshot (scenario_id, session_id, iteration_no, resource_id, time_bucket);

----------------------------------------------------------------
-- 11. Helpful Replay View
----------------------------------------------------------------

CREATE VIEW IF NOT EXISTS vw_ev_flow_event_replay AS
SELECT
    flow_id,
    scenario_id,
    session_id,
    iteration_no,
    lot_id,
    event_type,
    product_id,
    from_node,
    to_node,
    time_bucket,
    quantity_cpu,
    creation_sequence,
    COALESCE(event_priority, 999) AS replay_event_priority,
    causal_event_id,
    operator_id,
    source_type,
    status,
    metadata_json,
    created_at
FROM ev_flow_event;

----------------------------------------------------------------
-- 12. Helpful Comments / Usage Notes
----------------------------------------------------------------
-- Canonical replay ordering:
-- ORDER BY
--   time_bucket,
--   COALESCE(event_priority, 999),
--   creation_sequence,
--   flow_id;
--
-- Source of truth:
--   sc_lot
--   sc_demand_event
--   ev_flow_event
--   ev_trust_event
--   ev_operator_action
--
-- Derived/cache tables:
--   st_inventory_snapshot
--   st_backlog_snapshot
--   st_capacity_snapshot
--
-- Recommendation:
--   treat ev_flow_event as append-only as much as possible.