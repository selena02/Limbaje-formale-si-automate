import sys
import re

def invalid():
	print("invalid DFA")
	exit(0)

input_file = open(sys.argv[1])

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
matrix = [[0 for column in range(n)] for line in range(n)]
for t in transitions_ls:
    if (t[0] not in states_ls) or (t[1] not in sigma_ls) or (t[2] not in states_ls):
        invalid()
    i = states_ls.index(t[0])
    j = states_ls.index(t[2])
    matrix[i][j] = t[1]
matrice = [[0 for column in range(n)] for line in range(n)]
for i in range(len(states_ls)):
    for j in range(len(states_ls)):
        if (states_ls[i] in f_ls and states_ls[j] not in f_ls) or(states_ls[j] in f_ls and states_ls[i] not in f_ls):
            matrice[i][j]= 1
            matrice[j][i] = 1
ok=1
while ok==1:
    ok=0
    for i in range(len(states_ls)):
        for j in range(len(states_ls)):
            if matrice[i][j]==0 and i!=j:
                for k in sigma_ls:
                    if k in matrix[i] and k in matrix[j]:
                        a=matrix[i].index(k)
                        b=matrix[j].index(k)
                        if matrice[a][b]==1:
                            matrice[i][j]=1
                            matrice[j][i]=1
                            ok=1
lista=[]
for i in range(len(states_ls)):
    for j in range(i):
        if matrice[i][j]==0:
            lista.append([states_ls[i],states_ls[j]])

i=1
n=len(lista)
while i<n:
    for j in range(i):
        if lista[i][0] in lista[j] and lista[i][1] in lista[j]:
            lista=lista[:i]+lista[i+1:]
            n=n-1
            i-=1
        elif lista[i][0] in lista[j] :
            lista[j].extend(lista[i][1])
            lista = lista[:i] + lista[i + 1:]
            n=n-1
            i-=1
        elif lista[i][1] in lista[j]:
            lista[j].extend(lista[i][0])
            lista = lista[:i] + lista[i + 1:]
            n=n-1
            i-=1
    i+=1

for stare in states_ls:
    ok=0
    for j in lista:
        if stare in j:
            ok=1
    if ok==0:
        lista.append([stare])
print(lista)
final=[[0 for column in range(len(lista))] for line in range(len(lista))]
for i in range(len(lista)):
    for k in sigma_ls:
        stare=states_ls.index(lista[i][0])
        if k in matrix[stare]:
            a=matrix[stare].index(k)
            for j in range(len(lista)):
                if states_ls[a] in lista[j]:
                    b=j
            final[i][b]=k
for linie in final:
    print(linie)
print()
print("Sigma:")
for k in sigma_ls:
    print(k)
print("End")
print("States:")
for states in lista:
    print(states[0],end=" ")
    ok1=0
    ok2=0
    for c in states:
        if c in s_ls:
            ok1=1
        if c in f_ls:
            ok2=1
    if ok1==1:
        print(",S",end=" ")
    if ok2==1:
        print(",F", end=" ")
    print()
print("End")
print("Transitions:")
for i in range(len(lista)):
    for j in range(len(lista)):
        if final[i][j]!=0:
            print(lista[i][0],", ",final[i][j],", ", lista[j][0])
print("End")
