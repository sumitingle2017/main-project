#!/usr/bin/env python
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT_DIR = ROOT / "shreeom_bhel" / "shreeom"
sys.path.insert(0, str(PROJECT_DIR))
os.chdir(PROJECT_DIR)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shreeom.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

