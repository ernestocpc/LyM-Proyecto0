from enum import Enum, auto

class Token:
    def __init__(self, type, value) -> None:
        self.type = type
        self.value = value
    
    def __str__(self) -> str:
        return f'({self.type} - "{self.value}")'

class Iterator:
    index = -1

    def __init__(self, list) -> None:
        self.list = list

    def __iter__(self):
        return self
    
    def __next__(self):
        self.index += 1
        if self.index == len(self.list):
            raise StopIteration
        return self.list[self.index]
    
    def peek(self):
        if self.index+1 == len(self.list):
            return None
        return self.list[self.index+1]
        
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
