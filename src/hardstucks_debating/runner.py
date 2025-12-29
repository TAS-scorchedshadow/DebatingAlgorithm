"""
Legacy runner module for backwards compatibility.

This wraps the original DebateRunner class.
"""

from hardstucks_debating.debate_runner import DebateRunner as _DebateRunner

# Re-export for backwards compatibility
DebateRunner = _DebateRunner

__all__ = ["DebateRunner"]
