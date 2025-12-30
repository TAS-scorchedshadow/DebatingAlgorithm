# Debate Algorithm

A Python package for optimizing debate room assignments using min-cost max-flow algorithms. Assigns debaters to teams and rooms based on their preferences while maximizing overall satisfaction.

## Installation

You may need to install the additional requirement:
```bash
pip install inquirer
```

## Command Line Interface

You can either click on main.py or run through command line

### Interactive Mode
``` bash
python -m hardstucks_debating.cli 
OR
```
```bash
python src/hardstucks_debating/main.py
```

### CLI Mode with Arguments
```bash
# Traditional format (group-aware)
python -m hardstucks_debating.cli 
Oython src/hardstucks_debating/main.py -i tests/input_with_groups.csv -o output.csv -f traditional

# British Parliamentary format (group-aware)
python -m hardstucks_debating.cli -i input.csv -o output.csv -f bp

# Traditional format (ignore groups)
python -m hardstucks_debating.cli -i input.csv -o output.csv -f traditional_ignore_group

# British Parliamentary format (ignore groups)
python -m hardstucks_debating.cli -i input.csv -o output.csv -f bp_ignore_group
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
    4-5: Create N/6 + 1 rooms, extra room has 4-5 people
```

### British Parliamentary (8 roles)
BP format with 8 roles: PM, LO, DPM, DLO, MG, MO, GW, OW

## Input Format Examples

### Example 1: Basic CSV (without groups)

```csv
Name,1st Aff,1st Neg,2nd Aff,2nd Neg,3rd Aff,3rd Neg
Alice,1,2,3,4,5,6
Bob,6,5,4,3,2,1
Charlie,2,1,3,5,4,6
Diana,3,4,1,2,6,5
Eve,5,6,2,1,4,3
Frank,1,3,5,6,4,2
```

- **First column**: Participant name
- **Remaining columns**: Role preferences (1 = most preferred, higher = less preferred)

### Example 2: CSV with Groups/Timeslots

```csv
Name,1st Aff,1st Neg,2nd Aff,2nd Neg,3rd Aff,3rd Neg,Group
Alice,1,2,3,4,5,6,Morning
Bob,6,5,4,3,2,1,Afternoon
Charlie,2,1,3,5,4,6,"Morning,Afternoon"
Diana,3,4,1,2,6,5,Morning
Eve,5,6,2,1,4,3,Afternoon
Frank,1,3,5,6,4,2,
George,4,2,6,1,3,5,Morning
Helen,6,5,4,3,2,1,Afternoon
Ivan,1,2,3,4,5,6,
```

- **Group column**: Comma-separated list of valid timeslots/groups for this person
- Empty group = can attend any timeslot (flexible person)
- Multiple groups = can attend multiple timeslots (flexible person)
- Single group = must attend that specific timeslot

### Example 3: Multi-Timeslot Debate

**Input** (`tests/multi_group_test.csv`):
```csv
Name,1st Aff,1st Neg,2nd Aff,2nd Neg,3rd Aff,3rd Neg,Group
A,1,2,3,4,5,6,"Morning,Afternoon"
B,1,2,3,4,5,6,"Morning,Evening"
C,1,2,3,4,5,6,Morning
D,1,2,3,4,5,6,Morning
E,1,2,3,4,5,6,Afternoon
F,1,2,3,4,5,6,Afternoon
G,1,2,3,4,5,6,Afternoon
H,1,2,3,4,5,6,Afternoon
I,1,2,3,4,5,6,Evening
J,1,2,3,4,5,6,
K,1,2,3,4,5,6,
L,1,2,3,4,5,6,
M,1,2,3,4,5,6,
```

### Example 4: British Parliamentary Format

```csv
Name,PM,LO,DPM,DLO,MG,MO,GW,OW,Group
Alice,1,2,3,4,5,6,7,8,TeamA
Bob,8,7,6,5,4,3,2,1,TeamA
Charlie,1,2,3,4,5,6,7,8,TeamB
Diana,8,7,6,5,4,3,2,1,TeamB
Eve,1,2,3,4,5,6,7,8,TeamA
Frank,8,7,6,5,4,3,2,1,TeamB
George,1,2,3,4,5,6,7,8,
Helen,8,7,6,5,4,3,2,1,
```

