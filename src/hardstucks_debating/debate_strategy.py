from abc import ABC, abstractmethod
from typing import Dict, List, Tuple
from hardstucks_debating.graph import Graph
import random


class DebateFormatStrategy(ABC):
    """Abstract base class for debate format strategies."""

    @abstractmethod
    def build_graph(self, person_data: List[Dict]) -> Graph:
        """
        Build the flow network graph for this debate format.

        Args:
            person_data: List of person dictionaries with 'name' and 'preferences'

        Returns:
            Graph configured for this debate format with all edges and capacities set
        """

    @abstractmethod
    def generate_rooms(
        self, result_graph: Graph, num_participants: int, person_data: List[Dict]
    ) -> List[List[Tuple[str, str, int, str | None]]]:
        """
        Extract role assignments from the flow graph and generate room allocations.

        Args:
            result_graph: The graph after running cycle-canceling algorithm
            num_participants: Number of participants
            person_data: List of person dictionaries with 'name' and 'preferences'

        Returns:
            List of rooms, each containing (name, role, preference) tuples
        """
