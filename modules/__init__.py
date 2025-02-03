# modules/__init__.py

from .scan import scan_reseau
from .wan import test_latence
from .db import Database
from .install import setup
from .dashboard import Dashboard

__all__ = ["scan_reseau", "test_latence", "Database", "setup", "Dashboard"]