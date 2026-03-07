#pysi/tutorial/plot_pharma_v0.py

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt

from pysi.tutorial.pharma_v0_adapter import PharmaV0Model


def plot_pharma_v0(model: PharmaV0Model, title: str = "PSI Overview (Pharma Cold Chain V0)") -> None:
    """
    Plot one-page overview for Pharma Cold Chain V0.

    Left axis (flow / lots per month):
      - Import supply (to cold DC) [bar]
      - Demand (vaccination requests) [line]
      - Vaccination capacity [line]
      - Sales (vaccinations performed) [line]
      - Waste (expired + overflow) [bar]

    Right axis (stock / lots):
      - Inventory (cold DC) [bar]
      - Backlog/CO (unserved demand) [line]

    Notes:
      - Use same scale on both axes for readability if desired.
      - Default separates flow vs stock, which is usually clearer.
    """
    months = model.months
    x = np.arange(len(months))

    imp = model.import_supply.values
    demand = model.demand.values
    cap = model.vaccination_capacity.values
    sales = model.sales.values
    inv = model.inventory.values
    co = model.backlog.values
    waste = model.waste.values

    fig, ax = plt.subplots(figsize=(12, 6))

    # ---- Left axis: flows ----
    w = 0.38

    # Import supply as filled bar (to DC)
    ax.bar(x - w/2, imp, width=w, alpha=0.55, label="Import supply (to DC)")

    # Waste as filled bar (aligned to the other side)
    ax.bar(x + w/2, waste, width=w, alpha=0.55, label="Waste (expired + overflow)")

    # Demand / Capacity / Sales as lines
    ax.plot(
        x, demand,
        linewidth=2.6, marker="o", markersize=6,
        color="lightgrey",
        label="Demand (vaccination requests)", zorder=5
    )
    ax.plot(
        x, cap,
        linewidth=2.0, marker="^", markersize=5,
        label="Vaccination capacity", zorder=6
    )
    ax.plot(
        x, sales,
        linewidth=1.6, marker="o", markersize=4,
        label="Sales (vaccinations performed)", zorder=7
    )

    ax.set_xlabel("Month")
    ax.set_ylabel("Flow (lots / month)")

    # ---- Right axis: stock + backlog ----
    ax2 = ax.twinx()

    # Inventory as bar on right axis (semi-transparent)
    ax2.bar(x, inv, width=0.22, alpha=0.40, label="Inventory (DC)")

    # Backlog/CO as line
    ax2.plot(
        x, co,
        linewidth=2.2, marker="s", markersize=5,
        label="Backlog / CO", zorder=8
    )

    ax2.set_ylabel("Stock / Backlog (lots)")

    # ---- X ticks ----
    step = max(1, len(months) // 12)  # show about 12 labels
    ax.set_xticks(x[::step])
    ax.set_xticklabels([months[i] for i in range(0, len(months), step)], rotation=45, ha="right")

    # ---- Title + legends ----
    ax.set_title(title)

    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="upper left")

    fig.tight_layout()
    plt.show()


def plot_pharma_v0_same_scale(model: PharmaV0Model, title: str = "PSI Overview (Same Scale)") -> None:
    """
    Optional: Force right axis to match left axis scale.
    This is sometimes requested for 'PSI components on one ruler'.
    """
    months = model.months
    x = np.arange(len(months))

    imp = model.import_supply.values
    demand = model.demand.values
    cap = model.vaccination_capacity.values
    sales = model.sales.values
    inv = model.inventory.values
    co = model.backlog.values
    waste = model.waste.values

    fig, ax = plt.subplots(figsize=(12, 6))
    w = 0.38

    ax.bar(x - w/2, imp, width=w, alpha=0.55, label="Import supply (to DC)")
    ax.bar(x + w/2, waste, width=w, alpha=0.55, label="Waste (expired + overflow)")

    ax.plot(x, demand, linewidth=2.6, marker="o", markersize=6, color="lightgrey",
            label="Demand (vaccination requests)", zorder=5)
    ax.plot(x, cap, linewidth=2.0, marker="^", markersize=5,
            label="Vaccination capacity", zorder=6)
    ax.plot(x, sales, linewidth=1.6, marker="o", markersize=4,
            label="Sales (vaccinations performed)", zorder=7)

    ax2 = ax.twinx()
    ax2.bar(x, inv, width=0.22, alpha=0.40, label="Inventory (DC)")
    ax2.plot(x, co, linewidth=2.2, marker="s", markersize=5,
             label="Backlog / CO", zorder=8)

    ax.set_xlabel("Month")
    ax.set_ylabel("Lots")

    ax2.set_ylabel("Lots")

    # ---- Force same y-limits ----
    ymax = max(
        np.max(imp), np.max(demand), np.max(cap), np.max(sales),
        np.max(inv), np.max(co), np.max(waste),
    )
    ax.set_ylim(0, ymax * 1.15)
    ax2.set_ylim(0, ymax * 1.15)

    step = max(1, len(months) // 12)
    ax.set_xticks(x[::step])
    ax.set_xticklabels([months[i] for i in range(0, len(months), step)], rotation=45, ha="right")

    ax.set_title(title)

    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="upper left")

    fig.tight_layout()
    plt.show()
