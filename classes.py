from enum import Enum, auto

class Token:
    def __init__(self, type, value) -> None:
        self.type = type
        self.value = value
    
    def __str__(self) -> str:
        return f'({self.type} - "{self.value}")'

class Type(Enum):
    DEFID = auto()
    DEFFUNC =auto()
    IF =auto()
    LOOP =auto()
    REP =auto()
    COND = auto()
    NUM = auto()
    LOCALID = auto()
    ID = auto()
    IDFUNC = auto()
    DIRCONST = auto()
    CARDCONST = auto()
    ITEMCONST = auto()
    CLS = auto()
    OP = auto()
    NULL = auto()
    EOF = auto()
