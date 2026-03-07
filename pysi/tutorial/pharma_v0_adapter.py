#pysi/tutorial/pharma_v0_adapter.py

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional
import pandas as pd
import numpy as np
import os


# =========================
# Data model
# =========================

@dataclass
class PharmaV0Model:
    months: List[str]

    # time series
    import_supply: pd.Series          # arrival to cold DC
    demand: pd.Series                 # vaccination demand
    vaccination_capacity: pd.Series   # max shots/month

    # results
    inventory: pd.Series
    sales: pd.Series
    backlog: pd.Series
    waste: pd.Series                  # expired or overflow waste

    # parameters
    dc_capacity: int
    shelf_life: int


# =========================
# Loader
# =========================

def load_pharma_v0(
    data_dir: str,
    *,
    dc_capacity: int = 300,
    shelf_life: int = 3,
) -> PharmaV0Model:
    """
    Load Pharma Cold Chain V0 model from CSV and run simple PSI simulation.

    Assumptions (V0):
    - import_supply arrives to cold DC at the beginning of each month
    - sales (vaccination) is limited by:
        min(demand, vaccination_capacity, available_inventory)
    - inventory has:
        - upper bound: dc_capacity
        - shelf life: shelf_life months (FIFO expiration)
    - any overflow or expiration is counted as waste
    """

    ts_path = os.path.join(data_dir, "pharma_timeseries.csv")
    ts = pd.read_csv(ts_path)

    required_cols = {"month", "node_name", "item", "value"}
    if not required_cols.issubset(ts.columns):
        raise ValueError(f"CSV must contain columns {required_cols}")

    # ---- data quality check (教材向け：重複はエラー) ----
    dup = ts.duplicated(["month", "node_name", "item"], keep=False)
    if dup.any():
        raise ValueError(
            "Duplicate keys found in pharma_timeseries.csv:\n"
            + ts[dup].sort_values(["node_name", "item", "month"]).to_string(index=False)
        )

    # months axis
    months = sorted(ts["month"].unique().tolist())

    def _series(node: str, item: str) -> pd.Series:
        s = (
            ts[(ts["node_name"] == node) & (ts["item"] == item)]
            .set_index("month")["value"]
            .astype(float)
        )
        return s.reindex(months, fill_value=0.0)

    # ---- inputs ----
    import_supply = _series("DAD_COLD_DC", "import_supply")
    demand = _series("MKT_HOSP", "demand")
    vaccination_capacity = _series("MKT_HOSP", "vaccination_capacity")

    # initial inventory (default 0)
    init_inv = 0.0
    if (
        (ts["node_name"] == "DAD_COLD_DC")
        & (ts["item"] == "initial_inventory")
    ).any():
        init_inv = float(
            ts[(ts["node_name"] == "DAD_COLD_DC") & (ts["item"] == "initial_inventory")]
            ["value"]
            .iloc[0]
        )

    # =========================
    # PSI simulation (V0)
    # =========================

    inventory = []
    sales = []
    backlog = []
    waste = []

    # inventory buckets for shelf life (FIFO)
    # index 0 = newest, index shelf_life-1 = expiring
    buckets = [0.0 for _ in range(shelf_life)]
    buckets[0] = init_inv

    backlog_prev = 0.0

    for m in months:
        # 1) arrival to DC
        arrival = float(import_supply.loc[m])
        buckets[0] += arrival

        # 2) enforce DC capacity (overflow -> waste)
        total_inv = sum(buckets)
        overflow = max(total_inv - dc_capacity, 0.0)
        if overflow > 0:
            # remove overflow from newest stock
            buckets[0] -= overflow
        waste_month = overflow

        # 3) available for vaccination
        available = sum(buckets)

        # effective demand includes backlog
        eff_demand = float(demand.loc[m]) + backlog_prev
        cap = float(vaccination_capacity.loc[m])

        s = min(eff_demand, cap, available)

        # 4) consume inventory (FIFO from oldest)
        to_ship = s
        for i in reversed(range(shelf_life)):
            take = min(buckets[i], to_ship)
            buckets[i] -= take
            to_ship -= take
            if to_ship <= 0:
                break

        # 5) update backlog
        backlog_now = eff_demand - s

        # 6) expiration (shift buckets)
        expired = buckets[-1]
        waste_month += expired
        buckets = [0.0] + buckets[:-1]

        inventory.append(sum(buckets))
        sales.append(s)
        backlog.append(backlog_now)
        waste.append(waste_month)

        backlog_prev = backlog_now

    return PharmaV0Model(
        months=months,
        import_supply=import_supply,
        demand=demand,
        vaccination_capacity=vaccination_capacity,
        inventory=pd.Series(inventory, index=months),
        sales=pd.Series(sales, index=months),
        backlog=pd.Series(backlog, index=months),
        waste=pd.Series(waste, index=months),
        dc_capacity=dc_capacity,
        shelf_life=shelf_life,
    )
