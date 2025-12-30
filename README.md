# Debate Algorithm

A Python package for optimizing debate room assignments using min-cost max-flow algorithms. Assigns debaters to teams and rooms based on their preferences while maximizing overall satisfaction.


### 2. Command Line Interface

#### Interactive Mode
```bash
python -m hardstucks_debating.cli
```

#### CLI Mode with Arguments
```bash
# Traditional format
python -m hardstucks_debating.cli examples/input.csv -o output.csv -f traditional

# British Parliamentary format
python -m hardstucks_debating.cli -i examples/bpin.csv -o output.csv -f bp

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
- **Last column (optional)**: Group: Used for grouping students for example timeslots e.g. ("11am, 1pm")

### With Groups 
```csv
name,1Aff,1Neg,2Aff,2Neg,3Aff,3Neg,Group
Dylan,1,2,3,4,5,6,11am
Kim,6,100,2,1,5,4,"11am,1pm"
Alex,2,1,3,5,4,6,"1pm"
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
