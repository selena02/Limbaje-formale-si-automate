import sys
import re


def invalid():
    print("invalid NFA")
    exit(0)

input_file = open(sys.argv[1])
word = sys.argv[2]

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
matrix = [[0 for column in range(len(sigma_ls))] for line in range(n)]

for t in transitions_ls:
    if (t[0] not in states_ls) or (t[1] not in sigma_ls) or (t[2] not in states_ls):
        invalid()
    i = states_ls.index(t[0])
    j = sigma_ls.index(t[1])
    if not matrix[i][j]:
        matrix[i][j] = [t[2]]
    else:
        matrix[i][j].append(t[2])

print("Valid NFA")
for c in word:
    if c not in sigma_ls:
        print(f"The word should contain only the characters {sigma_ls}")
        exit()


def bkt(i, index_c):
    if index_c == len(word)-1:
        c = word[index_c]
        j = sigma_ls.index(c)
        for x in matrix[i][j]:
            if x in f_ls:
                print(f"Valid word ('{word}')")
                exit()
    elif index_c < len(word)-1:
        c = word[index_c]
        j = sigma_ls.index(c)
        for x in matrix[i][j]:
            index_c += 1
            bkt(states_ls.index(x), index_c)


bkt(states_ls.index(s_ls[0]), 0)
print(f"Invalid word ('{word}')")
