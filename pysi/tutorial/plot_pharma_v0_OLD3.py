# pysi/tutorial/plot_pharma_v0.py
# pysi/tutorial/plot_pharma_v0.py
from __future__ import annotations

import re
import numpy as np
import matplotlib.pyplot as plt

from pysi.tutorial.pharma_v0_adapter import PharmaV0Model


_MONTH_RE = re.compile(r"^\d{4}-\d{2}$")


def _filter_month_rows(model: PharmaV0Model):
    """
    Some scenario CSVs may include comment/label rows in the 'month' column
    (e.g., '# demand (...)'). This plot filters out non 'YYYY-MM' rows.
    """
    months_raw = list(model.months)
    keep = [i for i, m in enumerate(months_raw) if _MONTH_RE.match(str(m).strip())]

    # If nothing matches, fall back to raw (so we don't crash unexpectedly)
    if not keep:
        return (
            months_raw,
            model.demand.values,
            model.sales.values,
            model.import_supply.values,
            model.waste.values,
            model.inventory.values,
            model.backlog.values,
            model.vaccination_capacity.values,
        )

    months = [months_raw[i] for i in keep]

    def pick(arr):
        a = np.asarray(arr)
        return a[keep]

    return (
        months,
        pick(model.demand.values),
        pick(model.sales.values),
        pick(model.import_supply.values),
        pick(model.waste.values),
        pick(model.inventory.values),
        pick(model.backlog.values),
        pick(model.vaccination_capacity.values),
    )


def plot_pharma_v0(
    model: PharmaV0Model,
    title: str = "Pharma Cold Chain V0 (Japan Domestic Planning)",
) -> None:
    """
    Pharma Cold Chain V0 plot (monthly) - SINGLE AXIS version (no twinx):
      - One axis for Flow + Stock + Backlog
      - Keep style close to plot_rice_v0.py:
          Demand: lightgrey line (thicker)
          Sales:  navy line
          Inventory: brown bar
          Backlog/CO: darkblue line
    """
    (
        months,
        demand,
        sales,
        import_supply,
        waste,
        inv,
        backlog,
        vacc_cap,
    ) = _filter_month_rows(model)

    x = np.arange(len(months))
    fig, ax = plt.subplots(figsize=(14, 5))

    # --- Bars (single axis) ---
    w = 0.22  # bar width
    # Import supply (to DC)
    ax.bar(
        x - 1.5 * w,
        import_supply,
        width=w,
        alpha=0.55,
        label="Import supply (to DC)",
        zorder=1,
    )
    # Waste (expired + overflow)
    ax.bar(
        x - 0.5 * w,
        waste,
        width=w,
        alpha=0.55,
        label="Waste (expired + overflow)",
        zorder=1,
    )
    # Inventory (DC) - brown bar
    ax.bar(
        x + 0.5 * w,
        inv,
        width=w,
        color="brown",
        alpha=0.55,
        label="Inventory (DC)",
        zorder=1,
    )

    # --- Lines (single axis) ---
    # Demand (lightGrey, thicker, big markers)
    ax.plot(
        x,
        demand,
        color="lightgrey",
        linewidth=2.8,
        marker="o",
        markersize=7,
        label="Demand (vaccination requests)",
        zorder=5,
    )

    # Vaccination capacity (line)
    ax.plot(
        x,
        vacc_cap,
        linewidth=2.0,
        marker="^",
        markersize=5,
        label="Vaccination capacity",
        zorder=4,
    )

    # Sales (fulfilled) - darkBlue (navy)
    ax.plot(
        x,
        sales,
        color="navy",
        linewidth=2.0,
        marker="o",
        markersize=4,
        label="Sales (vaccinations performed)",
        zorder=6,
    )

    # Backlog / CO as line (darkBlue)
    ax.plot(
        x,
        backlog,
        color="darkblue",
        linewidth=2.4,
        marker="s",
        markersize=4,
        label="Backlog / CO",
        zorder=7,
    )

    # --- Labels / Ticks ---
    ax.set_title(title)
    ax.set_xlabel("Month")
    ax.set_ylabel("Lots")

    step = max(1, len(months) // 12)
    ax.set_xticks(x[::step])
    ax.set_xticklabels(
        [months[i] for i in range(0, len(months), step)],
        rotation=45,
        ha="right",
    )

    # Legend
    ax.legend(loc="upper left")

    fig.tight_layout()
    plt.show()


def plot_pharma_v0_compact(
    model: PharmaV0Model,
    title: str = "Pharma Cold Chain V0 (Japan Domestic Planning)",
) -> None:
    """
    Compact variant (single axis).
    """
    (
        months,
        demand,
        sales,
        import_supply,
        waste,
        inv,
        backlog,
        vacc_cap,
    ) = _filter_month_rows(model)

    x = np.arange(len(months))
    fig, ax = plt.subplots(figsize=(14, 4.8))

    w = 0.24
    ax.bar(x - 1.5 * w, import_supply, width=w, alpha=0.55, label="Import supply (to DC)", zorder=1)
    ax.bar(x - 0.5 * w, waste, width=w, alpha=0.55, label="Waste (expired + overflow)", zorder=1)
    ax.bar(x + 0.5 * w, inv, width=w, color="brown", alpha=0.55, label="Inventory (DC)", zorder=1)

    ax.plot(x, demand, color="lightgrey", linewidth=2.8, marker="o", markersize=7,
            label="Demand (vaccination requests)", zorder=5)
    ax.plot(x, vacc_cap, linewidth=2.0, marker="^", markersize=5,
            label="Vaccination capacity", zorder=4)
    ax.plot(x, sales, color="navy", linewidth=2.0, marker="o", markersize=4,
            label="Sales (vaccinations performed)", zorder=6)
    ax.plot(x, backlog, color="darkblue", linewidth=2.4, marker="s", markersize=4,
            label="Backlog / CO", zorder=7)

    ax.set_title(title)
    ax.set_xlabel("Month")
    ax.set_ylabel("Lots")

    step = max(1, len(months) // 12)
    ax.set_xticks(x[::step])
    ax.set_xticklabels([months[i] for i in range(0, len(months), step)], rotation=45, ha="right")

    ax.legend(loc="upper left")
    fig.tight_layout()
    plt.show()
