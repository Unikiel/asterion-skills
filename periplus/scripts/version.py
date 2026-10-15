#!/usr/bin/env python3
"""Read the canonical package release version without duplicating constants."""
from pathlib import Path

SKILL_VERSION = (Path(__file__).resolve().parent.parent / 'VERSION').read_text(encoding='ascii').strip()
SCHEMA_VERSION = '2.6.0'
