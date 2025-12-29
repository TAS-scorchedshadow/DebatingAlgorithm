from copy import deepcopy
from collections import deque
import sys


class Graph:
    """
    Graph representation for minimum-cost maximum-flow algorithms.

    Uses an adjacency matrix where each cell contains a tuple (capacity, cost).
    Supports flow network algorithms including Edmonds-Karp and cycle-canceling.

    Attributes:
        V: Number of vertices in the graph
        graph: 2D adjacency matrix where graph[i][j] = (capacity, cost)
    """

    def __init__(self, vertices: int) -> None:
        """
        Initialize a graph with the given number of vertices.

        Args:
            vertices: Number of vertices in the graph

        Raises:
            ValueError: If vertices is not positive
        """
        if vertices <= 0:
            raise ValueError("Number of vertices must be positive")
        self.V = vertices
        self.graph = [[(0, 0) for col in range(vertices)] for row in range(vertices)]

    def printGraph(self) -> None:
        """
        Print the graph node by node with incoming and outgoing edges.

        Shows each node's incoming and outgoing edges with (capacity, cost) information.
        """
        print("\n=== Graph Structure (Node by Node) ===")
        for node in range(self.V):
            print(f"\nNode {node}:")

            # Outgoing edges
            outgoing = []
            for dest in range(self.V):
                capacity, cost = self.graph[node][dest]
                if capacity > 0:
                    outgoing.append(f"  -> {dest} (cap={capacity}, cost={cost})")

            if outgoing:
                print("  Outgoing edges:")
                for edge in outgoing:
                    print(edge)
            else:
                print("  Outgoing edges: None")

            # Incoming edges
            incoming = []
            for src in range(self.V):
                capacity, cost = self.graph[src][node]
                if capacity > 0:
                    incoming.append(f"  <- {src} (cap={capacity}, cost={cost})")

            if incoming:
                print("  Incoming edges:")
                for edge in incoming:
                    print(edge)
            else:
                print("  Incoming edges: None")

        print("\n" + "="*40 + "\n")

    def addEdge(self, v: int, w: int, capacity: int, cost: int) -> None:
        """
        Add a directed edge from vertex v to vertex w.

        Args:
            v: Source vertex index
            w: Destination vertex index
            capacity: Maximum flow capacity of the edge
            cost: Cost per unit of flow on the edge

        Raises:
            ValueError: If vertices are out of bounds or capacity/cost are negative
        """
        if v < 0 or v >= self.V or w < 0 or w >= self.V:
            raise ValueError(f"Vertices ({v}, {w}) out of bounds [0, {self.V})")
        if capacity < 0:
            raise ValueError(f"Capacity must be non-negative, got {capacity}")
        # print(f"Adding an edge between {v} and {w} - ({capacity}, {cost})")
        self.graph[v][w] = (capacity, cost)

    def BFS(self, s: int, t: int, parent: list[int]) -> bool:
        """
        Breadth-first search to find an augmenting path from source to sink.

        Used by the Edmonds-Karp algorithm to find paths with available capacity.
        Updates the parent array to track the path from source to sink.

        Args:
            s: Source vertex index
            t: Sink (target) vertex index
            parent: List to store parent of each vertex in the BFS tree

        Returns:
            True if a path from source to sink exists with available capacity,
            False otherwise

        Raises:
            ValueError: If source or sink vertices are out of bounds
        """
        if s < 0 or s >= self.V or t < 0 or t >= self.V:
            raise ValueError(f"Source ({s}) or sink ({t}) out of bounds [0, {self.V})")

        visited = [False] * self.V

        queue = deque()
        queue.append(s)
        visited[s] = True

        while queue:
            u = queue.popleft()
            for i, val in enumerate(self.graph[u]):
                if not visited[i] and val[0] > 0:
                    queue.append(i)
                    visited[i] = True
                    parent[i] = u
                    if i == t:
                        return True

        return False

    def bellman_ford(self, source: int) -> list[tuple[int, int]] | None:
        """
        Detect negative cost cycles in the residual graph using Bellman-Ford algorithm.

        Used in the cycle-canceling algorithm to find negative cost cycles that
        can be used to reduce the total cost of the flow while maintaining the
        maximum flow value.

        Args:
            source: Source vertex index to start the algorithm

        Returns:
            List of edges (u, v) forming a negative cost cycle if one exists,
            None if no negative cycle is found

        Raises:
            ValueError: If source is out of bounds or invalid graph structure detected
            RuntimeError: If cycle detection exceeds maximum iterations
        """
        if source < 0 or source >= self.V:
            raise ValueError(f"Source {source} out of bounds [0, {self.V})")

        n = self.V

        # Convert to list of edges (only edges with positive capacity)
        edges = []

        for u, row in enumerate(self.graph):
            for v, col in enumerate(row):
                flow, cost = col
                if flow > 0:
                    edges.append((u, v, cost))

        # Initialize distances and predecessors
        dist = [float("Inf")] * self.V
        prev = [-1 for _ in range(n)]
        dist[source] = 0
        prev[source] = source

        # Relax edges V-1 times (standard Bellman-Ford)
        for _ in range(1, self.V):
            for edge in edges:
                u, v, cost = edge
                tempdist = float("Inf")
                if dist[u] != float("Inf"):
                    tempdist = dist[u] + cost
                if dist[v] > tempdist:
                    dist[v] = tempdist
                    prev[v] = u

        # Check for negative cycles
        cycle = []
        for edge in edges:
            u, v, cost = edge
            if dist[u] != float("Inf") and dist[u] + cost < dist[v]:
                temp = (u, v)

                max_iterations = self.V
                iterations = 0
                # Trace back to find the cycle
                while temp not in cycle and iterations < max_iterations:
                    cycle.append(temp)
                    prev_node = prev[temp[0]]

                    # Bounds check
                    if prev_node < 0 or prev_node >= self.V:
                        raise ValueError(
                            f"Invalid predecessor node {prev_node} for vertex {temp[0]}"
                        )

                    temp = (prev_node, temp[0])
                    iterations += 1
                    if self.graph[prev_node][temp[1]][0] == 0:
                        raise ValueError(
                            f"Zero capacity edge ({prev_node}, {temp[1]}) in cycle detection"
                        )

                if iterations >= max_iterations:
                    raise RuntimeError(
                        f"Exceeded maximum iterations ({max_iterations}) while detecting cycle"
                    )

                # Extract only the cycle portion (temp is start of cycle)
                cycle = []
                iterations = 0
                while temp not in cycle and iterations < max_iterations:
                    cycle.append(temp)
                    temp = (prev[temp[0]], temp[0])
                    iterations += 1

                if iterations >= max_iterations:
                    raise RuntimeError(
                        f"Exceeded maximum iterations ({max_iterations}) while extracting cycle"
                    )

                return cycle
        return None

    def edmondsKarp(self, source: int, sink: int) -> int:
        """
        Compute maximum flow from source to sink using Edmonds-Karp algorithm.

        This is an implementation of the Ford-Fulkerson method that uses BFS to
        find augmenting paths, guaranteeing O(VE²) time complexity. Modifies the
        graph in-place to create a residual graph.

        Args:
            source: Source vertex index
            sink: Sink vertex index

        Returns:
            Maximum flow value from source to sink

        Raises:
            ValueError: If source or sink are out of bounds or equal

        Note:
            This method modifies the graph in-place. The graph becomes a residual
            graph after execution, with forward edges reduced and backward edges
            increased based on the flow.
        """
        if source < 0 or source >= self.V or sink < 0 or sink >= self.V:
            raise ValueError(
                f"Source ({source}) or sink ({sink}) out of bounds [0, {self.V})"
            )
        if source == sink:
            raise ValueError("Source and sink must be different vertices")

        predecessor = [-1] * self.V
        max_flow = 0

        while self.BFS(source, sink, predecessor):
            # Find minimum capacity along the augmenting path
            path_flow = float("Inf")
            s = sink

            while s != source:
                path_flow = min(path_flow, self.graph[predecessor[s]][s][0])
                s = predecessor[s]

            max_flow += path_flow

            # Update residual capacities along the path
            v = sink
            while v != source:
                u = predecessor[v]
                # Reduce forward edge capacity
                self.graph[u][v] = (
                    self.graph[u][v][0] - path_flow,
                    self.graph[u][v][1],
                )
                # Increase backward edge capacity (reverse flow)
                self.graph[v][u] = (
                    self.graph[v][u][0] + path_flow,
                    -self.graph[u][v][1],
                )
                v = predecessor[v]
        return max_flow

    def ensureCorrectCosts(self, originalGraph: "Graph") -> None:
        """
        Restore correct edge costs from the original graph.

        After flow operations, edge costs need to be corrected based on the original
        graph. Backward edges (created during flow) get negative costs of their
        corresponding forward edges.

        Args:
            originalGraph: The original graph with correct cost values

        Note:
            This method modifies the graph in-place. Used in cycle-canceling to
            maintain correct costs while updating flow values.
        """
        costs = originalGraph.graph
        for i, row in enumerate(self.graph):
            for j, col in enumerate(row):
                # Locating backwards edges (did not exist in the original graph)
                if col[0] != 0 and costs[i][j][0] == 0:
                    # Backward edge: use negative cost of reverse edge
                    self.graph[i][j] = (self.graph[i][j][0], -costs[j][i][1])
                else:
                    # Forward edge: use original cost
                    self.graph[i][j] = (self.graph[i][j][0], costs[i][j][1])

    def cycleCancel(self, source: int, sink: int) -> "Graph":
        """
        Compute minimum-cost maximum-flow using the cycle-canceling algorithm.

        This algorithm works in two phases:
        1. Find maximum flow using Edmonds-Karp (ignoring costs)
        2. Iteratively find and cancel negative cost cycles to reduce total cost
           while maintaining the maximum flow value

        The algorithm terminates when no negative cost cycles exist in the
        residual graph, guaranteeing an optimal minimum-cost maximum-flow.

        Args:
            source: Source vertex index
            sink: Sink vertex index

        Returns:
            A new Graph object containing the optimal flow with minimum cost

        Raises:
            ValueError: If source or sink are invalid
            RuntimeError: If cycle detection fails

        Note:
            This method creates a deep copy of the graph and does not modify
            the original. The returned graph contains the residual network with
            optimal flow.

        Complexity:
            O(E * U * C) where U is max flow value and C is max cost magnitude
        """
        if source < 0 or source >= self.V or sink < 0 or sink >= self.V:
            raise ValueError(
                f"Source ({source}) or sink ({sink}) out of bounds [0, {self.V})"
            )
        if source == sink:
            raise ValueError("Source and sink must be different vertices")

        # Create a working copy to avoid modifying the original graph
        G = deepcopy(self)

        # Phase 1: Compute maximum flow
        G.edmondsKarp(source, sink)

        # Ensure costs are correct in the residual graph
        G.ensureCorrectCosts(self)

        # Phase 2: Cancel negative cost cycles
        cycle = G.bellman_ford(sink)

        while cycle is not None:
            # Find the minimum flow capacity along the cycle
            flow = min(G.graph[u][v][0] for u, v in cycle)

            # Push flow around the cycle
            for u, v in cycle:
                current_flow, _ = G.graph[u][v]
                reverse_flow, _ = G.graph[v][u]
                original_cost = self.graph[u][v][1]
                reverse_cost = self.graph[v][u][1]

                # Update flow along the cycle
                G.graph[u][v] = (current_flow - flow, original_cost)
                G.graph[v][u] = (reverse_flow + flow, reverse_cost)

            # Restore correct costs after flow update
            G.ensureCorrectCosts(self)

            # Look for another negative cost cycle
            cycle = G.bellman_ford(sink)

        return G

    def getOutgoingEdgesWithFlow(self, vertex: int) -> list[int]:
        """
        Get all vertices that have non-zero flow from the given vertex.

        Args:
            vertex: Source vertex index

        Returns:
            List of destination vertex indices with non-zero flow

        Raises:
            ValueError: If vertex is out of bounds
        """
        if vertex < 0 or vertex >= self.V:
            raise ValueError(f"Vertex {vertex} out of bounds [0, {self.V})")

        destinations = []
        for j, (capacity, cost) in enumerate(self.graph[vertex]):
            if capacity > 0:
                destinations.append(j)
        return destinations

    def getFlowCapacity(self, u: int, v: int) -> int:
        """
        Get the flow capacity on edge from u to v.

        Args:
            u: Source vertex
            v: Destination vertex

        Returns:
            Flow capacity (0 if no edge exists)

        Raises:
            ValueError: If vertices are out of bounds
        """
        if u < 0 or u >= self.V or v < 0 or v >= self.V:
            raise ValueError(f"Vertices ({u}, {v}) out of bounds")

        return self.graph[u][v][0]

    def hasFlow(self, u: int, v: int) -> bool:
        """
        Check if there is non-zero flow on edge from u to v.

        Args:
            u: Source vertex
            v: Destination vertex

        Returns:
            True if flow > 0, False otherwise

        Raises:
            ValueError: If vertices are out of bounds
        """
        if u < 0 or u >= self.V or v < 0 or v >= self.V:
            raise ValueError(f"Vertices ({u}, {v}) out of bounds")

        return self.graph[u][v][0] > 0
