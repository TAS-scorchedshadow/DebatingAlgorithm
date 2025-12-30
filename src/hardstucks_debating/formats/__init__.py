"""Debate format strategies for different debate styles."""

from hardstucks_debating.formats.traditional import TraditionalDebateFormat
from hardstucks_debating.formats.british_parliamentary import BritishParliamentaryFormat
from hardstucks_debating.formats.neo import NewTraditional
from hardstucks_debating.formats.traditional_ga import TraditionalGroupAware
from hardstucks_debating.formats.british_parliamentary_ga import (
    BritishParliamentaryGroupAware,
)

__all__ = [
    "TraditionalDebateFormat",
    "BritishParliamentaryFormat",
    "NewTraditional",
    "TraditionalGroupAware",
    "BritishParliamentaryGroupAware",
]
