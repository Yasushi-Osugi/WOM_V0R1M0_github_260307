----------------------------------------------------------------
-- Q1. Canonical replay order for a scenario/session
----------------------------------------------------------------
SELECT
    flow_id,
    lot_id,
    event_type,
    product_id,
    from_node,
    to_node,
    time_bucket,
    quantity_cpu,
    COALESCE(event_priority, 999) AS replay_event_priority,
    creation_sequence,
    operator_id,
    source_type
FROM ev_flow_event
WHERE scenario_id = 'sc-demo-phone-jp-v1'
  AND session_id = 'sess-demo-001'
ORDER BY
    time_bucket,
    COALESCE(event_priority, 999),
    creation_sequence,
    flow_id;

----------------------------------------------------------------
-- Q2. Replay order by iteration
----------------------------------------------------------------
SELECT
    iteration_no,
    flow_id,
    event_type,
    product_id,
    from_node,
    to_node,
    time_bucket,
    quantity_cpu,
    creation_sequence,
    operator_id
FROM ev_flow_event
WHERE scenario_id = 'sc-demo-phone-jp-v1'
  AND session_id = 'sess-demo-001'
ORDER BY
    iteration_no,
    time_bucket,
    COALESCE(event_priority, 999),
    creation_sequence,
    flow_id;

----------------------------------------------------------------
-- Q3. All trust events for a session
----------------------------------------------------------------
SELECT
    iteration_no,
    trust_event_id,
    event_type,
    severity,
    node_id,
    product_id,
    time_bucket,
    message
FROM ev_trust_event
WHERE scenario_id = 'sc-demo-phone-jp-v1'
  AND session_id = 'sess-demo-001'
ORDER BY
    iteration_no,
    time_bucket,
    trust_event_id;

----------------------------------------------------------------
-- Q4. Selected operator history
----------------------------------------------------------------
SELECT
    operator_id,
    iteration_no,
    operator_type,
    target_json,
    parameters_json,
    rationale,
    selected_flag,
    created_at
FROM ev_operator_action
WHERE scenario_id = 'sc-demo-phone-jp-v1'
  AND session_id = 'sess-demo-001'
ORDER BY
    iteration_no,
    created_at;

----------------------------------------------------------------
-- Q5. Iteration summary
----------------------------------------------------------------
SELECT
    iteration_no,
    evaluation_score,
    service_level,
    inventory_penalty,
    risk_penalty,
    selected_operator_id,
    trust_event_count,
    notes
FROM run_iteration_history
WHERE session_id = 'sess-demo-001'
ORDER BY iteration_no;

----------------------------------------------------------------
-- Q6. Sale analytics
----------------------------------------------------------------
SELECT
    sale_id,
    market_id,
    product_id,
    time_bucket,
    quantity_cpu,
    price,
    revenue_amount
FROM ev_sale_event
WHERE scenario_id = 'sc-demo-phone-jp-v1'
ORDER BY
    time_bucket,
    market_id,
    product_id;

----------------------------------------------------------------
-- Q7. Lot genealogy / event chain
----------------------------------------------------------------
SELECT
    lot_id,
    flow_id,
    event_type,
    from_node,
    to_node,
    time_bucket,
    quantity_cpu,
    creation_sequence,
    causal_event_id
FROM ev_flow_event
WHERE lot_id = 'lot-202611-P1-0001'
ORDER BY
    time_bucket,
    COALESCE(event_priority, 999),
    creation_sequence,
    flow_id;

----------------------------------------------------------------
-- Q8. Scenario demand vs sales
----------------------------------------------------------------
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
WHERE d.scenario_id = 'sc-demo-phone-jp-v1'
GROUP BY
    d.market_id,
    d.product_id,
    d.time_bucket,
    d.quantity_cpu
ORDER BY
    d.time_bucket,
    d.market_id,
    d.product_id;