"""
Core API for debate assignment solving.

This module provides a programmatic interface to the debate algorithm
that can be used as a library without CLI interaction.
"""

from enum import Enum
from typing import List, Dict, Tuple, Optional

from hardstucks_debating.graph import Graph
from hardstucks_debating.debate_strategy import DebateFormatStrategy
from hardstucks_debating.formats.traditional import TraditionalDebateFormat
from hardstucks_debating.formats.british_parliamentary import BritishParliamentaryFormat
from hardstucks_debating.formats.neo import NewTraditional


class DebateFormat(Enum):
    """Supported debate formats."""

    TRADITIONAL = "traditional"
    BRITISH_PARLIAMENTARY = "british_parliamentary"
    NEO = "neo"


class DebateSolution:
    """Result of a debate assignment solution."""

    def __init__(
        self,
        rooms: List[List[Tuple[str, str, int, Optional[str]]]],
        total_preference_score: int,
        num_participants: int,
    ):
        self.rooms = rooms
        self.total_preference_score = total_preference_score
        self.num_participants = num_participants
        self.average_preference = (
            round(total_preference_score / num_participants, 3)
            if num_participants > 0
            else 0
        )

    def to_dict(self) -> Dict:
        """Convert solution to dictionary format."""
        return {
            "rooms": [
                [
                    {
                        "name": person[0],
                        "role": person[1],
                        "preference": person[2],
                        "group": person[3] if len(person) > 3 else None,
                    }
                    for person in room
                ]
                for room in self.rooms
            ],
            "total_preference_score": self.total_preference_score,
            "num_participants": self.num_participants,
            "average_preference": self.average_preference,
        }

    def __repr__(self) -> str:
        return (
            f"DebateSolution(rooms={len(self.rooms)}, "
            f"participants={self.num_participants}, "
            f"avg_preference={self.average_preference})"
        )


def solve_debate_assignment(
    participants: List[Dict[str, any]],
    format: DebateFormat = DebateFormat.TRADITIONAL,
) -> DebateSolution:
    """
    Solve debate room assignment problem.

    This is the main programmatic API for the debate algorithm.

    Args:
        participants: List of participant dictionaries with structure:
            {
                "name": str,
                "preferences": List[int],  # Role preferences (1=most preferred)
                "group": List[str] or [],  # Optional group constraints (for neo format)
            }
        format: Debate format to use (TRADITIONAL, BRITISH_PARLIAMENTARY, or NEO)

    Returns:
        DebateSolution object containing room assignments and metrics

    Example:
        >>> participants = [
        ...     {"name": "Alice", "preferences": [1, 2, 3, 4, 5, 6], "group": []},
        ...     {"name": "Bob", "preferences": [2, 1, 4, 3, 6, 5], "group": []},
        ... ]
        >>> solution = solve_debate_assignment(participants, DebateFormat.TRADITIONAL)
        >>> print(solution.average_preference)
        1.5
    """
    # Select strategy based on format
    strategy_map = {
        DebateFormat.TRADITIONAL: TraditionalDebateFormat,
        DebateFormat.BRITISH_PARLIAMENTARY: BritishParliamentaryFormat,
        DebateFormat.NEO: NewTraditional,
    }

    strategy_class = strategy_map.get(format)
    if not strategy_class:
        raise ValueError(f"Unknown debate format: {format}")

    strategy = strategy_class()

    # Build flow graph
    G = strategy.build_graph(participants)

    # Run cycle-canceling algorithm
    resG = G.cycleCancel(0, len(G.graph) - 1)

    # Generate rooms
    P = len(participants)
    rooms = strategy.generate_rooms(resG, P, participants)

    # Calculate total preference score
    total_pref = sum(person[2] for room in rooms for person in room)

    return DebateSolution(rooms, total_pref, P)
