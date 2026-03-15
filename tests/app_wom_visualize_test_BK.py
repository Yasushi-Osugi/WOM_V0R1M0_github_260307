from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from dash import Dash, Input, Output, State, dcc, html, dash_table, ctx
import plotly.graph_objects as go


# ============================================================
# Data Models
# ============================================================

@dataclass(frozen=True)
class NodeViewModel:
    node_id: str
    node_type: str
    x: float
    y: float
    inventory_qty: float
    shortage_flag: bool
    overflow_flag: bool
    sales_qty: float


@dataclass(frozen=True)
class EdgeViewModel:
    edge_id: str
    from_node: str
    to_node: str
    capacity: float
    flow_qty: float
    congestion_ratio: float


@dataclass(frozen=True)
class LotViewModel:
    lot_id: str
    product_id: str
    quantity_cpu: float
    status: str
    current_node: Optional[str]
    current_edge: Optional[str]
    progress: float
    age_weeks: int
    linked_demand_id: Optional[str] = None


@dataclass(frozen=True)
class PSIViewModel:
    node_id: str
    product_id: str
    weeks: List[str]
    demand: List[float]
    shipment: List[float]
    arrival: List[float]
    sales: List[float]
    inventory: List[float]
    backlog: List[float]


@dataclass(frozen=True)
class EventRowViewModel:
    time_bucket: str
    event_type: str
    object_id: str
    node_id: Optional[str]
    description: str


# ============================================================
# Mock Snapshot Builder
# ============================================================

def build_mock_snapshots() -> Tuple[Dict[str, dict], List[str]]:
    """
    Build a minimal in-memory scenario.

    Network:
        FACTORY_A -> DC_TOKYO -> MARKET_TOKYO

    Time:
        4 weekly buckets

    This is intentionally simple so the Dash GUI can be verified first.
    Later this can be replaced by:
        minimal_kernel replay -> snapshots
    """
    time_buckets = ["2026W01", "2026W02", "2026W03", "2026W04"]
    snapshots: Dict[str, dict] = {}

    psi_dc = PSIViewModel(
        node_id="DC_TOKYO",
        product_id="SKU_A",
        weeks=time_buckets,
        demand=[100, 120, 150, 160],
        shipment=[90, 110, 130, 150],
        arrival=[85, 105, 120, 145],
        sales=[80, 100, 125, 150],
        inventory=[300, 305, 300, 295],
        backlog=[20, 25, 30, 20],
    )

    psi_factory = PSIViewModel(
        node_id="FACTORY_A",
        product_id="SKU_A",
        weeks=time_buckets,
        demand=[100, 120, 150, 160],
        shipment=[100, 115, 140, 155],
        arrival=[0, 0, 0, 0],
        sales=[0, 0, 0, 0],
        inventory=[500, 470, 420, 390],
        backlog=[0, 0, 10, 5],
    )

    psi_market = PSIViewModel(
        node_id="MARKET_TOKYO",
        product_id="SKU_A",
        weeks=time_buckets,
        demand=[100, 120, 150, 160],
        shipment=[80, 100, 125, 150],
        arrival=[80, 100, 125, 150],
        sales=[80, 100, 125, 150],
        inventory=[60, 55, 40, 30],
        backlog=[20, 20, 25, 10],
    )

    for i, tb in enumerate(time_buckets):
        nodes = [
            NodeViewModel(
                node_id="FACTORY_A",
                node_type="factory",
                x=0.0,
                y=0.0,
                inventory_qty=max(500 - i * 35, 0),
                shortage_flag=False,
                overflow_flag=False,
                sales_qty=0,
            ),
            NodeViewModel(
                node_id="DC_TOKYO",
                node_type="dc",
                x=5.0,
                y=0.0,
                inventory_qty=300 + (i * 10 if i < 2 else -5 * i),
                shortage_flag=False,
                overflow_flag=(i == 1),
                sales_qty=120 + i * 10,
            ),
            NodeViewModel(
                node_id="MARKET_TOKYO",
                node_type="market",
                x=10.0,
                y=0.0,
                inventory_qty=max(80 - i * 12, 0),
                shortage_flag=(i >= 2),
                overflow_flag=False,
                sales_qty=150 + i * 15,
            ),
        ]

        edges = [
            EdgeViewModel(
                edge_id="FACTORY_A->DC_TOKYO",
                from_node="FACTORY_A",
                to_node="DC_TOKYO",
                capacity=300.0,
                flow_qty=180 + i * 15,
                congestion_ratio=(180 + i * 15) / 300.0,
            ),
            EdgeViewModel(
                edge_id="DC_TOKYO->MARKET_TOKYO",
                from_node="DC_TOKYO",
                to_node="MARKET_TOKYO",
                capacity=250.0,
                flow_qty=160 + i * 8,
                congestion_ratio=(160 + i * 8) / 250.0,
            ),
        ]

        # A few lots moving or waiting at nodes.
        lots = [
            LotViewModel(
                lot_id=f"LOT_F2D_{i+1:03d}",
                product_id="SKU_A",
                quantity_cpu=100.0,
                status="in_transit",
                current_node=None,
                current_edge="FACTORY_A->DC_TOKYO",
                progress=min(0.18 + i * 0.22, 0.95),
                age_weeks=i,
                linked_demand_id=f"DEM_{i+1:03d}",
            ),
            LotViewModel(
                lot_id=f"LOT_D2M_{i+11:03d}",
                product_id="SKU_A",
                quantity_cpu=80.0,
                status="in_transit" if i >= 1 else "at_node",
                current_node=None if i >= 1 else "DC_TOKYO",
                current_edge="DC_TOKYO->MARKET_TOKYO" if i >= 1 else None,
                progress=min(0.10 + i * 0.25, 0.90) if i >= 1 else 0.0,
                age_weeks=i + 1,
                linked_demand_id=f"DEM_{i+11:03d}",
            ),
            LotViewModel(
                lot_id=f"LOT_BUFFER_{i+21:03d}",
                product_id="SKU_A",
                quantity_cpu=60.0,
                status="at_node",
                current_node="DC_TOKYO",
                current_edge=None,
                progress=0.0,
                age_weeks=i + 2,
                linked_demand_id=None,
            ),
        ]

        events = [
            EventRowViewModel(
                time_bucket=tb,
                event_type="production",
                object_id=f"LOT_F2D_{i+1:03d}",
                node_id="FACTORY_A",
                description=f"Factory produced LOT_F2D_{i+1:03d}",
            ),
            EventRowViewModel(
                time_bucket=tb,
                event_type="shipment",
                object_id=f"LOT_F2D_{i+1:03d}",
                node_id="FACTORY_A",
                description="Shipment departed FACTORY_A for DC_TOKYO",
            ),
            EventRowViewModel(
                time_bucket=tb,
                event_type="arrival",
                object_id=f"LOT_D2M_{i+11:03d}",
                node_id="MARKET_TOKYO" if i >= 2 else "DC_TOKYO",
                description="Lot progressing through downstream route",
            ),
            EventRowViewModel(
                time_bucket=tb,
                event_type="sale",
                object_id=f"DEM_{i+1:03d}",
                node_id="MARKET_TOKYO",
                description=f"Sales executed for week {tb}",
            ),
        ]

        snapshots[tb] = {
            "time_bucket": tb,
            "nodes": nodes,
            "edges": edges,
            "lots": lots,
            "psi_by_node_product": {
                ("FACTORY_A", "SKU_A"): psi_factory,
                ("DC_TOKYO", "SKU_A"): psi_dc,
                ("MARKET_TOKYO", "SKU_A"): psi_market,
            },
            "events": events,
            "kpis": {
                "inventory_total": round(sum(n.inventory_qty for n in nodes), 2),
                "sales_total": round(sum(n.sales_qty for n in nodes), 2),
                "backlog_total": psi_dc.backlog[i],
            },
        }

    return snapshots, time_buckets


