from typing import Dict, List
from graph import Graph
from debate_strategy import DebateFormatStrategy


class TraditionalDebateFormat(DebateFormatStrategy):
    """6-role traditional debate format strategy."""

    @property
    def role_map(self) -> List[str]:
        return ["1st Aff", "1st Neg", "2nd Aff", "2nd Neg", "3rd Aff", "3rd Neg"]

    @property
    def min_participants(self) -> int:
        return 6

    def build_graph(self, person_data: List[Dict]) -> Graph:
        """Build the flow network graph for traditional 6-role debate format."""
        P = len(person_data)
        N = P + 6 + 2  # P people + 6 roles + source + sink
        role_cap = P // 6

        # Create graph
        G = Graph(N)

        # Add edges from source (0) to each person (1 to P)
        for i in range(1, 1 + P):
            G.addEdge(0, i, 1, 0)
            costs = person_data[i - 1]["preferences"]

            # Add edges from person to each role
            for j in range(1 + P, N - 1):
                G.addEdge(i, j, 1, costs[j - P - 1])

        # Add edges from roles to sink with base capacity
        for i in range(1 + P, N - 1):
            G.addEdge(i, N - 1, role_cap, 0)

        # Handle uneven distribution (P % 6 modulo logic)
        mod = P % 6
        if mod == 0:
            pass
        elif mod < 4:
            # Add extra people to 3rd Neg (last role)
            G.addEdge(N - 2, N - 1, role_cap + mod, 0)
        else:
            # Distribute extras across multiple roles
            G.addEdge(N - 7, N - 1, role_cap + 1, 0)
            G.addEdge(N - 6, N - 1, role_cap + 1, 0)
            G.addEdge(N - 5, N - 1, role_cap + 1, 0)
            G.addEdge(N - 4, N - 1, role_cap + 1, 0)
            if mod == 5:
                G.addEdge(N - 3, N - 1, role_cap + 1, 0)

        return G
