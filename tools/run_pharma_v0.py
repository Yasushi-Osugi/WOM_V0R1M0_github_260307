#tools/run_pharma_v0.py

# 起動方法
# python -m tools.run_pharma_v0 --data_dir data/pharma_cold_v0


from __future__ import annotations

from pysi.tutorial.pharma_v0_adapter import load_pharma_v0
from pysi.tutorial.plot_pharma_v0 import plot_pharma_v0


def main() -> None:
    # Default data dir for tutorial
    data_dir = "data/pharma_cold_v0"

    # Parameters (V0 fixed by tutorial spec)
    dc_capacity = 300
    shelf_life = 3

    m = load_pharma_v0(
        data_dir,
        dc_capacity=dc_capacity,
        shelf_life=shelf_life,
    )

    #plot_pharma_v0(m, title="Pharma Cold Chain V0 (Japan Domestic Planning)")
    plot_pharma_v0(model, title="Pharma Cold Chain V0 (Japan Domestic Planning)")

if __name__ == "__main__":
    main()
