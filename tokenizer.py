from classes import Token, Type
import symbol

symbols = {
    '(': symbol.enter_context,
    ')': symbol.exit_context
}

depth = 0
clear_depth = float('-inf')
local_identifiers = set()
context = 0

token_identifiers = {
        "defvar": Type.DEFID,
        "=": Type.IDFUNC,
        "move": Type.IDFUNC,
        "turn": Type.IDFUNC,
        "face": Type.IDFUNC,
        "put": Type.IDFUNC,
        "pick": Type.IDFUNC,
        "move-dir": Type.IDFUNC,
        "run-dirs": Type.RUNDIRS,
        "move-face": Type.IDFUNC,
        "skip": Type.IDFUNC,
        "if": Type.IF,
        "loop": Type.LOOP,
        "repeat": Type.REP,
        "defun": Type.DEFFUNC,
        "facing-p": Type.IDFUNC,
        "can-put-p": Type.IDFUNC,
        "can-pick-p": Type.IDFUNC,
        "can-move-p": Type.IDFUNC,
        "not": Type.NOT,
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

    if len(tokens) > 0 and tokens[-1].type == Type.DEFID:
        if keyword in token_identifiers:
            return Token(Type.NULL, keyword)
        type = Type.ID
        if clear_depth > -1:
            type = Type.LOCALID
            local_identifiers.add(keyword)
        token_identifiers[keyword] = type
        return Token(type, keyword)
    elif keyword in token_identifiers:
        return Token(token_identifiers[keyword], keyword)
    elif keyword.isnumeric():
        return Token(Type.NUM, int(keyword))
    elif tokens[-1].type == Type.DEFFUNC:
        token_identifiers[keyword] = Type.IDFUNC
        clear_depth = depth
        return Token(Type.IDFUNC, keyword)
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