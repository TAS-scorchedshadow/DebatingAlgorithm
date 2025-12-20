import csv
from typing import List, Dict, Tuple


class DebateIO:
    """Handles CSV input/output operations for debate assignments."""

    @staticmethod
    def read_participant_data(file_path: str) -> List[Dict]:
        """
        Read participant preferences from CSV file.

        Args:
            file_path: Path to input CSV file

        Returns:
            List of dictionaries with 'name' and 'preferences' keys

        Raises:
            IOError: If file cannot be read
            ValueError: If CSV format is invalid
        """
        data = []
        try:
            with open(file_path, 'r') as file:
                csv_reader = csv.reader(file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    if line_count != 0:
                        person = {
                            "name": row[0],
                            "preferences": [int(x) for x in row[1:]]
                        }
                        data.append(person)
                    line_count += 1
        except IOError:
            raise IOError(f"Input file not found: {file_path}")
        except (ValueError, IndexError) as e:
            raise ValueError(f"Invalid CSV format: {e}")

        return data

    @staticmethod
    def write_room_assignments(
        file_path: str,
        rooms: List[List[Tuple[str, str, int]]]
    ) -> int:
        """
        Write room assignments to CSV file.

        Args:
            file_path: Path to output CSV file
            rooms: List of rooms, each containing (name, role, preference) tuples

        Returns:
            Total preference score across all assignments

        Raises:
            IOError: If file cannot be written
        """
        total_pref = 0

        try:
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Name", "Role", "Role preferenced at number"])

                for i, room in enumerate(rooms):
                    writer.writerow([f"Room {i + 1}"])
                    for name, role, pref in room:
                        writer.writerow([name, role, pref])
                        total_pref += pref
        except IOError as e:
            raise IOError(f"Failed to write output file: {e}")

        return total_pref

    @staticmethod
    def get_input_file() -> str:
        """Prompt user for input file name."""
        return input("Please enter the name of the input file: ")

    @staticmethod
    def get_output_file() -> str:
        """Prompt user for output file name with validation."""
        output_file = input("Please provide a name for the output file: ")
        while not output_file.endswith(".csv"):
            print("Error - Output file must be .csv")
            output_file = input("Please provide a name for the output file: ")
        return output_file
