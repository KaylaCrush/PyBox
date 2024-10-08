class Box:
    # 044464441
    # 5       5
    # 9       7
    # 5       5
    # 244484443
    #
    #
    #
    char_dict = {
        'double':["╔","╗","╚","╝","═","║","╦","╣","╩","╠","╬","═","║"],
        'table':["╔","╗","╚","╝","═","║","╤","╢","╧","╟","┼","─","│"]
    }


## TODO Ensure height and widht are at least 2 (smallest possible box)
    def __init__(self, height, width, style='double'):
        self.height = height
        self.width = width
        self.style = style
        self.chars = self.char_dict[self.style]

    def draw(self):
        string = self.top_row()
        string += self.middle_rows()
        string += self.bottom_row()
        print(string)

    def top_row(self):
        chars = self.chars
        return chars[0]+chars[4]*(self.width-2)+chars[1]+'\n'

    def middle_rows(self):
        return self.middle_row()*(self.height-2)

    def middle_row(self):
        chars = self.chars
        return chars[5]+" "*(self.width-2)+chars[5]+'\n'

    def bottom_row(self):
        chars = self.chars
        return chars[2]+chars[4]*(self.width-2)+chars[3]+'\n'


class TextBox(Box):
    def __init__(self, text):
        self.lines = text.splitlines()
        height = len(self.lines) + 4
        width = max(len(line) for line in self.lines) + 4
        super().__init__(height,width)

    def middle_rows(self):
        rows_string = ""
        for line in self.lines:
            rows_string+=self.middle_row(line)
        return rows_string

    def middle_row(self, line):
        chars = self.char_dict[self.style]
        return chars[5]+" "+line+" "*(self.width-3-len(line))+chars[5]+'\n'

class TableBox(Box):
    def __init__(self, table):
        # table = [[str(item) for item in inner_list] for inner_list in table]
        self.table = table

        self.col_widths =[]
        for i in range(len(table[0])):
            self.col_widths.append(max(len(row[i]) for row in table)+2)

        height = len(table)*2 + 1
        width = sum(self.col_widths)+len(table[0])+1
        self.justify = self.center_justify
        super().__init__(height, width, style='table')

    def left_justify(self, text, width):
        margin = " "*(width-len(text)-2)
        return " "+text+" "+margin

    def right_justify(self, text, width):
        margin = " "*(width-len(text)-2)
        return margin+" "+text+" "

    def center_justify(self, text, width):
        right_margin = " "*(((width-len(text)-2)//2)+(width-len(text))%2)
        left_margin = " "*((width-len(text)-2)//2)
        return left_margin+" "+text+" "+right_margin

    def top_row(self):
        top_string = self.chars[0]
        for width in self.col_widths[:-1]:
            top_string += self.chars[4]*width+self.chars[6]
        top_string += self.chars[4]*self.col_widths[-1]+self.chars[1]+'\n'
        return top_string

    def middle_rows(self):
        middle_string = ""
        for row in self.table[:-1]:
            middle_string += self.middle_row(row)
            middle_string += self.divider_row()
        middle_string += self.middle_row(self.table[-1])
        return middle_string

    def middle_row(self, row):
        row_string = self.chars[5]
        for i, col in enumerate(row[:-1]):
            width = self.col_widths[i]
            row_string += self.justify(col, width) + self.chars[12]

        row_string += self.justify(row[-1], self.col_widths[-1]) + self.chars[5]+'\n'
        return row_string


    def divider_row(self):
        divider_string = self.chars[9]
        for width in self.col_widths[:-1]:
            divider_string += self.chars[11]*width+self.chars[10]
        divider_string += (self.chars[11]*self.col_widths[-1]) +self.chars[7]+'\n'
        return divider_string

    def bottom_row(self):
        bottom_string = self.chars[2]
        for width in self.col_widths[:-1]:
            bottom_string += self.chars[4]*width+self.chars[8]
        bottom_string += self.chars[4]*self.col_widths[-1]+self.chars[3]+'\n'
        return bottom_string

from sympy import *
from sympy.logic.boolalg import truth_table
class LogicTable(TableBox):
    def __init__(self, expressions):
        props = list(set.union(*[exp.atoms() for exp in expressions]))

        def truthy(i):
            return 'True' if i == 1 else 'False'
        table = []
        row = []
        for prop in props:
            row.append(str(prop))
        for exp in expressions:
            row.append(str(exp))
        table.append(row)
        truth_tables = [list(truth_table(expression, props)) for expression in expressions]
        for i in range(len(truth_tables[0])):
            row = [truthy(val) for val in truth_tables[0][i][0]]
            for j in range(len(expressions)):
                row.append(str(truth_tables[j][i][1]))
            table.append(row)
        super().__init__(table)

    def draw_window(self):
        pass

p, q, r = symbols('p, q, r')
expressions = [p|q, p&r|q&(p|r)]

LogicTable(expressions).draw()
