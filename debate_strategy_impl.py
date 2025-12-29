from abc import ABC, abstractmethod
from typing import Dict, List, Tuple
from debate_strategy import DebateFormatStrategy
from graph import Graph
import random


class DebateFormatStrategyImpl(DebateFormatStrategy, ABC):
    """Abstract base class for debate format strategies."""

    @property
    @abstractmethod
    def role_map(self) -> List[str]:
        """Return the list of role names for this format."""
        pass

    @property
    @abstractmethod
    def min_participants(self) -> int:
        """Return minimum number of participants needed."""
        pass

    @property
    def last_role_index(self) -> int:
        """
        Return the index of the last role (for doubleups).

        By default this is set to min_participants - 1, to avoid creating an extra room with 1 person


        """
        return self.min_participants - 1

    @abstractmethod
    def build_graph(self, person_data: List[Dict]) -> Graph:
        """
        Build the flow network graph for this debate format.

        Args:
            person_data: List of person dictionaries with 'name' and 'preferences'

        Returns:
            Graph configured for this debate format with all edges and capacities set
        """
        pass

    def generate_rooms(
        self, result_graph: Graph, num_participants: int, person_data: List[Dict]
    ) -> List[List[Tuple[str, str, int]]]:
        """
        Extract role assignments from the flow graph and generate room allocations.

        Args:
            result_graph: The graph after running cycle-canceling algorithm
            num_participants: Number of participants
            person_data: List of person dictionaries with 'name' and 'preferences'

        Returns:
            List of rooms, each containing (name, role, preference) tuples
        """
        # Extract assignments from graph
        assignments = {i: [] for i in range(self.min_participants)}
        N = num_participants + self.min_participants + 2

        for i in range(1 + num_participants, N - 1):
            destinations = result_graph.getOutgoingEdgesWithFlow(i)
            links = [j - 1 for j in destinations]
            # random.shuffle(links)
            assignments[i - num_participants - 1] = links

        # Generate rooms from assignments
        n_rooms = len(assignments[0])
        rooms = [[] for _ in range(n_rooms)]

        for i, room in enumerate(rooms):
            should_break = False
            for role, person_list in assignments.items():
                if len(person_list) == 0:
                    should_break = True
                    break
                person_idx = person_list.pop(0)
                room.append(
                    (
                        person_data[person_idx]["name"],
                        self.role_map[role],
                        person_data[person_idx]["preferences"][role],
                        person_data[person_idx]["group"],
                    )
                )

            if should_break:
                break

        # Handle doubleups in the last role
        i = 0
        last_role_idx = self.last_role_index
        while len(assignments[last_role_idx]) > 0:
            person_idx = assignments[last_role_idx].pop(0)
            rooms[i].append(
                (
                    person_data[person_idx]["name"],
                    self.role_map[last_role_idx],
                    person_data[person_idx]["preferences"][last_role_idx],
                    person_data[person_idx]["group"],
                )
            )
            i = (i + 1) % n_rooms

        return rooms
