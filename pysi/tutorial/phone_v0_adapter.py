# pysi/tutorial/phone_v0_adapter.py
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import pandas as pd


@dataclass
class PhoneV0Model:
    months: list[str]                 # ["2025-01", ...]
    demand: pd.Series                 # index=month, value=demand at MKT
    production: pd.Series             # index=month, value=production at MOM
    inv: pd.Series                    # computed inventory at DAD (end of month)
    sales: pd.Series                  # fulfilled sales (= ship to market)
    shortage: pd.Series               # here: Carry Over (CO) / backlog (end of month)
    capacity: pd.Series | None = None # optional capacity at MOM (for graph)


def load_phone_v0(data_dir: str | Path, *, ship_lt: int = 2) -> PhoneV0Model:
    """
    Load Smartphone V0 CSV set and run a minimal PSI(+CO) simulation.

    Interpretation in this tutorial:
      - demand: market request (bell-shaped)
      - production: factory production decision
      - ship: production arrives to DAD after ship_lt months (physical lead time)
      - sales: fulfilled amount (limited by available inventory at DAD)
      - shortage: Carry Over (CO) / backlog remaining at end of month
    """
    data_dir = Path(data_dir)
    ts_path = data_dir / "phone_timeseries.csv"
    if not ts_path.exists():
        raise FileNotFoundError(f"phone_timeseries.csv not found: {ts_path}")

    ts = pd.read_csv(ts_path)
    required_cols = {"month", "node_name", "item", "value"}
    if not required_cols.issubset(set(ts.columns)):
        raise ValueError(
            f"phone_timeseries.csv must have columns {sorted(required_cols)}; got {list(ts.columns)}"
        )

    # Months
    months = sorted(ts["month"].astype(str).unique().tolist())

    def _series(node: str, item: str) -> pd.Series:
        s = (
            ts[(ts["node_name"] == node) & (ts["item"] == item)]
            .set_index("month")["value"]
            .astype(float)
        )
        # fill missing months with 0
        return s.reindex(months, fill_value=0.0)

    # Core inputs
    demand = _series("MKT_PHONE", "demand")
    production = _series("MOM_PHONE", "production")

    # Optional capacity
    cap_rows = ts[(ts["node_name"] == "MOM_PHONE") & (ts["item"] == "capacity")]
    capacity = None
    if len(cap_rows) > 0:
        capacity = _series("MOM_PHONE", "capacity")

    # Initial inventory at DAD (optional)
    init_inv = 0.0
    init_rows = ts[(ts["node_name"] == "DAD_PHONE") & (ts["item"] == "initial_inventory")]
    if len(init_rows) > 0:
        init_inv = float(init_rows["value"].iloc[0])

    # --- Physical lead time: production -> ship arriving to DAD after ship_lt months ---
    # ship[t] = production[t - ship_lt]
    ship = production.shift(ship_lt).fillna(0.0)

    # --- PSI(+CO) simulation at DAD ---
    inv = []
    sales = []
    co = []  # carry over (backlog) end-of-month

    inv_prev = init_inv
    co_prev = 0.0

    for m in months:
        available = inv_prev + float(ship.loc[m])            # DAD inventory + arrivals
        req = float(demand.loc[m]) + co_prev                 # this month's demand + backlog

        s = min(available, req)                              # fulfilled (sales)
        co_now = req - s                                     # remaining backlog
        inv_now = available - s                              # end inventory

        inv.append(inv_now)
        sales.append(s)
        co.append(co_now)

        inv_prev = inv_now
        co_prev = co_now

    inv_s = pd.Series(inv, index=months, name="inventory")
    sales_s = pd.Series(sales, index=months, name="sales")
    shortage_s = pd.Series(co, index=months, name="carry_over")  # note: backlog

    return PhoneV0Model(
        months=months,
        demand=demand.rename("demand"),
        production=production.rename("production"),
        inv=inv_s,
        sales=sales_s,
        shortage=shortage_s,  # used as CO/backlog
        capacity=capacity.rename("capacity") if capacity is not None else None,
    )
