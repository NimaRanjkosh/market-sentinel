import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ingestion import run_harvester
from src.pipeline import run_pipeline

def main():
    
    print("Application Starting...")
    # 1: Get Data
    run_harvester()
    # 2: Process Data
    run_pipeline()
    print("Cycle Complete.")

if __name__ == "__main__":
    main()