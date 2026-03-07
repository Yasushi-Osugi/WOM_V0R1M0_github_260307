#pysi/tutorial/plot_rice_v0.py
# pysi/tutorial/plot_rice_v0.py
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

    fig, ax = plt.subplots()

    # Production (filled bar)
    ax.bar(x, prod, label="Production (P)")

    # Capacity as "container" (outline only, thick, green)
    if model.capacity is not None:
        cap = model.capacity.values
        ax.bar(
            x, cap,
            fill=False,           # outline only

            edgecolor="red",      # capacity = container (red)
            #edgecolor="green",    # requested

            linewidth=2.5,        # thick
            label="Capacity (MOM)"
        )

    # Demand vs Sales (lines)
    ax.plot(x, demand, marker=".", linewidth=1.5, label="Demand (MKT)")
    ax.plot(x, sales, marker="o", linewidth=1.5, label="Sales (S, fulfilled)")

    # Inventory (secondary axis)
    ax2 = ax.twinx()
    ax2.plot(x, inv, marker="s", linewidth=2.0, label="Inventory (I)")

    #  Carry Over (CO) annotation (if any)
    if float(model.shortage.sum()) > 0:
        for i, co in enumerate(model.shortage.values):
            if co > 0:
                ax.annotate(
                    f"CO:{co:.0f}", (x[i], sales[i]),
                    textcoords="offset points", xytext=(0, 8), ha="center"
                )

    ax.set_title(title)
    ax.set_xlabel("Month")
    ax.set_ylabel("Lots")
    ax2.set_ylabel("Inventory")

    # X tick labels: reduce density
    step = max(1, len(months)//12)
    ax.set_xticks(x[::step])
    ax.set_xticklabels(
        [months[i] for i in range(0, len(months), step)],
        rotation=45, ha="right"
    )

    # Merge legends from both axes
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="upper left")
    # Note:
    # - Inventory (I): physical stock at DAD (right axis)
    # - Carry Over (CO): backlog / unmet demand, shown as annotations


    fig.tight_layout()
    plt.show()
