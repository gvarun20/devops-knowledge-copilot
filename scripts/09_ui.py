#!/usr/bin/env python
"""Optional: Streamlit UI for local experiments only.

Production UI: docs/index.html (GitHub Pages + nginx in docker compose).
See docs/OPERATIONS.md for the standard workflow.
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app" / "streamlit_app.py"


def main() -> None:
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", str(APP), "--server.headless", "true"],
        cwd=ROOT,
        check=True,
    )


if __name__ == "__main__":
    main()
