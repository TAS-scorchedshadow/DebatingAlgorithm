# Debate Algorithm

A Python package for optimizing debate room assignments using min-cost max-flow algorithms. Assigns debaters to teams and rooms based on their preferences while maximizing overall satisfaction.

## Features

- **Multiple Debate Formats**: Traditional (6 roles), British Parliamentary (8 roles), and Neo (group-based)
- **Optimization Algorithm**: Uses cycle-canceling min-cost max-flow for optimal assignments
- **Flexible Usage**: CLI tool, Python library, or programmatic API
- **Smart Room Distribution**: Automatically handles partial rooms and doubleups

## Installation

### From TestPyPI

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ Hardstucks-Debating
```

**Note:** The `--extra-index-url` is required to install dependencies from regular PyPI.

### From Source (Development)

```bash
cd DebatingAlgorithm
pip install -e .
```

This installs in editable mode, so code changes are immediately available.

See [INSTALLATION.md](INSTALLATION.md) for detailed installation instructions and troubleshooting.

## Usage

### 1. As a Python Library

Use the package programmatically in your own Python code:

```python
from debate_algorithm import solve_debate_assignment, DebateFormat

# Define participants with preferences
participants = [
    {"name": "Alice", "preferences": [1, 2, 3, 4, 5, 6], "group": []},
    {"name": "Bob", "preferences": [2, 1, 4, 3, 6, 5], "group": []},
    {"name": "Charlie", "preferences": [3, 4, 1, 2, 6, 5], "group": []},
    # ... more participants
]

# Solve the assignment
solution = solve_debate_assignment(participants, DebateFormat.TRADITIONAL)

# Access results
print(f"Average preference: {solution.average_preference}")
print(f"Total rooms: {len(solution.rooms)}")

# Get results as dictionary
results = solution.to_dict()
```

### 2. Command Line Interface

#### Interactive Mode
```bash
python main.py
```

#### CLI Mode with Arguments
```bash
# Traditional format
python main.py -i examples/input.csv -o output.csv -f traditional

# British Parliamentary format
python main.py -i examples/bpin.csv -o output.csv -f bp

# Neo format (with group constraints)
python main.py -i tests/input_with_groups.csv -o output.csv -f neo
```

#### Using installed CLI command
If you installed the package with `pip install -e .`:
```bash
debate-solver -i input.csv -o output.csv -f traditional
```

## Debate Formats

### Traditional (6 roles)
Standard debate format with 6 roles:
- 1st Affirmative Speaker
- 1st Negative Speaker
- 2nd Affirmative Speaker
- 2nd Negative Speaker
- 3rd Affirmative Speaker
- 3rd Negative Speaker

**Room Distribution Rules:**
```
(Number of People) mod 6 =
    0: Create N/6 rooms
    1-3: Create N/6 rooms, extras double up as 3rd Negative
    4-5: Create N/6 + 1 rooms, extra room has 4-5 people (1st-3rd Aff roles)
```

### British Parliamentary (8 roles)
BP format with 8 roles: PM, LO, DPM, DLO, GM, MO, GW, OW

### Neo (Group-based)
Advanced format supporting group constraints and timeslot management.

## Input Format

CSV file with preferences:

```csv
name,1Aff,1Neg,2Aff,2Neg,3Aff,3Neg
Dylan,1,2,3,4,5,6
Kim,6,100,2,1,5,4
Alex,2,1,3,5,4,6
```

- **First column**: Participant name
- **Middle columns**: Role preferences (1 = most preferred, higher = less preferred)
- **Last column (optional)**: Group (for neo format)

### With Groups (Neo format)
```csv
name,1Aff,1Neg,2Aff,2Neg,3Aff,3Neg,Group
Dylan,1,2,3,4,5,6,A
Kim,6,100,2,1,5,4,A,B
Alex,2,1,3,5,4,6,B
```

## Output Format

CSV file with room assignments:

```csv
Name,Role,Role preferenced at number,Group

Room 1
Alice,1st Aff,1,
Bob,1st Neg,2,
Charlie,2nd Aff,1,
...

Room 2
...
```

## Algorithm

The algorithm uses a **two-phase min-cost max-flow approach**:

1. **Edmonds-Karp**: Finds maximum flow (ensures all participants are assigned)
2. **Cycle-Canceling**: Iteratively finds and cancels negative-cost cycles to minimize total preference cost

This ensures optimal room assignments that maximize participant satisfaction.

## Examples

See the [examples/](examples/) directory for sample input files:
- [input.csv](examples/input.csv) - Traditional format with 13 people
- [bpin.csv](examples/bpin.csv) - British Parliamentary format

## Development

### Project Structure

```
DebatingAlgorithm/
├── debate_algorithm/          # Package directory
│   ├── __init__.py           # Package exports
│   ├── core.py               # Programmatic API
│   ├── cli.py                # CLI entry point
│   └── runner.py             # Legacy runner wrapper
├── graph.py                   # Graph algorithms
├── debate_runner.py           # Main orchestrator
├── debate_strategy.py         # Strategy pattern base
├── debate_io.py              # CSV I/O
├── debate_formats/           # Format implementations
│   ├── traditional.py
│   ├── british_parliamentary.py
│   └── neo.py
├── main.py                   # CLI script
├── pyproject.toml            # Package configuration
├── setup.py                  # Setup script
└── requirements.txt          # Dependencies
```

### Running Tests

```bash
pytest
```

## License

MIT

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.
