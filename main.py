from classes import Token, Type, Iterator
import symbol

symbols = {
    '(': symbol.enter_context,
    ')': symbol.exit_context
}

depth = 0
clear_depth = float('-inf')
local_identifiers = set()
context = 0
output = True
token_identifiers = {
        "defvar": Type.DEFID,
        "=": Type.IDFUNC,
        "move": Type.IDFUNC,
        "turn": Type.IDFUNC,
        "face": Type.IDFUNC,
        "put": Type.IDFUNC,
        "pick": Type.IDFUNC,
        "move-dir": Type.IDFUNC,
        "run-dirs": Type.IDFUNC,
        "move-face": Type.IDFUNC,
        "skip": Type.IDFUNC,
        "if": Type.IF,
        "loop": Type.LOOP,
        "repeat": Type.REP,
        "defun": Type.DEFFUNC,
        "facing-p": Type.COND,
        "can-put-p": Type.COND,
        "can-pick-p": Type.COND,
        "can-move-p": Type.COND,
        "not": Type.IDFUNC,
        ":front": Type.DIRCONST,
        ":up": Type.DIRCONST,
        ":right": Type.DIRCONST,
        ":left": Type.DIRCONST,
        ":back": Type.DIRCONST,
        ":down": Type.DIRCONST,
        ":north": Type.CARDCONST,
        ":south": Type.CARDCONST,
        ":west": Type.CARDCONST,
        ":east": Type.CARDCONST,
        ":chips": Type.ITEMCONST,
        ":balloons": Type.ITEMCONST
    }

filename = "Robot.txt"
lines = []
code = ""

with open(filename) as f:
    lines = [line.strip() for line in f.read().splitlines() if line != '']

for line in lines:
    code += line

def tokenizer()->list:
    global depth
    global clear_depth

    keyword = ""
    token = Token(Type.NULL, "")
    tokens = []
    for character in code:
        if depth < clear_depth:
            for key in local_identifiers:
                token_identifiers.pop(key)
            local_identifiers.clear()
            clear_depth = float('-inf')
        if character == ')':
            if keyword != "":
                tokens.append(get_token(keyword, tokens))
            tokens.append(Token(Type.CLS, ')'))
            depth -= 1
            keyword = ""
        elif character == '(':
            tokens.append(Token(Type.OP, '('))
            depth += 1
        elif character == ' ':
            if keyword != "":
                token = get_token(keyword, tokens)
                tokens.append(token)
                keyword = ""
        else:
            keyword += character
    tokens.append(Token(Type.EOF, ""))
    return tokens

def get_token(keyword: str, tokens: list)->Token:
    global depth
    global clear_depth

    if keyword in token_identifiers:
        return Token(token_identifiers[keyword], keyword)
    elif keyword.isnumeric():
        return Token(Type.NUM, int(keyword))
    elif tokens[-1].type == Type.DEFFUNC:
        token_identifiers[keyword] = Type.IDFUNC
        clear_depth = depth
        return Token(Type.IDFUNC, keyword)
    elif tokens[-1].type == Type.DEFID:
        token_identifiers[keyword] = Type.IDFUNC
        return Token(Type.ID, keyword)
    elif tokens[-1].type == Type.LOCALID or [t.type for t in tokens[-3:]] == [Type.DEFFUNC, Type.IDFUNC, Type.OP]:
        i = 0
        for token in reversed(tokens):
            if token.type == Type.LOCALID:
                i +=1
                continue

            verify = [t.type for t in tokens[-3-i:-i]]
            if i == 0:
                verify = [t.type for t in tokens[-3:]]
            
            if verify == [Type.DEFFUNC, Type.IDFUNC, Type.OP]:
                break
            else:
                return Token(Type.NULL, keyword)
        token_identifiers[keyword] = Type.LOCALID
        local_identifiers.add(keyword)
        return Token(Type.LOCALID, keyword)
    else:
        return Token(Type.NULL, keyword)

tokens = tokenizer()
iter_tokens= Iterator(tokens)
for token in iter_tokens:
    print(token)
    if token.type == Type.OP:
        context +=1
        continue
    elif token.type == Type.CLS:
        context -=1
        continue
    elif token.type == Type.DEIFD:
        pass
        
    elif token.type == Type.IDFUNC:
        defId()
    elif token.type == Type.IF:
        defId()
    elif token.type == Type.LOOP:
        defId()
    elif token.type == Type.REP:
        defId()
    elif token.type == Type.DEFFUNC:
        defId()
    elif token.type == Type.COND:
        defId()
    elif token.type == Type.DIRCONST:
        defId()
    elif token.type == Type.CARDCONST:
        defId()
    elif token.type == Type.ITEMCONST:
        defId()

    if context <0:
        output=False
        break
    
def defId():
    pass
