# pysi/apps/wom_visualizer_app.py

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from dash import Dash, Input, Output, State, dcc, html, dash_table
import plotly.graph_objects as go

from visualization.app_service import build_demo_runtime
from visualization.viewmodels import (
    EdgeViewModel,
    EventRowViewModel,
    LotViewModel,
    NodeViewModel,
    PSIViewModel,
)


# ============================================================
# Runtime bootstrap
# ============================================================

runtime = build_demo_runtime()
snapshots = runtime["snapshots"]
time_buckets = runtime["time_buckets"]

DEFAULT_NODE_ID = "market_TYO"
DEFAULT_PRODUCT_ID = "P1"


# ============================================================
# Risk / Constraint Helpers
# ============================================================

def compute_node_risk_score(node: NodeViewModel) -> float:
    score = 0.0

    if node.shortage_flag:
        score += 100.0

    if node.overflow_flag:
        score += 70.0

    if node.inventory_qty < 20:
        score += 30.0

    if node.inventory_qty > 400:
        score += 20.0

    return score


def compute_edge_risk_score(edge: EdgeViewModel) -> float:
    ratio = edge.congestion_ratio

    if ratio >= 1.0:
        return 100.0
    if ratio >= 0.9:
        return 70.0
    if ratio >= 0.8:
        return 40.0
    return 0.0


def _node_border_color(node: NodeViewModel) -> str:
    if node.shortage_flag:
        return "#d62728"
    if node.overflow_flag:
        return "#9467bd"
    return "#222222"


def _node_border_width(node: NodeViewModel, selected_node_id: Optional[str] = None) -> float:
    risk = compute_node_risk_score(node)

    if node.node_id == selected_node_id:
        return 6.0
    if risk >= 70.0:
        return 5.0
    if risk > 0.0:
        return 3.0
    return 1.5


def _lot_color(lot: LotViewModel) -> str:
    if lot.status == "sold":
        return "#8c8c8c"
    if lot.age_weeks >= 4:
        return "#d62728"
    if lot.age_weeks >= 2:
        return "#ff7f0e"
    return "#111111"


# ============================================================
# Figure Builders
# ============================================================

def _node_marker_size(inv: float) -> float:
    return 18.0 + max(inv / 10.0, 0.0)


def _edge_line_width(flow_qty: float) -> float:
    return 1.5 + max(flow_qty / 20.0, 0.0)


def _edge_color(congestion_ratio: float) -> str:
    if congestion_ratio >= 1.0:
        return "#d62728"
    if congestion_ratio >= 0.8:
        return "#ff7f0e"
    return "#7f7f7f"


def _node_color(node: NodeViewModel) -> str:
    if node.shortage_flag:
        return "#d62728"
    if node.overflow_flag:
        return "#9467bd"
    if node.node_type == "factory":
        return "#1f77b4"
    if node.node_type == "dc":
        return "#2ca02c"
    return "#17becf"


