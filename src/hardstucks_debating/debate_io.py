import csv
import os
from typing import Iterable, List, Dict, Tuple, Optional
import inquirer


class DebateIO:
    """Handles CSV input/output operations for debate assignments."""

    @staticmethod
    def read_participant_data(file_path: str) -> List[Dict]:
        """
        Read participant preferences from CSV file.

        CSV format:
        - First column: Name
        - Middle columns: Role preferences (integers)
        - Last column (optional): Group

        Args:
            file_path: Path to input CSV file

        Returns:
            List of dictionaries with 'name', 'preferences', and optionally 'group' keys

        Raises:
            IOError: If file cannot be read
            ValueError: If CSV format is invalid
        """
        data = []
        try:
            with open(file_path, "r") as file:
                csv_reader = csv.reader(file, delimiter=",")
                line_count = 0
                header = None
                has_group_column = False

                for row in csv_reader:
                    if line_count == 0:
                        # Check header for "Group" column
                        header = row
                        has_group_column = header[-1].lower() == "group"
                    else:
                        # Parse data row
                        name = row[0]

                        if has_group_column:
                            # Last column is group, middle columns are preferences
                            preferences = [int(x) for x in row[1:-1]]
                            group = row[-1]
                            person = {
                                "name": name,
                                "preferences": preferences,
                                "group": [] if len(group) == 0 else group.split(","),
                            }
                        else:
                            # All columns after name are preferences
                            preferences = [int(x) for x in row[1:]]
                            person = {
                                "name": name,
                                "preferences": preferences,
                                "group": [],
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
        file_path: str, rooms: List[List[Tuple[str, str, int, str | None]]]
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
            with open(file_path, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Name", "Role", "Role preferenced at number, Group"])

                for i, room in enumerate(rooms):
                    writer.writerow([f"Room {i + 1}"])
                    for row in room:
                        writer.writerow(row)
                        total_pref += row[2]
        except IOError as e:
            raise IOError(f"Failed to write output file: {e}")

        return total_pref

    @staticmethod
    def get_input_file(default: Optional[str] = None) -> str:
        """
        Prompt user for input file name using inquirer.

        Args:
            default: Optional default file path to use

        Returns:
            Selected input file path
        """
        if default:
            return default

        # Get list of CSV files in current directory and examples/ subdirectory
        csv_files = []
        for directory in [".", "examples"]:
            if os.path.isdir(directory):
                files = [
                    os.path.join(directory, f)
                    for f in os.listdir(directory)
                    if f.endswith(".csv")
                ]
                csv_files.extend(files)

        # Add option to enter custom path
        choices = sorted(csv_files) + ["[Enter custom path]"]

        questions = [
            inquirer.List(
                "file",
                message="Select input file",
                choices=choices,
            ),
        ]
        answers = inquirer.prompt(questions)

        if answers["file"] == "[Enter custom path]":
            custom_questions = [
                inquirer.Text(
                    "custom_file",
                    message="Enter the path to the input file",
                ),
            ]
            custom_answers = inquirer.prompt(custom_questions)
            return custom_answers["custom_file"]

        return answers["file"]

    @staticmethod
    def get_output_file(default: Optional[str] = None) -> str:
        """
        Prompt user for output file name using inquirer.

        Args:
            default: Optional default file path to use

        Returns:
            Output file path (guaranteed to end with .csv)
        """
        if default:
            if not default.endswith(".csv"):
                return default + ".csv"
            return default

        questions = [
            inquirer.Text(
                "file",
                message="Enter the output file name",
            ),
        ]
        answers = inquirer.prompt(questions)
        output_file = answers["file"]

        if not output_file.endswith(".csv"):
            output_file += ".csv"

        return output_file

    @staticmethod
    def get_debate_format(default: Optional[str] = None) -> str:
        """
        Prompt user to select debate format using arrow keys.

        Args:
            default: Optional default format ('traditional', 'british_parliamentary', or 'neo')

        Returns:
            Selected format name: 'traditional', 'british_parliamentary', or 'neo'
        """
        if default:
            return default

        questions = [
            inquirer.List(
                "format",
                message="Select debate format",
                choices=[
                    ("Traditional (6 roles)", "traditional"),
                    ("British Parliamentary (8 roles)", "british_parliamentary"),
                    ("Neo (6 roles with room nodes)", "neo"),
                ],
            ),
        ]
        answers = inquirer.prompt(questions)
        return answers["format"]
