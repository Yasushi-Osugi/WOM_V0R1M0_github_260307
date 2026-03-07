# pysi/tutorial/plot_pharma_v0.py
# pysi/tutorial/plot_pharma_v0.py
from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt

from pysi.tutorial.pharma_v0_adapter import PharmaV0Model


def _as_float_array(v, n: int | None = None) -> np.ndarray:
    """Accept pandas Series / list / scalar and return float ndarray."""
    if hasattr(v, "values"):
        arr = np.asarray(v.values, dtype=float)
    else:
        arr = np.asarray(v, dtype=float)

    # scalar -> length n
    if arr.ndim == 0:
        if n is None:
            return np.asarray([float(arr)], dtype=float)
        return np.full(n, float(arr), dtype=float)
    return arr.astype(float)


def _shade_where(ax, x: np.ndarray, mask: np.ndarray, *, alpha: float = 0.18) -> None:
    """Shade contiguous True segments on x-axis."""
    if mask.size == 0:
        return
    in_seg = False
    start = 0
    for i, m in enumerate(mask):
        if m and not in_seg:
            in_seg = True
            start = i
        elif not m and in_seg:
            in_seg = False
            ax.axvspan(start - 0.5, (i - 1) + 0.5, color="red", alpha=alpha, zorder=0)
    if in_seg:
        ax.axvspan(start - 0.5, (len(mask) - 1) + 0.5, color="red", alpha=alpha, zorder=0)


def plot_pharma_v0(model: PharmaV0Model, title: str = "Pharma Cold Chain V0 (Japan Domestic Planning)") -> None:
    """
    Pharma Cold Chain V0 plot (monthly) - single axis (no twinx).

    Demand-related lines (readability design):
      D      : market demand (light grey, thick + big marker)
      CO     : backlog/carryover (dark blue)
      CO + D : total need this month (carryover + demand) (dark red dashed)
      S_cap  : vaccination capacity "ceiling" (red, thin, marker "_")
      S      : vaccinations performed (navy, thin)

    Bars:
      Import supply (to DC) : gold-like (same family as Production in rice plot)
      Inventory (DC)        : brown
      Waste                 : orange-ish

    Visual helpers:
      - Shade periods where (CO + D) > S_cap (capacity gap)
      - Draw DC ceiling (storage limit) as dotted line (kept out of legend to reduce clutter)
    """
    months = list(model.months)
    n = len(months)
    x = np.arange(n)

    demand = _as_float_array(model.demand, n)
    sales = _as_float_array(model.sales, n)
    import_supply = _as_float_array(model.import_supply, n)
    waste = _as_float_array(model.waste, n)
    inv = _as_float_array(model.inventory, n)
    backlog = _as_float_array(model.backlog, n)
    s_cap = _as_float_array(model.vaccination_capacity, n)

    # CO + D
    total_need = backlog + demand

    fig, ax = plt.subplots(figsize=(14, 5))

    # --- Capacity gap shading: (CO+D) > S_cap ---
    gap_mask = total_need > s_cap
    _shade_where(ax, x, gap_mask, alpha=0.10)  # thin red veil

    # --- Bars (align like rice: left group, center group, right group) ---
    w = 0.24
    # Import supply (use "gold" to match rice's Production feel)
    ax.bar(x - w, import_supply, width=w, color="gold", alpha=0.65, label="Import supply (to DC)", zorder=2)
    # Waste
    ax.bar(x, waste, width=w, alpha=0.55, label="Waste (expired + overflow)", zorder=2)
    # Inventory
    ax.bar(x + w, inv, width=w, color="brown", alpha=0.55, label="Inventory (DC)", zorder=1)

    # --- Lines: order = story order ---
    # D (light gray, thick)
    ax.plot(
        x, demand,
        color="lightgrey",
        linewidth=3.0,
        marker="o",
        markersize=7,
        label="D: Demand (vaccination requests)",
        zorder=7,
    )

    # CO + D (dark red dashed)
    ax.plot(
        x, total_need,
        color="firebrick",
        linewidth=2.0,
        linestyle="--",
        marker=None,
        label="CO+D: Total need (carryover + demand)",
        zorder=6,
    )

    # S_cap (red, thin, marker "_" as ceiling tick)
    ax.plot(
        x, s_cap,
        color="red",
        linewidth=1.4,
        marker="_",
        markersize=14,
        label="S_cap: Vaccination capacity",
        zorder=5,
    )

    # S (navy, thin)  ←ご要望どおり darkBlue
    ax.plot(
        x, sales,
        color="navy",
        linewidth=1.6,
        marker="o",
        markersize=4,
        label="S: Vaccinations performed",
        zorder=8,
    )

    # CO (dark blue)
    ax.plot(
        x, backlog,
        color="darkblue",
        linewidth=2.2,
        marker="s",
        markersize=4,
        label="CO: Backlog / carryover",
        zorder=9,
    )

    # --- DC ceiling (storage limit) ---
    dc_cap = getattr(model, "dc_capacity", None)
    if dc_cap is not None:
        dc_cap_arr = _as_float_array(dc_cap, n)
        # if scalar -> constant line
        y = float(dc_cap_arr[0]) if dc_cap_arr.size > 0 else None
        if y is not None:
            ax.axhline(y, color="red", linestyle=":", linewidth=1.4, label="_nolegend_", zorder=3)

    ax.set_title(title)
    ax.set_xlabel("Month")
    ax.set_ylabel("Lots")

    # X ticks
    step = max(1, n // 12)
    ax.set_xticks(x[::step])
    ax.set_xticklabels([months[i] for i in range(0, n, step)], rotation=45, ha="right")

    # Legend: keep the reading order (already plotted in order, but bars were earlier)
    # -> reconstruct explicitly
    handles, labels = ax.get_legend_handles_labels()
    order = [
        "D: Demand (vaccination requests)",
        "CO+D: Total need (carryover + demand)",
        "S_cap: Vaccination capacity",
        "S: Vaccinations performed",
        "CO: Backlog / carryover",
        "Import supply (to DC)",
        "Waste (expired + overflow)",
        "Inventory (DC)",
    ]
    label_to_handle = {lab: h for h, lab in zip(handles, labels)}
    ordered_handles = [label_to_handle[l] for l in order if l in label_to_handle]
    ordered_labels = [l for l in order if l in label_to_handle]

    ax.legend(ordered_handles, ordered_labels, loc="upper left", framealpha=0.92)

    fig.tight_layout()
    plt.show()


def plot_pharma_v0_compact(model: PharmaV0Model, title: str = "Pharma Cold Chain V0 (Japan Domestic Planning)") -> None:
    """Compact variant (same styling rules)."""
    plot_pharma_v0(model, title=title)
