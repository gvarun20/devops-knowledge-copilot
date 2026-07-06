import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.ingest.parser import run_ingestion

if __name__ == "__main__":
    run_ingestion()
