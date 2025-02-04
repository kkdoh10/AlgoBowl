from enum import Enum


class Type(Enum):
    BLANK = '.'
    LIGHT = 'L'
    GREY = 'X'
    GREY0 = '0'
    GREY1 = '1'
    GREY2 = '2'
    GREY3 = '3'
    GREY4 = '4'
    

class Cell:
    def __init__(self , cell_row, cell_col, is_lit: bool = False, cell_type: str = 'L') :
        self.is_lit = is_lit
        self.row = cell_row
        self.col = cell_col

        if cell_type  == '.':
            self.type = Type.BLANK
        elif cell_type  == 'L':
            self.type = Type.LIGHT
        elif cell_type  == 'X':
            self.type = Type.GREY
        elif cell_type  == '0':
            self.type = Type.GREY0
        elif cell_type  == '1':
            self.type = Type.GREY1
        elif cell_type  == '2':
            self.type = Type.GREY2
        elif cell_type  == '3':
            self.type = Type.GREY3
        elif cell_type  == '2':
            self.type = Type.GREY2
        elif cell_type  == '3':
            self.type = Type.GREY3          
        elif cell_type  == '4':
            self.type = Type.GREY4
    
    def __str__(self) -> str:
        return self.type.value  