# ============================================================
# Figure Builders
# ============================================================

def _node_marker_size(inv: float) -> float:
    return 18.0 + max(inv / 18.0, 0.0)


def _edge_line_width(flow_qty: float) -> float:
    return 1.5 + max(flow_qty / 80.0, 0.0)


def _edge_color(congestion_ratio: float) -> str:
    if congestion_ratio >= 1.0:
        return "#d62728"  # overloaded
    if congestion_ratio >= 0.8:
        return "#ff7f0e"  # warning
    return "#7f7f7f"      # normal


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

    # Edges
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
                ),
                showlegend=False,
            )
        )

    # Nodes
    node_sizes = [_node_marker_size(n.inventory_qty) for n in nodes]
    node_colors = [_node_color(n) for n in nodes]
    node_line_widths = [4 if n.node_id == selected_node_id else 1.5 for n in nodes]

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
                "line": {"width": node_line_widths, "color": "#222"},
            },
            hoverinfo="text",
            hovertext=[
                f"{n.node_id}"
                f"<br>type={n.node_type}"
                f"<br>inventory={n.inventory_qty:.1f}"
                f"<br>sales={n.sales_qty:.1f}"
                for n in nodes
            ],
            name="Nodes",
        )
    )

    # Lots
    lot_x: List[float] = []
    lot_y: List[float] = []
    lot_text: List[str] = []
    lot_sizes: List[float] = []
    lot_outline: List[float] = []
    lot_customdata: List[List[str]] = []

    for lot in lots:
        if lot.current_edge and lot.current_edge in edge_map:
            edge = edge_map[lot.current_edge]
            src = node_map[edge.from_node]
            dst = node_map[edge.to_node]
            x = src.x + (dst.x - src.x) * lot.progress
            y = src.y + (dst.y - src.y) * lot.progress
        elif lot.current_node and lot.current_node in node_map:
            n = node_map[lot.current_node]
            x = n.x
            y = n.y - 0.35
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
        lot_sizes.append(10 + lot.quantity_cpu / 25.0)
        lot_outline.append(4 if lot.lot_id == selected_lot_id else 1.0)
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
                "color": "#111111",
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
        idx = psi.weeks.index(current_time_bucket)
        fig.add_vline(x=psi.weeks[idx], line_width=2, line_dash="dash", line_color="black")

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

    sections = [
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

snapshots, time_buckets = build_mock_snapshots()

DEFAULT_NODE_ID = "DC_TOKYO"
DEFAULT_PRODUCT_ID = "SKU_A"

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
                    [
                        dcc.Graph(id="network-graph"),
                    ],
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
                            page_size=8,
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
        # fall back gracefully
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