def build_network_figure(
    nodes: List[NodeViewModel],
    edges: List[EdgeViewModel],
    lots: List[LotViewModel],
    selected_node_id: Optional[str] = None,
    selected_lot_id: Optional[str] = None,
) -> go.Figure:
    fig = go.Figure()
    node_map = {n.node_id: n for n in nodes}
    edge_map = {e.edge_id: e for e in edges}

    for edge in edges:
        src = node_map[edge.from_node]
        dst = node_map[edge.to_node]
        fig.add_trace(
            go.Scatter(
                x=[src.x, dst.x],
                y=[src.y, dst.y],
                mode="lines",
                line={
                    "width": _edge_line_width(edge.flow_qty),
                    "color": _edge_color(edge.congestion_ratio),
                },
                hoverinfo="text",
                hovertext=(
                    f"{edge.edge_id}"
                    f"<br>flow={edge.flow_qty:.1f}"
                    f"<br>capacity={edge.capacity:.1f}"
                    f"<br>congestion={edge.congestion_ratio:.2f}"
                    f"<br>risk_score={compute_edge_risk_score(edge):.1f}"
                ),
                showlegend=False,
            )
        )

    node_sizes = [_node_marker_size(n.inventory_qty) for n in nodes]
    node_colors = [_node_color(n) for n in nodes]
    node_line_widths = [_node_border_width(n, selected_node_id) for n in nodes]
    node_line_colors = [_node_border_color(n) for n in nodes]

    fig.add_trace(
        go.Scatter(
            x=[n.x for n in nodes],
            y=[n.y for n in nodes],
            mode="markers+text",
            text=[n.node_id for n in nodes],
            textposition="top center",
            customdata=[[n.node_id, "node"] for n in nodes],
            marker={
                "size": node_sizes,
                "color": node_colors,
                "line": {"width": node_line_widths, "color": node_line_colors},
            },
            hoverinfo="text",
            hovertext=[
                f"{n.node_id}"
                f"<br>type={n.node_type}"
                f"<br>inventory={n.inventory_qty:.1f}"
                f"<br>sales={n.sales_qty:.1f}"
                f"<br>risk_score={compute_node_risk_score(n):.1f}"
                for n in nodes
            ],
            name="Nodes",
        )
    )

    lot_x: List[float] = []
    lot_y: List[float] = []
    lot_text: List[str] = []
    lot_sizes: List[float] = []
    lot_outline: List[float] = []
    lot_colors: List[str] = []
    lot_customdata: List[List[str]] = []

    for lot in lots:
        if lot.status == "sold":
            # sold lots are not shown on the network
            continue

        if lot.current_edge and lot.current_edge in edge_map:
            edge = edge_map[lot.current_edge]
            src = node_map[edge.from_node]
            dst = node_map[edge.to_node]
            x = src.x + (dst.x - src.x) * lot.progress
            y = src.y + (dst.y - src.y) * lot.progress
        elif lot.current_node and lot.current_node in node_map:
            n = node_map[lot.current_node]
            x = n.x
            y = n.y - 0.25
        else:
            continue

        lot_x.append(x)
        lot_y.append(y)
        lot_text.append(
            f"{lot.lot_id}"
            f"<br>product={lot.product_id}"
            f"<br>qty={lot.quantity_cpu:.1f}"
            f"<br>status={lot.status}"
            f"<br>age_weeks={lot.age_weeks}"
        )
        lot_sizes.append(10 + lot.quantity_cpu / 10.0)
        lot_outline.append(4 if lot.lot_id == selected_lot_id else 1.0)
        lot_colors.append(_lot_color(lot))
        lot_customdata.append([lot.lot_id, "lot"])

    fig.add_trace(
        go.Scatter(
            x=lot_x,
            y=lot_y,
            mode="markers",
            customdata=lot_customdata,
            marker={
                "size": lot_sizes,
                "symbol": "square",
                "line": {"width": lot_outline, "color": "#111"},
                "color": lot_colors,
            },
            hoverinfo="text",
            hovertext=lot_text,
            name="Lots",
        )
    )

    fig.update_layout(
        title="Network Flow View",
        height=500,
        margin=dict(l=20, r=20, t=45, b=20),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        plot_bgcolor="white",
        paper_bgcolor="white",
        clickmode="event+select",
    )
    return fig


def build_psi_figure(psi: PSIViewModel, current_time_bucket: str) -> go.Figure:
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=psi.weeks, y=psi.demand, mode="lines+markers", name="Demand"))
    fig.add_trace(go.Scatter(x=psi.weeks, y=psi.shipment, mode="lines+markers", name="Shipment"))
    fig.add_trace(go.Scatter(x=psi.weeks, y=psi.arrival, mode="lines+markers", name="Arrival"))
    fig.add_trace(go.Scatter(x=psi.weeks, y=psi.sales, mode="lines+markers", name="Sales"))
    fig.add_trace(go.Scatter(x=psi.weeks, y=psi.inventory, mode="lines+markers", name="Inventory"))
    fig.add_trace(go.Scatter(x=psi.weeks, y=psi.backlog, mode="lines+markers", name="Backlog"))

    if current_time_bucket in psi.weeks:
        fig.add_vline(
            x=current_time_bucket,
            line_width=2,
            line_dash="dash",
            line_color="black",
        )

    fig.update_layout(
        title=f"PSI Time View: {psi.node_id} / {psi.product_id}",
        height=320,
        margin=dict(l=40, r=20, t=45, b=40),
        paper_bgcolor="white",
        plot_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0.0),
    )
    return fig


def build_event_table(events: List[EventRowViewModel]) -> List[dict]:
    return [
        {
            "time_bucket": e.time_bucket,
            "event_type": e.event_type,
            "object_id": e.object_id,
            "node_id": e.node_id or "",
            "description": e.description,
        }
        for e in events
    ]


# ============================================================
# Detail Panel Builders
# ============================================================

