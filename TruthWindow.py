import tkinter as tk
from tkinter import ttk
from sympy import *
from sympy.logic.boolalg import truth_table

class TruthWindow(tk.Tk):
    def __init__(self):
        super().__init__()  # Initialize the Tk object
        self.title("Logic Expressions")
        # self.geometry("400x300")
        self.frame=ttk.Frame(self,padding=(4,4,4,4))
        self.frame.grid(sticky='nsew')

        # Store entry boxes for logical expressions
        self.input_boxes = []

        # Set up the frame and widgets
        self.create_widgets()

    def create_widgets(self):
        """Initial setup of widgets."""
        # Add first input box by default

        plus_button = ttk.Button(self.frame, text="+", command=self.add_input,width=3).grid(row=0,column=0)
        min_button = ttk.Button(self.frame, text="-",command=self.remove_input,width=3).grid(row=0,column=1)
        self.add_input()
        # Button to show the truth table in a new window
        self.table_button = ttk.Button(self.frame, text="Show Truth Table", command=self.show_truth_table)
        self.table_button.grid(row=0, column=10, columnspan=2)


    def add_input(self):
        """Add a new entry widget for logical expression input."""
        row = len(self.input_boxes)

        exp_entry = ttk.Entry(self.frame, width=20)
        if row == 0:
            exp_entry.focus_set()
        exp_entry.grid(row=row, column=2, padx=5,pady=2)
        exp_entry.bind("<Return>", self.on_return_key)

        # Add the entry widget to the list for later use
        self.input_boxes.append(exp_entry)

    def on_return_key(self, event):
        self.show_truth_table()

    def remove_input(self):
        if len(self.input_boxes) > 1:
            self.input_boxes[-1].grid_forget()
            self.input_boxes.pop(-1)

    def show_truth_table(self):
        """Open a new window to display the truth table."""
        new_window = tk.Toplevel(self)
        new_window.title("Truth Table")
        table = self.create_table()
        for i, row in enumerate(table):
            for j, data in enumerate(row):
                ttk.Label(new_window, text=data).grid(column=j, row=i,padx=5,pady=5)


    def create_table(self):
        expressions = [parse_expr(expr.get()) for expr in self.input_boxes]
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
        return table

# Run the application
if __name__ == "__main__":
    app = TruthWindow()
    app.mainloop()
