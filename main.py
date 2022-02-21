from classes import Token, Type, Iterator
from tokenizer import tokenizer

function_params = {
    "move": [Type.NUM],
    "turn": [Type.DIRCONST],
    "face": [Type.CARDCONST],
    "put": [Type.ITEMCONST, Type.NUM],
    "pick": [Type.ITEMCONST, Type.NUM],
    "move-dir": [Type.NUM, Type.DIRCONST],
    "move-face": [Type.NUM, Type.CARDCONST],
    "facing-p": [Type.CARDCONST],
    "can-put-p": [Type.ITEMCONST, Type.NUM],
    "can-pick-p": [Type.ITEMCONST, Type.NUM],
    "can-move-p": [Type.CARDCONST],
    "skip": []
}

def parse_args(iter: Iterator, token: Token ,args: Iterator): # Has func token taken
    expected_type = args.next()
    if expected_type == None and iter.peek().type == Type.CLS:
        return True

    expected_types = [expected_type]
    if expected_type == Type.NUM:
        expected_types.append(Type.ID)
        expected_types.append(Type.LOCALID)
    if iter.peek().type in expected_types:
        iter.next()
        if args.peek() == None:
            return True
        else:
            return parse_args(iter, token, args)
    else:
        print(f"Token {token} did not have the correct args. Expected {expected_type}, got {iter.peek().type}")
        return False

def parse_defid(iter: Iterator): # Has defid token taken
    if iter.next().type != Type.ID:
        print("Missing name on definition of variable")
        return False
    if iter.next().type != Type.NUM:
        print("Missing number on definition of variable")
        return False
    return True

def parse_local_vars(iter: Iterator, func: Token):
    next = iter.next()
    if next.type == Type.LOCALID:
        function_params[func.value].append(Type.NUM)
        return parse_local_vars(iter, func)
    elif next.type == Type.CLS:
        return True
    else:
        print(f"Expected CLS, got {next}")
        return False

def parse_deffunc(iter: Iterator): # Has deffunc token taken
    func_token = iter.next()
    if func_token.type != Type.IDFUNC:
        return False
    function_params[func_token.value] = []
    if iter.next().type == Type.OP:
        valid = parse_local_vars(iter, func_token)
        if not valid:
            print("Local variables shaped incorrectly")
            return False
        
        valid = parse_block(iter)
        if not valid:
            print("Could not find block on deffunc")
            return False
        while iter.peek().type == Type.OP:
            valid = parse_block(iter)
            if not valid:
                print("Invalid block on deffunc")
                return False
        return True

    else:
        print("Misshaped function definition")
        return False

def parse_not(iter: Iterator):
    next = iter.next()
    if next.type == Type.OP:
        next = iter.next()
        if next.type == Type.IDFUNC:
            valid = parse_args(iter, next, Iterator(function_params[next.value]))
            iter.next()
            if not valid:
                print("Misshaped NOT statement")
                return False
            return True
        else:
            print("NOT requires a no-params function or a block-function to work")
            return False
    elif next.type == Type.IDFUNC:
        next_char = iter.next()
        if next_char.type == Type.CLS and len(function_params[next.value]) == 0:
            return True
        else:
            print("Invalid function for NOT statement")
            return False
    else:
        print(f"NOT operator cannot use token {next}")

def parse_cond(iter: Iterator):
    next = iter.next()
    if next.type in (Type.IDFUNC, Type.NOT):
        if next.type == Type.IDFUNC:
            valid = parse_args(iter, next, Iterator(function_params[next.value]))
            iter.next()
            if not valid:
                print("Misshaped conditional statement: Could not parse func args")
                return False
        else:
            valid = parse_not(iter)
            if not valid:
                print("Misshaped conditional statement: Could not parse NOT statement")
                return False
        return True
    else:
        print("Conditional statement is not a function")
        return False

def parse_if(iter: Iterator):
    next = iter.next()
    if next.type == Type.OP:
        valid = parse_cond(iter)
        if not valid:
            print("Error on IF statement: Invalid conditional")
            return False
        valid = parse_block(iter)
        if not valid:
            print("Misshaped IF statement: Could not parse Block1")
            return False
        valid = parse_block(iter)
        if not valid:
            print("Misshaped IF statement: Could not parse Block2")
            return False
        return True
    else:
        print(f"IF expected a function, got {next} instead")
        return False

def parse_loop(iter: Iterator):
    next = iter.next()
    if next.type == Type.OP:
        valid = parse_cond(iter)
        if not valid:
            print("Error on LOOP statement: Invalid conditional")
            return False
        valid = parse_block(iter)
        if not valid:
            print("Misshaped LOOP statement: Could not parse Block")
            return False
        return True
    else:
        print(f"LOOP expected a function, got {next} instead")
        return False

def parse_repeat(iter: Iterator):
    next = iter.next()
    if next.type in [Type.NUM, Type.ID, Type.LOCALID]:
        valid = parse_block(iter)
        if not valid:
            print("Misshaped LOOP statement: Could not parse Block")
            return False
        return True
    else:
        print(f"REPEAT expected a num/var, got {next} instead")

def parse_run_dirs(iter: Iterator):
    next = iter.peek()
    if next.type == Type.DIRCONST:
        iter.next()
        return parse_run_dirs(iter)
    elif next.type == Type.CLS:
        return True
    return False

def parse_block(iter: Iterator):  # Recieves as raw block ( no '(' taken )
    token = iter.next() # Grabs hopefully '('
    if token.type == Type.OP:
        valid = False
        token = iter.peek() # Tries to guess what next character could be
        if token.type != Type.OP:
            iter.next()
        if token.type == Type.IDFUNC:
            valid = parse_args(iter, token, Iterator(function_params[token.value]))
        elif token.type == Type.DEFID:
            valid = parse_defid(iter)
        elif token.type == Type.OP:
            while True:
                if not parse_block(iter):
                    return False
                if iter.peek().type != Type.OP:
                    iter.next()
                    return True
        elif token.type == Type.CLS:
            return True
        elif token.type == Type.DEFFUNC:
            valid = parse_deffunc(iter)
        elif token.type == Type.NOT:
            valid = parse_not(iter)
        elif token.type == Type.IF:
            valid = parse_if(iter)
        elif token.type == Type.LOOP:
            valid = parse_loop(iter)
        elif token.type == Type.REP:
            valid = parse_repeat(iter)
        elif token.type == Type.RUNDIRS:
            valid = parse_run_dirs(iter)
        iter.next()
        return valid
    else:
        print("Expected open parenthesis")
        return False

def parse_start(iter: Iterator):
    value = parse_block(iter)
    if not value:
        return False
    if iter.peek().type == Type.OP:
        return parse_start(iter)
    elif iter.peek().type == Type.EOF:
        return value
    print("----")
    for i in iter:
        print(i)
    return False

tokens = tokenizer()
iter_tokens = Iterator(tokens)
print(parse_start(iter_tokens))
