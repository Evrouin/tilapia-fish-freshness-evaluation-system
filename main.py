#!/usr/bin/env python3
"""
Tilapia Fish Freshness Evaluation System

Main entry point for the application.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from tilapia_freshness.gui.main_window import main


if __name__ == "__main__":
    main()
