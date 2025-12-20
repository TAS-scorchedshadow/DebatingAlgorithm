# Graph ADT

#
# (Capacity, Cost, Flow)

import random
from graph import Graph
from copy import deepcopy
import csv

ROLEMAP = ["PM", "LO", "DPM", "DLO", "GM", "MO", "GW", "OW",]

def generateRooms(assignment, person_data) -> list:
    n_rooms = len(assignment[0])
    rooms = [[] for i in range(0,n_rooms)]
    flag = False
    for i, room in enumerate(rooms):
        for role, person_list in assignment.items():
            if len(person_list) == 0:
                flag = True
                break;
            x = person_list.pop(0)
            room.append((person_data[x]["name"], ROLEMAP[role], person_data[x]["preferences"][role]))

        if flag == True:
            break

    # Finally assign any double ups to the remaining rooms
    i = 0
    while len(assignment[7]) > 0:
        x = assignment[7].pop(0)
        rooms[i].append((person_data[x]["name"], ROLEMAP[role], person_data[x]["preferences"][7]))
        i += 1
        i = i % n_rooms

    return rooms


def main():
    print(r"""

        _   _               _     _              _     ______     _           _   _             
        | | | |             | |   | |            | |    |  _  \   | |         | | (_)            
        | |_| | __ _ _ __ __| |___| |_ _   _  ___| | __ | | | |___| |__   __ _| |_ _ _ __   __ _ 
        |  _  |/ _` | '__/ _` / __| __| | | |/ __| |/ / | | | / _ \ '_ \ / _` | __| | '_ \ / _` |
        | | | | (_| | | | (_| \__ \ |_| |_| | (__|   <  | |/ /  __/ |_) | (_| | |_| | | | | (_| |
        \_| |_/\__,_|_|  \__,_|___/\__|\__,_|\___|_|\_\ |___/ \___|_.__/ \__,_|\__|_|_| |_|\__, |
                                                                                            __/ |
                                                                                           |___/ 
    """)

    input_file = input("Please enter the name of the input file: ")

    data = []
    try:
        with open(input_file, 'r') as file:
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
        print("Input file not found")
        exit(1)

    output_file = input("Please provide a name for the output file: ")
    while output_file[-4:] != ".csv":
        print("Error - Output file must be .csv")
        output_file = input("Please provide a name for the output file: ")

    P = len(data)

    if P < 8:
        print("Trivial Solution")
        exit(0)


    N = P + 8 + 2

    role_cap = P // 8

    G = Graph(N)

    for i in range(1,1+P):
        G.addEdge(0,i,1,0)
        costs = data[i-1]["preferences"]
        # print(costs)
        for j in range(1+P,N-1):
            # print(j - P - 1, end=' ')
            G.addEdge(i,j,1, costs[j - P - 1])


    # Construct all edges from roles to sink
    for i in range(1+P,N-1):
        G.addEdge(i,N-1,role_cap,0)

    # Handle uneven people correction
    mod = P % 8
    if mod == 0:
        pass
    elif mod < 4:
        # Add extra people to 3rd negs
        G.addEdge(N-2,N-1,role_cap + mod,0)
    else:
        #add extra ppl exceeding alt 3n threshold to semi filled room
        G.addEdge(N-9,N-1,role_cap + 1, 0)
        G.addEdge(N-8,N-1,role_cap + 1, 0)
        G.addEdge(N-7,N-1,role_cap + 1, 0)
        G.addEdge(N-6,N-1,role_cap + 1, 0)
        #add extra ppl to semi filled room based on # of extras
        #ik this is janky dont @ me
        if mod >= 5:
            G.addEdge(N-5,N-1,role_cap + 1, 0)
            if mod >= 6:
                G.addEdge(N-4,N-1,role_cap + 1, 0)
                if mod == 7:
                    G.addEdge(N-3,N-1,role_cap + 1,0)


    # G.printGraph()
    resG = G.cycleCancel(0,N-1)    

    assignments = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: []}
    for i in range(1+P,N-1):
        row = resG.graph[i]
        links = []
        for j, tup in enumerate(row):
            if tup[0] != 0:
                links.append(j-1)
        # Randomize the order of users for room assignments
        random.shuffle(links)
        assignments[i-P-1] = links

    rooms = generateRooms(assignments,data)

    total_pref = 0
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Role", "Role preferenced at number"])
        for i, room in enumerate(rooms):
            writer.writerow([f"Room {i + 1}"])
            for name, role, pref in room:
                writer.writerow([name, role, pref])
                total_pref += pref

    print(r"""
        
            _____                                 _ 
            / ____|                              | |
            | (___  _   _  ___ ___ ___  ___ ___  | |
            \___ \| | | |/ __/ __/ _ \/ __/ __|  | |
            ____) | |_| | (_| (_|  __/\__ \__ \  |_|
            |_____/ \__,_|\___\___\___||___/___/ (_)
                                                    
                                                    
    """)
    print(f"Output wrote to {output_file}")
    print(f"On average people got their {total_pref}/{P} = {round(total_pref/P,3)} choice")

if __name__ == "__main__":
    main()
