"""Data files and configurations"""

import json
from pathlib import Path

# Load mood mapping data
MOOD_MAPPING_FILE = Path(__file__).parent / "mood_mapping.json"

def load_mood_mapping():
    """Load mood mapping configuration from JSON file"""
    with open(MOOD_MAPPING_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

__all__ = ["load_mood_mapping", "MOOD_MAPPING_FILE"]

