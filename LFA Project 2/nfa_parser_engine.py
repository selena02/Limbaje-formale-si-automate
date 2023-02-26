import sys
import re

input_file = open(sys.argv[1])

def func(input_file):
    sigma_ls = list()
    states_ls = list()
    transitions_ls = list()
    s_ls = list()
    f_ls = list()
    last_call = ""
    for line in input_file:
        line = line.strip()

        if line[0] == '#':
            continue
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
            return False

    n = len(states_ls)
    matrix = [[0 for column in range(n)] for line in range(n)]
    for t in transitions_ls:
        if (t[0] not in states_ls) or (t[1] not in sigma_ls) or (t[2] not in states_ls):
            return False
        i = states_ls.index(t[0])
        j = states_ls.index(t[2])
        matrix[i][j] = t[1]

    return True


if func(input_file):
    print("Valid NFA")
else:
    print("Invalid NFA")
