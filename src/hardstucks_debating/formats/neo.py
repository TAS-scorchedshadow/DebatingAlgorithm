from typing import Dict, List, Set
from hardstucks_debating.debate_strategy import DebateFormatStrategy
from hardstucks_debating.debate_io import Room
from hardstucks_debating.graph import Graph


# This is the original file that group_aware_impl is based off not used in the codebase
class NewTraditional(DebateFormatStrategy):
    """6-role traditional debate format strategy with group support."""

    def build_graph(self, person_data: List[Dict]) -> Graph:
        """Build the flow network graph using role-room pair nodes with group constraints."""
        P = len(person_data)

        # Identify groups in the dataset
        groups = self._identify_groups(person_data)

        # Calculate room allocations: list of (timeslot, room_size) tuples
        room_allocations = self._calculate_room_allocations(person_data, groups)

        total_rooms = len(room_allocations)

        # Graph structure: SOURCE → PERSONS → ROLE-ROOM-PAIRS → SINK
        # We have 6 roles and total_rooms, with rooms dedicated to groups
        n_pairs = 6 * total_rooms
        N = 1 + P + n_pairs + 1  # source + P people + role-room pairs + sink

        # Create graph
        G = Graph(N)

        # Node indices:
        # 0: source
        # 1 to P: persons
        # P+1 to P+n_pairs: role-room pairs
        # N-1: sink

        # Add edges from source to each person (capacity 1)
        for i in range(1, 1 + P):
            G.addEdge(0, i, 1, 0)

        # Create role-room pairs and map them to groups
        role_room_group_map = {}  # Maps (role, room_idx) to group

        # Create rooms based on allocations
        for room_idx, (timeslot, room_size) in enumerate(room_allocations):
            for role in range(6):
                role_room_group_map[(role, room_idx)] = timeslot

        # Add edges from persons to role-room pairs (capacity 1, cost based on preference)
        for person_idx in range(P):
            person_node = person_idx + 1
            person = person_data[person_idx]
            person_groups = person.get("group", [])
            # Filter out empty strings from group list
            person_groups = [g.strip() for g in person_groups if g.strip()]

            costs = person["preferences"]

            # Connect to compatible role-room pairs
            for room in range(total_rooms):
                for role in range(6):
                    role_room_node = P + 1 + (room * 6) + role
                    assigned_group = role_room_group_map.get((role, room))

                    # Person can connect to a room if:
                    # 1. Person has no groups (empty list) → can connect to ANY room
                    # 2. Room is assigned to one of the person's groups
                    can_connect = False
                    if len(person_groups) == 0:
                        # Generic person can go to any room
                        can_connect = True
                    else:
                        # Check if room's group is in person's group list
                        can_connect = assigned_group in person_groups

                    if can_connect:
                        G.addEdge(person_node, role_room_node, 1, costs[role])

        # Add edges from role-room pairs to sink
        # Set capacity based on room size: most roles get capacity 1,
        # but the last role (3rd Neg) gets extra capacity for doubleups
        for room_idx, (timeslot, room_size) in enumerate(room_allocations):
            for role in range(6):
                pair_idx = room_idx * 6 + role
                role_room_node = P + 1 + pair_idx

                # Determine capacity for this role based on room size
                if room_size <= 6:
                    # Room has 6 or fewer people: each role gets capacity 1
                    # The flow algorithm will naturally fill only room_size roles
                    capacity = 1 if role < room_size else 0
                else:
                    # Room has more than 6 people: need doubleups on last role
                    if role == 5:  # Last role (3rd Neg)
                        # Room size 7 → capacity 2 (5 roles with 1 + last role with 2)
                        # Room size 8 → capacity 3 (5 roles with 1 + last role with 3)
                        capacity = room_size - 5
                    else:
                        # Other roles: capacity 1
                        capacity = 1

                G.addEdge(role_room_node, N - 1, capacity, 0)

        return G

    def _identify_groups(self, person_data: List[Dict]) -> Set[str]:
        """Identify all unique non-empty groups in person_data."""
        groups = set()
        for person in person_data:
            person_groups = person.get("group", [])
            # Add all non-empty groups from this person's list
            for group in person_groups:
                group = group.strip()
                if group:
                    groups.add(group)

        # If no groups found, create a default "General" timeslot
        if len(groups) == 0:
            groups.add("General")

        return groups

    def _calculate_room_allocations(
        self, person_data: List[Dict], groups: Set[str]
    ) -> List[tuple[str, int]]:
        """
        Calculate room allocations with specific sizes.

        Strategy (Timeslot-based):
        - Each group represents a timeslot
        - Maximize rooms with exactly 6 people
        - Distribute generic people to fill timeslots to multiples of 6 when possible
        - Only create smaller rooms (4-5 people) for leftovers

        Returns:
            List of (timeslot, room_size) tuples where:
            - timeslot: The group/timeslot name
            - room_size: Number of people in this specific room (e.g., 6, 7 with doubleup, etc.)
        """
        # Count group-specific people (those who can only go to specific timeslots)
        group_counts = {group: 0 for group in groups}
        flexible_people = []  # People with flexibility in timeslot choice

        for person in person_data:
            person_groups = person.get("group", [])
            person_groups = [g.strip() for g in person_groups if g.strip()]

            if len(person_groups) == 0:
                # Generic people can attend any timeslot
                flexible_people.append(list(groups))
            elif len(person_groups) == 1:
                # Single group - definitely count them
                group = person_groups[0]
                if group in groups:
                    group_counts[group] += 1
            else:
                # Multiple groups - save for flexible allocation
                flexible_people.append(person_groups)

        # Allocate flexible people (multi-group and generic) to timeslots
        # Strategy: Assign each person to help fill timeslots to multiples of 6
        # Prefer timeslots that already have people (avoid creating new timeslots)
        def allocate_flexible_person(person_valid_groups):
            """Allocate one flexible person to the best timeslot."""
            # Find valid groups that this person can attend
            valid_groups = [g for g in person_valid_groups if g in groups]
            if not valid_groups:
                return

            # Filter to groups with existing people (avoid creating new timeslots)
            active_groups = [g for g in valid_groups if group_counts[g] > 0]

            if active_groups:
                # Assign to active group that's closest to next multiple of 6
                # Priority: fill to 6, 12, 18, etc.
                def distance_to_next_multiple_of_6(g):
                    count = group_counts[g]
                    mod = count % 6
                    return 6 - mod if mod > 0 else 6  # Distance to next multiple

                best_group = min(active_groups, key=distance_to_next_multiple_of_6)
                group_counts[best_group] += 1
            else:
                # No active groups available, assign to first preference
                group_counts[valid_groups[0]] += 1

        # First pass: Fill timeslots to multiples of 6 (greedy approach)
        # Sort flexible people by number of options (fewer options = higher priority)
        flexible_people.sort(key=len)

        for person_valid_groups in flexible_people:
            allocate_flexible_person(person_valid_groups)

        # Calculate rooms with specific sizes per timeslot
        rooms = []  # List of (timeslot, room_size) tuples

        for group in sorted(groups):
            count = group_counts.get(group, 0)
            if count == 0:
                continue

            # Calculate how many full rooms of 6 and remainder
            base_rooms = count // 6
            mod = count % 6

            # Add full rooms of 6
            for _ in range(base_rooms):
                rooms.append((group, 6))

            # Handle remainder
            if mod > 0:
                if mod <= 3:
                    # Can fit extras via doubleup in last room (if we have rooms)
                    if base_rooms > 0:
                        # Replace last room with 6+mod
                        rooms[-1] = (group, 6 + mod)
                    else:
                        # Only room is smaller than 6
                        rooms.append((group, mod))
                else:
                    # Need additional room for 4 or 5 people
                    rooms.append((group, mod))

        return rooms

    def generate_rooms(self, result_graph, num_participants, person_data):
        """
        Generate room allocations from the result graph.

        Graph structure: SOURCE(0) → PERSONS(1 to P) → ROLE-ROOM-PAIRS(P+1 to P+6*n_rooms) → SINK(N-1)
        """
        P = num_participants
        role_map = ["1st Aff", "1st Neg", "2nd Aff", "2nd Neg", "3rd Aff", "3rd Neg"]

        # Identify groups and calculate room allocations
        groups = self._identify_groups(person_data)
        room_allocations = self._calculate_room_allocations(person_data, groups)
        total_rooms = len(room_allocations)

        # Initialize rooms
        rooms = [[] for _ in range(total_rooms)]

        # Extract assignments from the flow graph
        # Check each role-room pair to see which person was assigned (by checking reverse edges)
        n_pairs = 6 * total_rooms

        for pair_idx in range(n_pairs):
            role_room_node = P + 1 + pair_idx
            room = pair_idx // 6
            role = pair_idx % 6

            # Check each person to see if they have a reverse edge from this role-room pair
            # (meaning flow went from person to role-room)
            for person_idx in range(P):
                person_node = person_idx + 1

                # In residual graph, if flow went person→role-room,
                # then there's a reverse edge role-room→person with capacity
                reverse_capacity = result_graph.getFlowCapacity(
                    role_room_node, person_node
                )

                if reverse_capacity > 0:
                    # This person was assigned to this role-room pair
                    person = person_data[person_idx]
                    preference = person["preferences"][role]
                    person_groups = person.get("group", [])
                    # Join groups with comma for CSV output
                    group_str = ",".join(person_groups) if person_groups else ""

                    rooms[room].append(
                        (person["name"], role_map[role], preference, group_str)
                    )

        # Filter out empty rooms and create Room objects
        rooms_with_data = []
        for room_idx, room in enumerate(rooms):
            if len(room) > 0:  # Only include non-empty rooms
                # Create room name with timeslot
                timeslot = room_allocations[room_idx][0]
                room_name = f"Room {len(rooms_with_data) + 1} ({timeslot})"
                rooms_with_data.append(Room(name=room_name, assignments=room))

        return rooms_with_data
