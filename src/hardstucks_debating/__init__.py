"""
Debate Algorithm Package

A Python package for optimizing debate room assignments using min-cost max-flow algorithms.
"""

from hardstucks_debating.core import solve_debate_assignment, DebateFormat
from hardstucks_debating.runner import DebateRunner

__version__ = "1.0.0"
__all__ = ["solve_debate_assignment", "DebateFormat", "DebateRunner"]
