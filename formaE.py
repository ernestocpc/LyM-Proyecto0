
from operator import length_hint
import sys

    
filename=input('Nombre archivo: ')
code = []

keywords = {'defvar', '=', 'move', 'turn', 'face', 'put', 'pick', 'move-dir', 'run-dirs', 'move-face', 
'skip', 'if', 'loop', 'repeat', 'defun', 'facing-p', 'can-put-p', 'can-pick-p', 'can-move-p', 'not'}

symbols = {'(', ')', ' ', ':'}    

output=True

variables = {}
functions = set()

turn_options = {'left','right','around'}
face_options = {'north', 'south','east','west'}
object_options = {'Balloon','Chips'}
move_options = {':up',':right',':left',':down'}

condition_options = {'facing-p','can-put-p','can-pick-p','can-move-p','not'}

with open(filename) as f:
    lines = f.read().splitlines()
    code = [line.strip() for line in lines if line != '']


def defvar(command_line):
    global output
    if len(command_line)==3:
        var_value = command_line[2]
        if var_value.isnumeric():
            variables[command_line[1]] = command_line[2]
        else:
            output=False
    else:
        output=False

def equals(command_line):
    global output
    if len(command_line)==3:
        var_value = command_line[2]
        if var_value.isnumeric():
            variables[command_line[1]] = command_line[2]
        else:
            output=False
    else:
        output=False

def move(command_line):
    global output
    if len(command_line)==2:
        var_value = command_line[1]
        if not var_value.isnumeric():
            output=False
    else:
        output=False
    
def turn(command_line):
    global output
    if len(command_line)==2:
        if command_line[1] not in turn_options:
            output=False
    else:
        output=False
    
def face(command_line):
    global output
    if len(command_line)==2:
        if command_line[1] not in face_options:
            output=False
    else:
        output=False
    
def put(command_line):
    global output
    if len(command_line)==3:
        if command_line[1] in object_options:
            if command_line[2] not in variables and not command_line[2].isnumeric():
                output = False
        else:
            output=False
    else:
        output=False

def pick(command_line):
    global output
    if len(command_line)==3:
        if command_line[1] in object_options:
            if command_line[2] not in variables and not command_line[2].isnumeric():
                output = False
        else:
            output=False
    else:
        output=False
    
def moveDir(command_line):
    global output
    if len(command_line) == 3:
        if command_line[1] not in variables and not command_line[1].isnumeric():
            output=False
        if command_line[2] not in move_options:
            output=False
    else:
        output = False 

def runDirs(command_line):

    global output
    if len(command_line) ==2:
        directions= command_line[1]
        if isinstance(directions,list) and not directions:
            for direction in directions:
                if direction not in move_options:
                    output = False 
        else:
            output=False
    else:
        output=False
    
    
def moveFace(command_line):
    global output
    if len(command_line) == 3:
        if command_line[1] not in variables or not command_line[1].isnumeric():
            output=False
        if command_line[2] not in face_options:
            output=False
    else:
        output=False
    
    
def CondIf(command_line):
    global output
    conditional = command_line[1]
    print(conditional)
    if conditional not in condition_options:
        print('Entry')
        # output = False 
    

    pass
def loop(command_line):
    global output
    pass

def repeat(command_line):
    global output
    pass

def defun(command_line):
    global output
    pass

def facingP(command_line):
    global output
    pass

def canPutP(command_line):
    global output
    pass

def canPickP(command_line):
    global output
    pass

def canMoveP(command_line):
    global output
    pass

def CondNot(command_line):
    global output
    pass



def stripCommands(code):
    """
    Retorna una lista donde cada posicion es un comando sin parentesis y sin importar la identacion
    Revisa tambien que la cantidad de parentesis sea la adecuada.
    """
    context = 0
    command_block = []
    word = ''
    for command in code:
        command_line = command.split(' ')
        for keyword in command_line:
            
            
            for letter in keyword:
                if letter =='(':
                    context +=1
                elif letter==')':
                    context-=1
                elif letter != '(' and letter != ')':
                    word+=letter
            word+=' '
            if context ==0:
                command_block.append(word)
                word = ''
            elif context <0:
                output = False
                break
    return command_block



command_block = stripCommands(code)

if output == False:
    print('Invalid sintaxis (Check parenthesis)')
else:
    for command_string in command_block:
        # command_string = command_string[1:len(command_string)-2]
        command_line =command_string.split()
        # while command_line[0][0]=='(':
        #     command_line[0] = command_line[0][1:len(keyword)-1]
        print(command_line)
        for keyword in command_line:
            # print(keyword)
            if keyword in keywords:
                if keyword == 'defvar':
                    defvar(command_line)
                elif keyword == '=':
                    equals(command_line)
                elif keyword == 'move':
                    move(command_line)
                elif keyword == 'turn':
                    turn(command_line)
                elif keyword == 'face':
                    face(command_line)
                elif keyword == 'put':
                    put(command_line)
                elif keyword == 'pick':
                    pick(command_line)
                elif keyword == 'move-dir':
                    moveDir(command_line)
                elif keyword == 'run-dirs':
                    runDirs(command_line)
                elif keyword == 'move-face':
                    moveFace(command_line)

                elif keyword == 'if':
                    CondIf(command_line)
                elif keyword == 'loop':
                    loop(command_line)
                elif keyword == 'repeat':
                    repeat(command_line)
                elif keyword == 'defun':
                    defun(command_line)
        
                elif keyword == 'facing-p':
                    facingP(command_line)
                elif keyword == 'can-put-p':
                    canPutP(command_line)
                elif keyword == 'can-pick-p':
                    canPickP(command_line)
                elif keyword == 'can-move-p':
                    canMoveP(command_line)
                elif keyword == 'not':
                    CondNot(command_line)
                continue
        if output == False:
            print('Invalid Sintaxis')
            break