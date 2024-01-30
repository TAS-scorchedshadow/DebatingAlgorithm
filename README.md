# Debating Algorithm

Script for sorting debaters into teams and rooms based on given preferences. Example input and output values have been provided

## Background
In debating a debate consists of 6 roles, that debate in the following order
- 1st Affirmitive Speaker
- 1st Negative Speaker
- 2nd Affirmitive Speaker
- 2nd Negative Speaker
- 3rd Affirmitive Speaker
- 3rd Negative Speaker

When organsing practice and team selection for a large group of debaters an organiser may want to maximise the number of full rooms and also ensure that people are generally happy with their roles.

This script will first create "rooms" based on the following rules
```
(Number of People) mod 6 =
    0: Create N/6 Rooms
    1-3: Create N/6 Rooms, any extra people in a room will be allowed to double up as 3rd Negative Speaker
    4-5: Create N/6 + 1 Rooms, the extra room will have 4 or 5 people that will be labelled as 1st Aff through to 3rd Aff
```

Next we use the cycle cancelling algorithm to assign people to rooms based on their preferences.


## Running the program
```
python3 app.py
```

Note: Tailored implementation of the cycle-cancelling algorithm to solve the min-cost max flow 

Input is a CSV where each record contains the name and the preference for each position. The prefence value should be a positive interger 1+. Where 1 is the most preferred

## Example Input
```
name, 1Aff, 1Neg, 2Aff, 2Neg, 3Aff,3Neg #First line of input is ignored
Dylan,1,2,3,4,5,6
Kim,6,100,2,1,5,4
```
## Example Output
```
Name,Role,Role preferenced at number

Room 1
A,1st Aff,1
K,1st Neg,2
F,2nd Aff,4
G,2nd Neg,3
J,3rd Aff,2
L,3rd Neg,1
M,3rd Neg,1

Room 2
I,1st Aff,1
D,1st Neg,2
E,2nd Aff,3
H,2nd Neg,3
B,3rd Aff,1
C,3rd Neg,1
```
