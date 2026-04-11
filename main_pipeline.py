 #!/usr/bin/env python3
"""
Main Movie Data Pipeline - End-to-End Execution
Runs: scrape → clean → enrich
"""

import os
import sys
from pathlib import Path

def run_step(step_name, command):
    print(f"🚀 Running {step_name}...")
    os.system(command)
    print(f"✅ {step_name} complete!")

if __name__ == "__main__":
    print("🎬 Movie Data Pipeline Starting...")
    
    # Check API key (optional now)
    api_key = os.getenv('TMDb_API_KEY')
    if not api_key:
        print("⚠️ No TMDb_API_KEY - skipping enrichment step (add to .env for full features)")
        ENRICH = False
    else:
        ENRICH = True
        print("✅ TMDb API ready")
    
    # 1. Scrape
    run_step("Scrape Wikipedia", "python scripts/scrape_wikipedia.py")
    
    # 2. Clean
    run_step("Clean Data", "python scripts/clean_movies_data.py")
    
    # 3. Enrich (optional)
    if ENRICH:
        run_step("Enrich with TMDb", "python scripts/enrich_movies.py")
    else:
        print("⏭️ Skipping enrichment (no API key)")
    
    print("🎉 Pipeline Complete!")
    print("📁 Check data/enriched/movies_enriched_2025_hindi.csv")

