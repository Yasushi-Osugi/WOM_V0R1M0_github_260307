# pysi/tutorial/plot_pharma_v0.py
from __future__ import annotations

from dataclasses import asdict
from typing import Any, Iterable, Optional

import numpy as np
import matplotlib.pyplot as plt


def _to_1d_array(x: Any, n_fallback: Optional[int] = None) -> np.ndarray:
    """Convert list/Series/ndarray/scalar -> 1D float array."""
    if x is None:
        if n_fallback is None:
            return np.asarray([], dtype=float)
        return np.zeros(n_fallback, dtype=float)

    # pandas Series / Index / etc.
    if hasattr(x, "values"):
        arr = np.asarray(x.values, dtype=float)
    else:
        arr = np.asarray(x, dtype=float)

    # scalar -> 1d
    if arr.ndim == 0:
        if n_fallback is None:
            return np.asarray([float(arr)], dtype=float)
        return np.full(n_fallback, float(arr), dtype=float)

    return arr.astype(float).reshape(-1)


def _get_series(model: Any, name: str, fallback: Any = None):
    v = getattr(model, name, None)
    if v is None:
        return fallback
    return v


def plot_pharma_v0(
    model: Any,
    title: str = "Pharma Cold Chain V0 (Japan Domestic Planning)",
    *,
    s_cap_fixed: float = 120.0,     # ★ここで接種能力を固定（全期間）
    dc_ceiling: Optional[float] = None,  # Noneなら model.dc_capacity を使う
    shade_gap: bool = True,         # ★CO+D vs S_cap の乖離帯
    show: bool = True,
):
    """
    Pharma Cold Chain V0 plot (single axis).

    Expected model fields (best-effort):
      - months (index-like, list of YYYY-MM, etc)
      - demand (Series)
      - vaccination_capacity (Series)   # 使わず固定上書きするが、長さ取りに使える
      - sales (Series)
      - backlog (Series)                # carryover / CO
      - import_supply (Series)
      - waste (Series)
      - inventory (Series)              # DC stock
      - dc_capacity (float)             # storage limit
    """

    # --- X axis (months) ---
    months = _get_series(model, "months", None)
    if months is None:
        # fallback: infer from demand index
        d = _get_series(model, "demand", None)
        if d is None:
            raise ValueError("model.months or model.demand is required for plotting.")
        months = list(getattr(d, "index", range(len(d))))

    x_labels = [str(m) for m in months]
    x = np.arange(len(x_labels))

    # --- series ---
    demand_s = _get_series(model, "demand", None)
    sales_s = _get_series(model, "sales", None)
    backlog_s = _get_series(model, "backlog", None)
    import_s = _get_series(model, "import_supply", None)
    waste_s = _get_series(model, "waste", None)
    inv_s = _get_series(model, "inventory", None)

    n = len(x_labels)

    demand = _to_1d_array(demand_s, n)
    sales = _to_1d_array(sales_s, n)
    backlog = _to_1d_array(backlog_s, n)
    import_supply = _to_1d_array(import_s, n)
    waste = _to_1d_array(waste_s, n)
    inventory = _to_1d_array(inv_s, n)


    # --- S_cap from model (CSV-driven) ---
    s_cap_s = _get_series(model, "vaccination_capacity", None)
    if s_cap_s is None:
        raise ValueError("model.vaccination_capacity is required for plotting.")
    s_cap = _to_1d_array(s_cap_s, n)



    # --- DC ceiling ---
    if dc_ceiling is None:
        dc_cap_raw = getattr(model, "dc_capacity", None)
        if dc_cap_raw is None:
            dc_ceiling = 300.0
        else:
            dc_ceiling = float(np.asarray(dc_cap_raw).reshape(-1)[0])
    else:
        dc_ceiling = float(dc_ceiling)

    # --- CO+D line (total need) ---
    # carryover/backlog is treated as "this month's CO" (start-of-month backlog)
    co_plus_d = backlog + demand

    # --- plot ---
    fig, ax = plt.subplots(figsize=(16, 7))
    ax.set_title(title)

    # Bars layout
    w = 0.22
    #ax.bar(x - w, import_supply, width=w, label="Import supply (to DC)", alpha=0.95)
    #ax.bar(x, waste, width=w, label="Waste (expired + overflow)", alpha=0.85)
    #ax.bar(x + w, inventory, width=w, label="Inventory (DC)", alpha=0.55)

    ax.bar(
        x - w, import_supply,
        width=w,
        color="gold",          # ★ P: GOLD
        label="Import supply (to DC)",
        alpha=0.95
    )
    ax.bar(
        x + w, inventory,
        width=w,
        color="brown",         # ★ I: BROWN
        label="Inventory (DC)",
        alpha=0.55
    )
    ax.bar(
        x, waste,
        width=w,
        color="orange",        # ★ Waste: ORANGE
        label="Waste (expired + overflow)",
        alpha=0.85
    )


    # Demand (D): light gray thick + big marker
    ax.plot(
        x, demand,
        color="lightgray",
        linewidth=3.2,
        marker="o",
        markersize=7,
        label="D: Demand (vaccination requests)",
        zorder=5,
    )

    # CO+D: dashed red-brown (total need)
    ax.plot(
        x, co_plus_d,
        color="firebrick",
        linestyle="--",
        linewidth=2.0,
        label="CO+D: Total need (carryover + demand)",
        zorder=6,
    )

    # S_cap: red marker-only (no line) : "_" looks like a ceiling tick
    ax.plot(
        x, s_cap,
        color="red",
        linestyle="None",
        marker="_",
        markersize=16,
        markeredgewidth=2.2,
        label="S_cap: Vaccination capacity (fixed)",
        zorder=7,
    )

    # Sales (S): dark blue thinner
    ax.plot(
        x, sales,
        color="navy",
        linewidth=1.6,
        marker="o",
        markersize=4.5,
        label="S: Vaccinations performed",
        zorder=7,
    )

    # CO: backlog (dark blue, square markers)
    ax.plot(
        x, backlog,
        color="darkblue",
        linewidth=2.2,
        marker="s",
        markersize=4.5,
        label="CO: Backlog / carryover",
        zorder=7,
    )

    # DC ceiling line
    ax.axhline(
        y=dc_ceiling,
        color="red",
        linestyle=":",
        linewidth=1.8,
        label="DC ceiling (storage limit)",
        zorder=2,
    )

    # --- Gap shading: where total_need (CO+D) > S_cap ---
    if shade_gap:
        gap_mask = co_plus_d > s_cap
        # shade contiguous segments
        in_seg = False
        seg_start = 0
        for i, flag in enumerate(gap_mask):
            if flag and not in_seg:
                in_seg = True
                seg_start = i
            if in_seg and (not flag or i == len(gap_mask) - 1):
                seg_end = i if not flag else i
                ax.axvspan(
                    seg_start - 0.5,
                    seg_end + 0.5,
                    color="red",
                    alpha=0.06,
                    zorder=1,
                )
                in_seg = False

    # Axis styling
    ax.set_ylabel("Lots")
    ax.set_xlabel("Month")

    # ticks: show every 2 months for readability (adjust if you want)
    step = 2 if n > 12 else 1
    ax.set_xticks(x[::step])
    ax.set_xticklabels(x_labels[::step], rotation=35, ha="right")

    # Legend order (読み順)
    handles, labels = ax.get_legend_handles_labels()
    order = [
        "D: Demand (vaccination requests)",
        "CO+D: Total need (carryover + demand)",
        "S_cap: Vaccination capacity (fixed)",
        "S: Vaccinations performed",
        "CO: Backlog / carryover",
        "Import supply (to DC)",
        "Inventory (DC)",
        "Waste (expired + overflow)",
        "DC ceiling (storage limit)",
    ]
    idx = {lab: i for i, lab in enumerate(labels)}
    new_handles = [handles[idx[o]] for o in order if o in idx]
    new_labels = [labels[idx[o]] for o in order if o in idx]
    ax.legend(new_handles, new_labels, loc="upper right", framealpha=0.9)

    ax.grid(True, axis="y", alpha=0.25)

    fig.tight_layout()
    if show:
        plt.show()
    return fig, ax
