# pysi/tutorial/plot_rice_v0.py

#重複と値チェック用
#python -c "import pandas as pd; ts=pd.read_csv('data/phone_v0/phone_timeseries.csv'); x=ts[(ts.node_name=='DAD_PHONE')&(ts.item=='initial_inventory')]; print(x)"

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from pysi.tutorial.rice_v0_adapter import RiceV0Model




def plot_psi_with_capacity(model: RiceV0Model, title: str = "PSI Overview (Demand / Supply / Inventory)") -> None:
    months = model.months
    x = np.arange(len(months))

    prod = model.production.values
    sales = model.sales.values
    demand = model.demand.values
    inv = model.inv.values
    co = model.shortage.values if hasattr(model, "shortage") and model.shortage is not None else None

    fig, ax = plt.subplots()

    # --- Bars: Production on left axis, Inventory on right axis ---
    w = 0.38
    # Production (gold)
    ax.bar(x - w/2, prod, width=w, color="gold", label="Production (P)")

    # Capacity as "container" (outline only, thick, red)
    if model.capacity is not None:
        cap = model.capacity.values
        ax.bar(
            x - w/2, cap,
            fill=False,
            edgecolor="red",
            linewidth=2.5,
            label="Capacity (MOM)"
        )

    # Inventory (brown) on secondary axis as bar
    ax2 = ax.twinx()
    ax2.bar(x + w/2, inv, width=w, color="brown", alpha=0.55, label="Inventory (I)")

    # Demand vs Sales (lines) — make overlap readable
    ax.plot(
        x, demand,
        color="lightgrey",
        linewidth=2.8, marker="o", markersize=7,
        label="Demand (MKT)", zorder=5
    )
    ax.plot(
        x, sales,
        #color="blue",
        color="lightblue",
        linewidth=1.2, marker="o", markersize=4,
        label="Sales (S, fulfilled)", zorder=6
    )

    # Backlog / Carry Over (CO) as line (dark blue)
    if co is not None and float(np.sum(co)) > 0:
        ax.plot(
            x, co,
            color="darkblue",
            linewidth=2.0, marker="^", markersize=4,
            label="Backlog (CO)", zorder=7
        )

    ax.set_title(title)
    ax.set_xlabel("Month")
    ax.set_ylabel("Lots")
    ax2.set_ylabel("Inventory")

    # --- Sync right axis scale to left axis scale (same visual scale) ---
    ax2.set_ylim(ax.get_ylim())
    ax2.set_yticks(ax.get_yticks())

    step = max(1, len(months)//12)
    ax.set_xticks(x[::step])
    ax.set_xticklabels([months[i] for i in range(0, len(months), step)], rotation=45, ha="right")

    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="upper right")

    fig.tight_layout()
    plt.show()