def build_bottleneck_summary(snapshot: dict) -> html.Div:
    nodes = snapshot["nodes"]
    edges = snapshot["edges"]

    ranked_nodes = sorted(
        [(n.node_id, compute_node_risk_score(n)) for n in nodes],
        key=lambda x: x[1],
        reverse=True,
    )
    ranked_edges = sorted(
        [(e.edge_id, compute_edge_risk_score(e)) for e in edges],
        key=lambda x: x[1],
        reverse=True,
    )

    top_node_1 = ranked_nodes[0] if ranked_nodes else ("N/A", 0.0)
    top_node_2 = ranked_nodes[1] if len(ranked_nodes) > 1 else ("N/A", 0.0)
    top_edge_1 = ranked_edges[0] if ranked_edges else ("N/A", 0.0)

    return html.Div(
        [
            html.H4("Bottleneck Summary"),
            html.P(f"Top Node Risk: {top_node_1[0]} ({top_node_1[1]:.1f})"),
            html.P(f"2nd Node Risk: {top_node_2[0]} ({top_node_2[1]:.1f})"),
            html.P(f"Top Edge Risk: {top_edge_1[0]} ({top_edge_1[1]:.1f})"),
            html.Hr(),
        ]
    )


def _find_node(nodes: List[NodeViewModel], node_id: str) -> Optional[NodeViewModel]:
    for n in nodes:
        if n.node_id == node_id:
            return n
    return None


def _find_lot(lots: List[LotViewModel], lot_id: str) -> Optional[LotViewModel]:
    for lot in lots:
        if lot.lot_id == lot_id:
            return lot
    return None


def build_detail_panel(
    snapshot: dict,
    selected_node_id: Optional[str],
    selected_lot_id: Optional[str],
) -> html.Div:
    tb = snapshot["time_bucket"]
    kpis = snapshot["kpis"]
    nodes = snapshot["nodes"]
    lots = snapshot["lots"]

    bottleneck_summary = build_bottleneck_summary(snapshot)

    sections = [
        bottleneck_summary,
        html.H4("Detail Inspector"),
        html.P(f"Time Bucket: {tb}"),
        html.P(f"Inventory Total: {kpis['inventory_total']}"),
        html.P(f"Sales Total: {kpis['sales_total']}"),
        html.P(f"Backlog Total: {kpis['backlog_total']}"),
        html.Hr(),
    ]

    if selected_node_id:
        node = _find_node(nodes, selected_node_id)
        if node:
            sections.extend(
                [
                    html.H5("Selected Node"),
                    html.P(f"node_id: {node.node_id}"),
                    html.P(f"type: {node.node_type}"),
                    html.P(f"inventory_qty: {node.inventory_qty}"),
                    html.P(f"sales_qty: {node.sales_qty}"),
                    html.P(f"shortage_flag: {node.shortage_flag}"),
                    html.P(f"overflow_flag: {node.overflow_flag}"),
                    html.P(f"risk_score: {compute_node_risk_score(node):.1f}"),
                    html.Hr(),
                ]
            )

    if selected_lot_id:
        lot = _find_lot(lots, selected_lot_id)
        if lot:
            sections.extend(
                [
                    html.H5("Selected Lot"),
                    html.P(f"lot_id: {lot.lot_id}"),
                    html.P(f"product_id: {lot.product_id}"),
                    html.P(f"quantity_cpu: {lot.quantity_cpu}"),
                    html.P(f"status: {lot.status}"),
                    html.P(f"current_node: {lot.current_node}"),
                    html.P(f"current_edge: {lot.current_edge}"),
                    html.P(f"progress: {lot.progress:.2f}"),
                    html.P(f"age_weeks: {lot.age_weeks}"),
                    html.P(f"linked_demand_id: {lot.linked_demand_id}"),
                ]
            )

    if not selected_node_id and not selected_lot_id:
        sections.extend(
            [
                html.H5("Selection"),
                html.P("Click a node or lot in the network graph."),
            ]
        )

    return html.Div(sections)


# ============================================================
# Dash App
# ============================================================

app = Dash(__name__)
app.title = "WOM Visual Operating Console"

