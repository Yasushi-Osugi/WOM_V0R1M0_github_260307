# scripts/run_wom_visualizer.py

# ****
# a simple starter
# ****
#from __future__ import annotations
#
#from apps.wom_visualizer_app import app
#
#
#if __name__ == "__main__":
#    app.run(debug=True)

# ****
# recommend starter
# ****

# ****
# setting change
# ****
#set WOM_DEBUG=0
#set WOM_PORT=8060
#python scripts\run_wom_visualizer.py


from __future__ import annotations

import os

from apps.wom_visualizer_app import app


def main() -> None:
    debug = os.getenv("WOM_DEBUG", "1") == "1"
    host = os.getenv("WOM_HOST", "127.0.0.1")
    port = int(os.getenv("WOM_PORT", "8050"))

    app.run(
        debug=debug,
        host=host,
        port=port,
    )


if __name__ == "__main__":
    main()
