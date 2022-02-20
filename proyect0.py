from operator import length_hint
import sys

    
filename=input('Nombre archivo: ')
code = []
context = 0
keywords = {'defvar', '=', 'move', 'turn', 'face', 'put', 'pick', 'move-dir', 'run-dirs', 'move-face', 
'skip', 'if', 'loop', 'repeat', 'defun', 'facing-p', 'can-put-p', 'can-pick-p', 'can-move-p', 'not'}

symbols = {'(', ')', ' ', ':'}    

output=True
variables={}

turn_options = {'left','right','around'}
face_options = {'north', 'south','east','west'}
object_options = {'Balloon','Chips'}
move_options = {':front',':right',':left',':back'}

with open(filename) as f:
    lines = f.read().splitlines()
    code = [line.strip() for line in lines if line != '']


def defvar(tokens):
    global output
    if len(tokens)==3:
        var_value = tokens[2][:-1]
        if var_value.isnumeric():
            variables[tokens[1]] = tokens[2][:-1]
        else:
            output=False
    else:
        output=False

def equals(tokens):
    global output
    if len(tokens)==3:
        var_value = tokens[2][:-1]
        if var_value.isnumeric():
            variables[tokens[1]] = tokens[2][:-1]
        else:
            output=False
    else:
        output=False

def move(tokens):
    global output
    if len(tokens)==2:
        var_value = tokens[1][:-1]
        if not var_value.isnumeric():
            output=False
    else:
        output=False
    
def turn(tokens):
    global output
    if len(tokens)==2:
        if tokens[1][:-1] not in turn_options:
            output=False
    else:
        output=False
    
def face(tokens):
    global output
    if len(tokens)==2:
        if tokens[1][:-1] not in face_options:
            output=False
    else:
        output=False
    
def put(tokens):
    global output
    if len(tokens)==3:
        if tokens[1] in object_options:
            if tokens[2][:-1] not in variables and not tokens[2][:-1].isnumeric():
                output = False
        else:
            output=False
    else:
        output=False

def pick(tokens):
    global output
    if len(tokens)==3:
        if tokens[1] in object_options:
            if tokens[2][:-1] not in variables and not tokens[2][:-1].isnumeric():
                output = False
        else:
            output=False
    else:
        output=False
    
def moveDir(tokens):
    global output
    if len(tokens) == 3:
        if tokens[1] not in variables and not tokens[1].isnumeric():
            output=False
        if tokens[2][:-1] not in move_options:
            output=False
    else:
        output = False 

def runDirs(tokens):
    # Falta asegurarse que la direccion final sea igual a la inicial.

    global output
    if len(tokens) ==2:
        directions= tokens[1][:-1]
        if isinstance(directions,list) and not directions:
            for direction in directions:
                if direction not in move_options:
                    output = False 
        else:
            output=False
    else:
        output=False
    
    
def moveFace(tokens):
    global output
    if len(tokens) == 3:
        if tokens[1] not in variables or not tokens[1].isnumeric():
            output=False
        if tokens[2][:-1] not in face_options:
            output=False
    else:
        output=False
    
def skip(tokens):
    global output
    if len(tokens)!=1:
        output=False
    
def CondIf(tokens):
    global output
    pass
def loop(tokens):
    global output
    pass
def repeat(tokens):
    global output
    pass
def defun(tokens):
    global output
    pass
def facingP(tokens):
    global output
    pass
def canPutP(tokens):
    global output
    pass
def canPickP(tokens):
    global output
    pass
def canMoveP(tokens):
    global output
    pass
def CondNot(tokens):
    global output
    pass

while context >=0:

    for command in code:
        tokens = command.split(' ')

        for token in tokens:

            keyword = token
            if token[0] == '(':
                context += 1
                keyword = token[1:]
            if token[0] == ')':
                context -= 1

        
            if keyword in keywords:
                if keyword == 'defvar':
                    defvar(tokens)
                elif keyword == '=':
                    equals(tokens)
                elif keyword == 'move':
                    move(tokens)
                elif keyword == 'turn':
                    turn(tokens)
                elif keyword == 'face':
                    face(tokens)
                elif keyword == 'put':
                    put(tokens)
                elif keyword == 'pick':
                    pick(tokens)
                elif keyword == 'move-dir':
                    moveDir(tokens)
                elif keyword == 'run-dirs':
                    runDirs(tokens)
                elif keyword == 'move-face':
                    moveFace(tokens)
                elif keyword == 'skip':
                    skip(tokens)
                elif keyword == 'if':
                    CondIf(tokens)
                elif keyword == 'loop':
                    loop(tokens)
                elif keyword == 'repeat':
                    repeat(tokens)
                elif keyword == 'defun':
                    defun(tokens)
                elif keyword == 'facing-p':
                    facingP(tokens)
                elif keyword == 'can-put-p':
                    canPutP(tokens)
                elif keyword == 'can-pick-p':
                    canPickP(tokens)
                elif keyword == 'can-move-p':
                    canMoveP(tokens)
                elif keyword == 'not':
                    CondNot(tokens)
                continue
    if context<0 or output == False:
        print('Invalid Sintaxis')
        break
            



