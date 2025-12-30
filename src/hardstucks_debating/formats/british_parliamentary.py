from typing import Dict, List
from hardstucks_debating.debate_strategy_impl import DebateFormatStrategyImpl
from hardstucks_debating.graph import Graph
from hardstucks_debating.debate_strategy import DebateFormatStrategy


class BritishParliamentaryFormat(DebateFormatStrategyImpl):
    """8-role British Parliamentary debate format strategy."""

    @property
    def role_map(self) -> List[str]:
        return ["PM", "LO", "DPM", "DLO", "GM", "MO", "GW", "OW"]

    @property
    def min_participants(self) -> int:
        return 8

    def build_graph(self, person_data: List[Dict]) -> Graph:
        """Build the flow network graph for British Parliamentary 8-role debate format."""
        P = len(person_data)
        N = P + 8 + 2  # P people + 8 roles + source + sink
        role_cap = P // 8

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

        # Handle uneven distribution (P % 8 modulo logic)
        mod = P % 8
        if mod == 0:
            pass
        elif mod < 4:
            # Add extra people to last role (OW)
            G.addEdge(N - 2, N - 1, role_cap + mod, 0)
        else:
            # Distribute extras across first 4 roles
            G.addEdge(N - 9, N - 1, role_cap + 1, 0)
            G.addEdge(N - 8, N - 1, role_cap + 1, 0)
            G.addEdge(N - 7, N - 1, role_cap + 1, 0)
            G.addEdge(N - 6, N - 1, role_cap + 1, 0)

            if mod >= 5:
                G.addEdge(N - 5, N - 1, role_cap + 1, 0)
                if mod >= 6:
                    G.addEdge(N - 4, N - 1, role_cap + 1, 0)
                    if mod == 7:
                        G.addEdge(N - 3, N - 1, role_cap + 1, 0)

        return G