## Output Format Examples

### Example 1: Basic Output (without groups)

```csv
Name,Role,"Role preferenced at number, Group"
Room 1
Alice,1st Aff,1,
Charlie,1st Neg,1,
Diana,2nd Aff,1,
Bob,2nd Neg,3,
Eve,3rd Aff,1,
Frank,3rd Neg,2,
```

- **Name**: Participant name
- **Role**: Assigned debate role
- **Preference number**: How much they preferred this role (lower = better)
- **Group**: Original group assignment from input (empty if no groups)

### Example 2: Output with Groups (Group-Aware Format)

```csv
Name,Role,"Role preferenced at number, Group"
Room 1 (Morning)
Alice,1st Aff,1,Morning
Charlie,1st Neg,1,"Morning,Afternoon"
Diana,2nd Aff,1,Morning
George,2nd Neg,1,Morning
Ivan,3rd Aff,1,
Frank,3rd Neg,2,
Room 2 (Afternoon)
Bob,1st Aff,6,Afternoon
Eve,1st Neg,6,Afternoon
Helen,2nd Aff,4,Afternoon
Charlie,2nd Neg,5,"Morning,Afternoon"
...
```

Notice how:
- Rooms are named with their timeslot: `Room 1 (Morning)`, `Room 2 (Afternoon)`
- People with single groups are assigned to their timeslot
- Flexible people (empty or multiple groups) are distributed to fill rooms
- The Group column shows each person's original group constraints

### Example 3: Multi-Timeslot Output

**Command**:
```bash
python src/hardstucks_debating/main.py -i tests/multi_group_test.csv -o output.csv -f traditional
```

**Output** (`output.csv`):
```csv
Name,Role,"Role preferenced at number, Group"
Room 1 (Afternoon)
A,1st Aff,1,"Morning,Afternoon"
E,1st Neg,2,Afternoon
F,2nd Aff,3,Afternoon
G,2nd Neg,4,Afternoon
H,3rd Aff,5,Afternoon
J,3rd Neg,6,
Room 2 (Evening)
I,1st Aff,1,Evening
Room 3 (Morning)
C,1st Aff,1,Morning
D,1st Neg,2,Morning
K,2nd Aff,3,
L,2nd Neg,4,
M,3rd Aff,5,
B,3rd Neg,6,"Morning,Evening"
```

**Analysis**:
- 6 people assigned to Afternoon (E, F, G, H + flexible A + flexible J)
- 1 person in Evening (I only) - creating a partial room
- 6 people assigned to Morning (C, D + flexibles K, L, M, B)
- Flexible people (A, B, J, K, L, M) distributed to fill rooms optimally

### Example 4: Doubleup Scenario

**Input** (7 people):
```csv
Name,1st Aff,1st Neg,2nd Aff,2nd Neg,3rd Aff,3rd Neg,Group
A,1,2,3,4,5,6,TeamAlpha
B,1,2,3,4,5,6,TeamAlpha
C,1,2,3,4,5,6,TeamAlpha
D,1,2,3,4,5,6,TeamBeta
E,1,2,3,4,5,6,TeamBeta
F,1,2,3,4,5,6,TeamBeta
G,1,2,3,4,5,6,TeamBeta
```

**Output**:
```csv
Name,Role,"Role preferenced at number, Group"
Room 1 (TeamAlpha)
A,1st Aff,1,TeamAlpha
B,1st Neg,2,TeamAlpha
C,2nd Aff,3,TeamAlpha
Room 2 (TeamBeta)
D,1st Aff,1,TeamBeta
E,1st Neg,2,TeamBeta
F,2nd Aff,3,TeamBeta
G,2nd Neg,4,TeamBeta
```

**Analysis**:
- TeamAlpha: 3 people → creates partial room with 3 roles
- TeamBeta: 4 people → creates room with 4 roles (no doubleup needed)

## See Also

- `tests/` directory for more example input files
- `tests/input_with_groups.csv` - Traditional format with team groups
- `tests/multi_group_test.csv` - Multiple timeslots with flexible people
- `tests/timeslot_doubleup_test.csv` - Doubleup scenarios
