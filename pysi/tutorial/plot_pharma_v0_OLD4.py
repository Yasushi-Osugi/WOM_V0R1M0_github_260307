# pysi/tutorial/plot_pharma_v0.py

# pysi/tutorial/plot_pharma_v0.py

from __future__ import annotations

import re
from typing import Iterable, List, Tuple

import numpy as np
import matplotlib.pyplot as plt

from pysi.tutorial.pharma_v0_adapter import PharmaV0Model


_YYYY_MM = re.compile(r"^\d{4}-\d{2}$")


def _as_array(x) -> np.ndarray:
    """Accept pandas Series / list / np array."""
    return np.asarray(x.values if hasattr(x, "values") else x, dtype=float)


def _filter_month_rows(model: PharmaV0Model) -> Tuple[List[str], np.ndarray]:
    """
    Some scenario CSVs may include comment/title rows like '# demand (...)'.
    Keep only rows whose month is YYYY-MM and return index mask.
    """
    months_all = list(model.months)
    mask = np.array([bool(_YYYY_MM.match(str(m))) for m in months_all], dtype=bool)
    months = [str(m) for m, ok in zip(months_all, mask) if ok]
    return months, mask


def plot_pharma_v0(
    model: PharmaV0Model,
    title: str = "Pharma Cold Chain V0 (Japan Domestic Planning)",
    show_gap_band: bool = True,
    show_dc_ceiling: bool = True,
) -> None:
    """
    Single-axis PSI overview for Pharma Cold Chain V0 (domestic planning).

    Lines (demand-related):
      - D: Demand (vaccination requests)               : lightgrey, thick, big markers
      - CO: Backlog / CO (unserved demand carryover)   : dark blue, square markers
      - CO+D: Total need this month                    : (CO_prev + D), dark red, dashed
      - S_cap: Vaccination capacity                    : red, thin, '_' (ceiling) marker
      - S: Vaccinations performed (Sales)              : navy (darkBlue), thinner

    Bars:
      - Import supply (to DC)                          : gold-ish (match P feel)
      - Inventory (DC)                                 : brown
      - Waste (expired + overflow)                     : orange-ish

    Visual aids:
      - Light red band where S_cap < (CO_prev + D)
      - DC storage ceiling line at model.dc_capacity (e.g., 300 lots)
    """

    # ----------------------------
    # Filter "month" to YYYY-MM only (drop comment rows)
    # ----------------------------
    months, mask = _filter_month_rows(model)
    if not months:
        raise ValueError("No valid YYYY-MM months found in model.months.")

    # Series
    demand = _as_array(model.demand)[mask]
    s_cap = _as_array(model.vaccination_capacity)[mask]
    sales = _as_array(model.sales)[mask]
    inv = _as_array(model.inventory)[mask]
    co_end = _as_array(model.backlog)[mask]
    imp = _as_array(model.import_supply)[mask]
    waste = _as_array(model.waste)[mask]

    # CO to use in CO+D line: backlog entering the month (carryover)
    co_prev = np.r_[0.0, co_end[:-1]]
    need = co_prev + demand  # CO + D

    x = np.arange(len(months))

    # ----------------------------
    # Figure / Axis (single axis)
    # ----------------------------
    fig, ax = plt.subplots(figsize=(13, 6))

    # ----------------------------
    # Bars (match Rice/Phone "bar vs line" feel)
    # ----------------------------
    w = 0.25

    # Import supply (acts like "P" in this domestic view)
    ax.bar(
        x - w,
        imp,
        width=w,
        color="gold",
        alpha=0.85,
        label="Import supply (to DC)",
        zorder=2,
    )

    # Inventory (brown)
    ax.bar(
        x,
        inv,
        width=w,
        color="brown",
        alpha=0.45,
        label="Inventory (DC)",
        zorder=2,
    )

    # Waste (orange-ish)
    ax.bar(
        x + w,
        waste,
        width=w,
        color="sandybrown",
        alpha=0.75,
        label="Waste (expired + overflow)",
        zorder=2,
    )

    # ----------------------------
    # Lines (demand-related)
    # ----------------------------

    # D: Demand
    ax.plot(
        x,
        demand,
        color="lightgrey",
        linewidth=3.0,
        marker="o",
        markersize=7,
        label="D: Demand (vaccination requests)",
        zorder=6,
    )

    # CO+D: total need this month
    ax.plot(
        x,
        need,
        color="firebrick",
        linewidth=2.0,
        linestyle="--",
        marker=".",
        markersize=4,
        label="CO+D: Total need (carryover + demand)",
        zorder=7,
    )

    # S_cap: capacity as a "ceiling container" 느낌 (red, thin, '_' marker)
    ax.plot(
        x,
        s_cap,
        color="red",
        linewidth=1.3,
        marker="_",          # horizontal bar marker
        markersize=14,
        label="S_cap: Vaccination capacity",
        zorder=8,
    )

    # S: Sales (performed) — darkBlue, thinner
    ax.plot(
        x,
        sales,
        color="navy",
        linewidth=1.6,
        marker="o",
        markersize=4,
        label="S: Vaccinations performed",
        zorder=9,
    )

    # CO: backlog — dark blue (slightly different tone), square markers
    ax.plot(
        x,
        co_end,
        color="midnightblue",
        linewidth=2.2,
        marker="s",
        markersize=5,
        label="CO: Backlog / carryover",
        zorder=10,
    )

    # ----------------------------
    # Gap band: highlight months where capacity is below need (CO+D)
    # ----------------------------
    if show_gap_band:
        gap = need - s_cap
        # highlight where gap positive AND there is something to serve
        for i in range(len(x)):
            if gap[i] > 1e-9 and need[i] > 0:
                ax.axvspan(i - 0.5, i + 0.5, color="lightcoral", alpha=0.12, zorder=1)

    # ----------------------------
    # DC ceiling line (storage limit)
    # ----------------------------
    if show_dc_ceiling:
        dc_cap = getattr(model, "dc_capacity", None)
        if dc_cap is not None:
            # dc_capacity may be scalar or per-month
            dc_cap_arr = _as_array(dc_cap)

            #if dc_cap_arr.size == 1:
            #    y = float(dc_cap_arr[0])

            if dc_cap_arr.ndim == 0:
                # scalar (e.g., array(300.))
                y = float(dc_cap_arr)
                ax.axhline(
                    y=y,
                    color="brown",
                    linewidth=1.4,
                    linestyle=":",
                    label="DC ceiling (storage limit)",
                    zorder=4,
                )
            elif dc_cap_arr.size == 1:
                # 1-element vector
                y = float(dc_cap_arr.reshape(-1)[0])

                ax.axhline(
                    y=y,
                    color="brown",
                    linewidth=1.4,
                    linestyle=":",
                    label="DC ceiling (storage limit)",
                    zorder=4,
                )
            else:
                dc_cap_arr = dc_cap_arr[mask]
                ax.plot(
                    x,
                    dc_cap_arr,
                    color="brown",
                    linewidth=1.4,
                    linestyle=":",
                    label="DC ceiling (storage limit)",
                    zorder=4,
                )

    # ----------------------------
    # Axes labels / ticks
    # ----------------------------
    ax.set_title(title)
    ax.set_xlabel("Month")
    ax.set_ylabel("Lots")

    step = max(1, len(months) // 12)
    ax.set_xticks(x[::step])
    ax.set_xticklabels([months[i] for i in range(0, len(months), step)], rotation=45, ha="right")

    # ----------------------------
    # Legend (reading order)
    # ----------------------------
    desired = [
        "D: Demand (vaccination requests)",
        "CO+D: Total need (carryover + demand)",
        "S_cap: Vaccination capacity",
        "S: Vaccinations performed",
        "CO: Backlog / carryover",
        "Import supply (to DC)",
        "Inventory (DC)",
        "Waste (expired + overflow)",
        "DC ceiling (storage limit)",
    ]

    handles, labels = ax.get_legend_handles_labels()
    by_label = {lab: h for h, lab in zip(handles, labels)}

    ordered_h = []
    ordered_l = []
    for lab in desired:
        if lab in by_label:
            ordered_h.append(by_label[lab])
            ordered_l.append(lab)

    # add any remaining (safe fallback)
    for lab in labels:
        if lab not in ordered_l:
            ordered_h.append(by_label[lab])
            ordered_l.append(lab)

    ax.legend(ordered_h, ordered_l, loc="upper left")

    fig.tight_layout()
    plt.show()

