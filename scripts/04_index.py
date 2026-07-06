import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.retrieval.pipeline import run_indexing

if __name__ == "__main__":
    run_indexing()
