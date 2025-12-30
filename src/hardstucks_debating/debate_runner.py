from hardstucks_debating.graph import Graph
from hardstucks_debating.debate_strategy import DebateFormatStrategy
from hardstucks_debating.debate_io import DebateIO


class DebateRunner:
    """Main orchestrator that runs debate assignment using a given strategy."""

    def __init__(self, strategy: DebateFormatStrategy):
        """Initialize with a debate format strategy."""
        self.strategy = strategy
        self.io = DebateIO()

    def display_banner(self) -> None:
        """Display application banner."""
        print(
            r"""

        _   _               _     _              _     ______     _           _   _
        | | | |             | |   | |            | |    |  _  \   | |         | | (_)
        | |_| | __ _ _ __ __| |___| |_ _   _  ___| | __ | | | |___| |__   __ _| |_ _ _ __   __ _
        |  _  |/ _` | '__/ _` / __| __| | | |/ __| |/ / | | | / _ \ '_ \ / _` | __| | '_ \ / _` |
        | | | | (_| | | | (_| \__ \ |_| |_| | (__|   <  | |/ /  __/ |_) | (_| | |_| | | | | (_| |
        \_| |_/\__,_|_|  \__,_|___/\__|\__,_|\___|_|\_\ |___/ \___|_.__/ \__,_|\__|_|_| |_|\__, |
                                                                                            __/ |
                                                                                           |___/
    """
        )

    def display_success(
        self, output_file: str, total_pref: int, num_participants: int
    ) -> None:
        """Display success message."""
        print(
            r"""

            _____                                 _
            / ____|                              | |
            | (___  _   _  ___ ___ ___  ___ ___  | |
            \___ \| | | |/ __/ __/ _ \/ __/ __|  | |
            ____) | |_| | (_| (_|  __/\__ \__ \  |_|
            |_____/ \__,_|\___\___\___||___/___/ (_)


    """
        )
        print(f"Output wrote to {output_file}")
        avg_pref = round(total_pref / num_participants, 3)
        print(
            f"On average people got their {total_pref}/{num_participants} = {avg_pref} choice"
        )

    def run(self) -> None:
        """Main execution flow."""

        # Step 1: Read input
        input_file = self.io.get_input_file()
        try:
            person_data = self.io.read_participant_data(input_file)
        except IOError as e:
            print(str(e))
            exit(1)
        except ValueError as e:
            print(f"CSV format error: {e}")
            exit(1)

        # Step 2: Validate minimum participants
        P = len(person_data)
        # if P < self.strategy.min_participants:
        #     print("Trivial Solution")
        #     exit(0)

        # Step 3: Get output file
        output_file = self.io.get_output_file()

        self.display_banner()

        # Step 4: Build flow graph using strategy
        G = self.strategy.build_graph(person_data)

        # Step 5: Run cycle-canceling algorithm
        resG = G.cycleCancel(0, len(G.graph) - 1)

        # Step 6: Generate rooms from graph
        rooms = self.strategy.generate_rooms(resG, P, person_data)

        # Step 8: Write output
        try:
            total_pref = self.io.write_room_assignments(output_file, rooms)
        except IOError as e:
            print(str(e))
            exit(1)

        # Step 9: Display success
        self.display_success(output_file, total_pref, P)