app.layout = html.Div(
    [
        html.H2("WOM Visual Operating Console"),
        html.Div(
            [
                html.Label("Time Bucket"),
                dcc.Slider(
                    id="time-slider",
                    min=0,
                    max=len(time_buckets) - 1,
                    step=1,
                    value=0,
                    marks={i: tb for i, tb in enumerate(time_buckets)},
                    updatemode="drag",
                ),
                html.Div(
                    [
                        html.Button("Play / Pause", id="play-button", n_clicks=0),
                        dcc.Interval(
                            id="play-interval",
                            interval=1200,
                            n_intervals=0,
                            disabled=True,
                        ),
                    ],
                    style={"marginTop": "10px"},
                ),
            ],
            style={"marginBottom": "20px"},
        ),
        dcc.Store(id="selected-node-store", data=DEFAULT_NODE_ID),
        dcc.Store(id="selected-lot-store", data=None),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="network-graph")],
                    style={
                        "width": "68%",
                        "display": "inline-block",
                        "verticalAlign": "top",
                    },
                ),
                html.Div(
                    [
                        html.Div(id="detail-panel", style={"marginBottom": "12px"}),
                        html.H4("Event Log"),
                        dash_table.DataTable(
                            id="event-table",
                            columns=[
                                {"name": "time_bucket", "id": "time_bucket"},
                                {"name": "event_type", "id": "event_type"},
                                {"name": "object_id", "id": "object_id"},
                                {"name": "node_id", "id": "node_id"},
                                {"name": "description", "id": "description"},
                            ],
                            data=[],
                            style_table={"overflowX": "auto"},
                            style_cell={
                                "textAlign": "left",
                                "fontSize": "12px",
                                "padding": "6px",
                                "whiteSpace": "normal",
                                "height": "auto",
                            },
                            style_header={"fontWeight": "bold"},
                            page_size=10,
                        ),
                    ],
                    style={
                        "width": "30%",
                        "display": "inline-block",
                        "verticalAlign": "top",
                        "paddingLeft": "20px",
                    },
                ),
            ]
        ),
        dcc.Graph(id="psi-graph"),
    ],
    style={"padding": "20px", "fontFamily": "Arial, sans-serif"},
)


# ============================================================
# Callbacks
# ============================================================

@app.callback(
    Output("play-interval", "disabled"),
    Input("play-button", "n_clicks"),
    State("play-interval", "disabled"),
    prevent_initial_call=True,
)
def toggle_play(_, disabled: bool) -> bool:
    return not disabled


@app.callback(
    Output("time-slider", "value"),
    Input("play-interval", "n_intervals"),
    State("play-interval", "disabled"),
    State("time-slider", "value"),
    prevent_initial_call=True,
)
def advance_time(_, disabled: bool, current_value: int) -> int:
    if disabled:
        return current_value
    next_value = current_value + 1
    if next_value > len(time_buckets) - 1:
        next_value = 0
    return next_value


@app.callback(
    Output("selected-node-store", "data"),
    Output("selected-lot-store", "data"),
    Input("network-graph", "clickData"),
    State("selected-node-store", "data"),
    State("selected-lot-store", "data"),
)
def update_selection(click_data, current_node_id, current_lot_id):
    if not click_data or "points" not in click_data or not click_data["points"]:
        return current_node_id, current_lot_id

    point = click_data["points"][0]
    customdata = point.get("customdata")

    if not customdata or len(customdata) < 2:
        return current_node_id, current_lot_id

    object_id, object_type = customdata[0], customdata[1]

    if object_type == "node":
        return object_id, None
    if object_type == "lot":
        return current_node_id, object_id

    return current_node_id, current_lot_id


@app.callback(
    Output("network-graph", "figure"),
    Output("psi-graph", "figure"),
    Output("detail-panel", "children"),
    Output("event-table", "data"),
    Input("time-slider", "value"),
    Input("selected-node-store", "data"),
    Input("selected-lot-store", "data"),
)
def update_main_view(time_index: int, selected_node_id: Optional[str], selected_lot_id: Optional[str]):
    tb = time_buckets[time_index]
    snapshot = snapshots[tb]

    nodes = snapshot["nodes"]
    edges = snapshot["edges"]
    lots = snapshot["lots"]

    if not selected_node_id:
        selected_node_id = DEFAULT_NODE_ID

    psi_map: Dict[Tuple[str, str], PSIViewModel] = snapshot["psi_by_node_product"]
    psi = psi_map.get((selected_node_id, DEFAULT_PRODUCT_ID))
    if psi is None:
        psi = next(iter(psi_map.values()))

    network_fig = build_network_figure(
        nodes=nodes,
        edges=edges,
        lots=lots,
        selected_node_id=selected_node_id,
        selected_lot_id=selected_lot_id,
    )

    psi_fig = build_psi_figure(psi, tb)
    detail_panel = build_detail_panel(snapshot, selected_node_id, selected_lot_id)
    event_rows = build_event_table(snapshot["events"])

    return network_fig, psi_fig, detail_panel, event_rows


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)