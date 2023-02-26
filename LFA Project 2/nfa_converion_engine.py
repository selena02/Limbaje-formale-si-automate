import sys
import re

def invalid():
    print("invalid NFA")
    exit(0)


input_file = open(sys.argv[1])

sigma_ls = list()
states_ls = list()
transitions_ls = list()
s_ls = list()
f_ls = list()

DFA_states_ls = list()
DFA_transitions_ls = list()
DFA_f_ls = list()

last_call = ""
for line in input_file:
    line = line.strip()

    if line[0] == '#':
        continue
    if '#' in line:
        line = line[0:line.index('#')]
    elif line == "End":
        last_call = ""

    elif last_call == "Sigma":
        sigma_ls.append(line)
    elif last_call == "States":
        line = re.findall(r'[^,\s]+', line)
        states_ls.append(line[0])
        if len(line) == 3:
            s_ls.append(line[0])
            f_ls.append(line[0])
        elif len(line) == 2:
            if line[1] == "S":
                s_ls.append(line[0])
            else:
                f_ls.append(line[0])
    elif last_call == "Transitions":
        line = re.findall(r'[^,\s]+', line)
        transitions_ls.append([line[0], line[1], line[2]])

    elif line == "Sigma:":
        last_call = "Sigma"
    elif line == "States:":
        last_call = "States"
    elif line == "Transitions:":
        last_call = "Transitions"

    elif len(s_ls) != 1 or len(f_ls) < 1:
        invalid()

n = len(states_ls)
matrix = [[[] for column in range(len(sigma_ls))] for line in range(n)]

for t in transitions_ls:
    if (t[0] not in states_ls) or (t[1] not in sigma_ls) or (t[2] not in states_ls):
        invalid()
    i = states_ls.index(t[0])
    j = sigma_ls.index(t[1])
    if not matrix[i][j]:
        matrix[i][j] = [t[2]]
    else:
        matrix[i][j].append(t[2])

DFA_matrix = []
new_states = {}

for i in range(len(matrix)):
    DFA_matrix.append(list())
    for j in range(len(matrix[i])):
        DFA_matrix[i].append((list()))
        DFA_matrix[i][j] = matrix[i][j]

def conversion(s):
    if s not in DFA_states_ls:
        i = states_ls.index(s)
        j = len(DFA_matrix)
        DFA_matrix.append(list())
        DFA_matrix[j].copy()

    for x in matrix[i]:
        if len(x) > 1:
            STATE = "q" + str(len(states_ls))
            states_ls.append(STATE)
            new_states[STATE] = x
            j = len(DFA_matrix)
            DFA_matrix.append(list())

#print("\n")
# print("Sigma:")
# for x in sigma_ls:
#     print(f"    {x}")
# print("End")
# print("States:")
# for x in states_ls:
#     print(f"    {x}", end="")
#     if x in s_ls:
#         print(", S", end="")
#     if x in f_ls:
#         print(", F ", end="")
#     print()
# print("End")
# print("Transitions: ")
# for x in transitions_ls:
#     print(f"{x[0]}, {x[1]}, {x[2]}")
# print("End")
