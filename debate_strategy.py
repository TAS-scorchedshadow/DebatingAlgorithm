from abc import ABC, abstractmethod
from typing import Dict, List, Tuple
from graph import Graph


class DebateFormatStrategy(ABC):
    """Abstract base class for debate format strategies."""

    @property
    @abstractmethod
    def role_map(self) -> List[str]:
        """Return the list of role names for this format."""
        pass

    @property
    @abstractmethod
    def num_roles(self) -> int:
        """Return the number of roles in this format."""
        pass

    @property
    @abstractmethod
    def min_participants(self) -> int:
        """Return minimum number of participants needed."""
        pass

    @property
    @abstractmethod
    def last_role_index(self) -> int:
        """Return the index of the last role (for doubleups)."""
        pass

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

    @abstractmethod
    def extract_assignments_from_graph(
        self,
        result_graph: Graph,
        num_participants: int
    ) -> Dict[int, List[int]]:
        """
        Extract role assignments from the flow graph.

        Args:
            result_graph: The graph after running cycle-canceling algorithm
            num_participants: Number of participants

        Returns:
            Dictionary mapping role indices to lists of person indices
        """
        pass

    def generate_rooms(
        self,
        assignments: Dict[int, List[int]],
        person_data: List[Dict]
    ) -> List[List[Tuple[str, str, int]]]:
        """
        Generate room allocations from assignments.

        This method has identical logic in both formats except for the
        last_role_index parameter, so it can be implemented in the base class.

        Args:
            assignments: Dictionary mapping role indices to lists of person indices
            person_data: List of person dictionaries with 'name' and 'preferences'

        Returns:
            List of rooms, each containing (name, role, preference) tuples
        """
        n_rooms = len(assignments[0])
        rooms = [[] for _ in range(n_rooms)]

        for i, room in enumerate(rooms):
            should_break = False
            for role, person_list in assignments.items():
                if len(person_list) == 0:
                    should_break = True
                    break
                person_idx = person_list.pop(0)
                room.append((
                    person_data[person_idx]["name"],
                    self.role_map[role],
                    person_data[person_idx]["preferences"][role]
                ))

            if should_break:
                break

        # Handle doubleups in the last role
        i = 0
        last_role_idx = self.last_role_index
        while len(assignments[last_role_idx]) > 0:
            person_idx = assignments[last_role_idx].pop(0)
            rooms[i].append((
                person_data[person_idx]["name"],
                self.role_map[last_role_idx],
                person_data[person_idx]["preferences"][last_role_idx]
            ))
            i = (i + 1) % n_rooms

        return rooms
