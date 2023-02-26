# Hurloi Selena Andreea
# Oancea Elena-Antonia
# Nistor Gheorghe
# grupa 142


input_file = open("tm_config_file_cerinta2.txt")
print("Loading confile file...")


def invalid():
    print("The config file is NOT a valid turing machine!")
    exit(0)


# Printare tape principal și tape copie
def printTapes():
    print("main tape:", *tapeMatrix[0])
    print("copy tape:", *tapeMatrix[1])
    print()


# simulatorTM reprezintă HEAD-ul de la Turing Machine
def simulatorTM(tapeMatrix, q1, i, j):
    if i: # i reprezintă tape-ul curent
        tape = "copyTape"
    else:
        tape = "mainTape"
    tS_1 = tapeMatrix[i][j] # tS_1 este simbolul curent citit de pe tape
    if tS_1 not in transitions[q1][tape]: # dacă nu există nicio funcție de tranziție pentru starea, simbolul și tape-ul curent atunci starea trece în q_Reject
        print("INVALID string! ~ (q_reject)")
        return
    q2 = transitions[q1][tape][tS_1][0] # q2 reprezintă starea în care se va trece
    tS_2 = transitions[q1][tape][tS_1][1] # tS_2 este simbolul care va fi scris pe tape
    d = transitions[q1][tape][tS_1][2] # d este direcția în care va merge HEAD-ul : Up, Down, Left, Right
    if tS_2 == blankSymbol: # daca simbolul care trebuie scris pe tape este blank, tape-ul rămâne neschimbat
        tS_2 = tapeMatrix[i][j]
    tapeMatrix[i][j] = tS_2
    if d == 'D':
        i += 1
    elif d == 'L' and j:
        j -= 1
    elif d == 'R':
        j += 1
    elif d == 'U' and i:
        i -= 1
    if q2 == acceptState_ls[0] and tS_1== blankSymbol: # s-a ajuns în prima stare de accept, urmează să se verifice cele două tape-uri
        print("VALID string! ~ (q_firstAccept)")
        printTapes()
        return
    return simulatorTM(tapeMatrix, q2, i, j)

states_ls = list()
inputAlphabet_ls = list()
tapeAlphabet_ls = list()
blankSymbol = ""
initialState = ""
acceptState_ls = list()
rejectState = ""
input = list()
language = ""
last_call = ""
transitions = dict()

# validare config file
for line in input_file:
    line = line.strip()
    if line == '':
        continue
    if line == "End":
        last_call = ""

    elif last_call == "States":
        states_ls.append(line)  # adăugare stare în lista de stări, etc..
    elif last_call == "Input alphabet":
        inputAlphabet_ls.append(line)
    elif last_call == "Tape alphabet":
        tapeAlphabet_ls.append(line)
    elif last_call == "Blank symbol":
        if blankSymbol != "":  # vericăm dacă există deja alt "blank simbol"
            invalid()
        blankSymbol = line
        tapeAlphabet_ls.append(line)
    elif last_call == "Initial state":
        if initialState != "":
            invalid()  # dacă sunt mai multe stări de început atunci config file-ul nu este valid
        initialState = line
    elif last_call == "Accept state":
        if line not in states_ls:
            invalid()  # dacă starea de accept nu se află în lista de stări atunci => invalid()
        acceptState_ls.append(line)
    elif last_call == "Reject state":
        if line not in states_ls:
            invalid()   # dacă starea de reject nu se află în lista de stări atunci => invalid()
        if rejectState != "":
            invalid() # dacă sunt mai multe stări de reject atunci config file-ul nu este valid
        rejectState = line
        if rejectState in acceptState_ls:
            invalid()  # dacă starea de reject se regăsește in lista cu stări de accept atunci config file-ul este invalid
    elif last_call == "Check state":
        continue
    elif last_call == "Transitions":
        # o tranziție arată în config file în felul următor
        # C mainTape x -> A x R
        x, y = line.split("->")
        # x = C mainTape x
        [q1, tape, tS_1] = x.split()
        q1 = q1.strip()         # q1 = C
        tape = tape.strip()     # tape = mainTape
        tS_1 = tS_1.strip()     # ts_1 = x

        if q1 not in states_ls:
            invalid()
        if tS_1 not in tapeAlphabet_ls:
            invalid()

        y = y.split()
        q2 = y[0].strip()
        tS_2 = y[1].strip()
        d = y[2].strip()

        if tS_2 not in tapeAlphabet_ls:
            invalid()
        if q2 not in states_ls:
            invalid()
        if d not in ['U', 'D', 'L', 'R', '.']:
            invalid()
        if tape not in ["mainTape", "copyTape"]:
            invalid()

        # în dictionarul transitions vor fi memorate toate tranzițiile din config file
        # 'copyTape' fiind o bandă doar pentru copierea lui 'mainTape'
        # are doar tranziții pentru urcarea HEAD-ul înapoi pe prima bandă
        if q1 not in transitions:
            transitions[q1] = {"mainTape": {}, "copyTape": {}}
        transitions[q1][tape][tS_1] = [q2, tS_2, d]
    elif last_call == "Input":
        input = line.split(' ')
    elif last_call == "Language":
        language = line

    elif line == "States:":
        last_call = "States"
    elif line == "Input alphabet:":
        last_call = "Input alphabet"
    elif line == "Tape alphabet:":
        last_call = "Tape alphabet"
    elif line == "Transitions:":
        last_call = "Transitions"
    elif line == "Blank symbol:":
        last_call = "Blank symbol"
    elif line == "Initial state:":
        last_call = "Initial state"
    elif line == "Accept state:":
        last_call = "Accept state"
    elif line == "Reject state:":
        last_call = "Reject state"
    elif line == "Check state:":
        last_call = "Check state"
    elif line == "Input:":
        last_call = "Input"
    elif line == "Language:":
        last_call = "Language"

# dacă s-a trecut de partea de validare și nu s-a intrat pe invalid() => config file-ul reprezintă un Turing Machine valid
print("Yee! The config file is a valid turing machine.\n")
print("language:", language)
print("input:", *input)
tapeMatrix = [input.copy(), ['_' if x.isdigit() else x for x in input]] # aici sunt construite cele două tape-uri
print("\nInitial tapes:")
printTapes()
simulatorTM(tapeMatrix, initialState, 0, 1) # începe simularea pentru Turing Machine cu input-ul dat