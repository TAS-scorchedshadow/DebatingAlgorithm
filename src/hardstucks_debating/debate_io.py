import csv
import os
from typing import Iterable, List, Dict, Tuple, Optional, NamedTuple
import inquirer


class Room(NamedTuple):
    """Represents a debate room with name and participant assignments."""

    name: str
    assignments: List[Tuple[str, str, int, str]]  # (name, role, preference, group)


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
                            pref_strings = row[1:-1]
                            group = row[-1]
                        else:
                            # All columns after name are preferences
                            pref_strings = row[1:]
                            group = ""

                        # Convert preferences, handling missing/empty values
                        preferences = []
                        for pref_str in pref_strings:
                            pref_str = pref_str.strip()
                            if pref_str == "":
                                # Missing preference - will fill in later
                                preferences.append(None)
                            else:
                                try:
                                    preferences.append(int(pref_str))
                                except ValueError:
                                    raise ValueError(
                                        f"Invalid preference value '{pref_str}' for participant '{name}'"
                                    )

                        # Fill in missing preferences with max + 1
                        valid_prefs = [p for p in preferences if p is not None]
                        if valid_prefs:
                            fill_value = max(valid_prefs) + 1
                        else:
                            # All preferences are missing, use a default
                            fill_value = 1

                        preferences = [
                            p if p is not None else fill_value for p in preferences
                        ]

                        person = {
                            "name": name,
                            "preferences": preferences,
                            "group": [] if len(group) == 0 else group.split(","),
                        }

                        data.append(person)
                    line_count += 1
        except IOError:
            raise IOError(f"Input file not found: {file_path}")
        except (ValueError, IndexError) as e:
            raise ValueError(f"Invalid CSV format: {e}")

        return data

    @staticmethod
    def write_room_assignments(file_path: str, rooms: List[Room]) -> int:
        """
        Write room assignments to CSV file.

        Args:
            file_path: Path to output CSV file
            rooms: List of Room objects with name and assignments

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

                for room in rooms:
                    writer.writerow([room.name])
                    for row in room.assignments:
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
            default: Optional default format

        Returns:
            Selected format name
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
                    (
                        "LEGACY: Traditional without groups (6 roles, ignore groups)",
                        "traditional_ignore_group",
                    ),
                    (
                        "LEGACY: British Parliamentary without groups (8 roles, ignore groups)",
                        "bp_ignore_group",
                    ),
                ],
            ),
        ]
        answers = inquirer.prompt(questions)
        return answers["format"]
