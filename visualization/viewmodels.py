# pysi/visualization/viewmodels.py

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


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