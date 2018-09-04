__author__ = "Alex Hunziker"
__email__ = "alexhunziker@sunrise.ch"
__licence__ = "GPL v3"

import tkinter as tk
from tkinter import messagebox
from contextlib import redirect_stdout
import io

import EntITyGUI
import EntITyElement


class EntITy(object):
    """ The EntITy Class is the main class for EntITy. 
It governs the behaviour of the program and invokes the GUI Class and EntITyElements """
    
    def __init__(self):
        """ Initializes the essential data structures """
        self.program_elements = []
        self.cursor_position=0
        self.myEntITGUI = EntITyGUI.EntITyGUI(self)
        # Set a reference to self in the EntITy Class var.
        EntITyElement.EntITyElement.entITy = self

    def cursor_forward(self):
        """ Moves the cursor one position forward, w/o affecting the duck positions """
        if not self.init_save_current():
            return
        # If the end was not reached
        if self.cursor_position < len(self.program_elements):
            self.cursor_position += 1
            self.myEntITGUI.draw_ducks()
        else:
            messagebox.showinfo("Quack", "You have reached the end of the code")

    def cursor_backward(self):
        """ Moves the cursor one position backwards, w/o affecting duck positions """
        if not self.init_save_current():
            return
        # Check if move is possible
        if self.cursor_position > 0:
            print("Cursor_backward")
            self.cursor_position -= 1
            self.myEntITGUI.draw_ducks()
        else:
            messagebox.showinfo("Quack", "You have reached the begining of the code")

    def move_forward(self):
        """ Exchanges the current duck with the next duck and moves the cursor forward """
        if not self.init_save_current():
            return
        self.exchange_elements()
        if self.cursor_position < len(self.program_elements):
            self.cursor_position += 1
        self.myEntITGUI.draw_ducks()
        

    def move_backward(self):
        """ Exchanges the current and previous duck and moves the cursor backward """
        if not self.init_save_current():
            return
        if self.cursor_position > 0:
            self.cursor_position -= 1
            self.exchange_elements()
            self.myEntITGUI.draw_ducks()
        else:
            messagebox.showwarning("Quack", "No previous element to exchange with")

    def exchange_elements(self):
        """ Helper function, that allows to exchange two concurrent ducks """
        if not self.cursor_position < len(self.program_elements)-1:
            messagebox.showwarning("Quack", "Elements cannot be exchanged")
            return
        tmp = self.program_elements[self.cursor_position]
        self.program_elements[self.cursor_position] = self.program_elements[self.cursor_position+1]
        self.program_elements[self.cursor_position+1] = tmp
    
    def extend_2(self):
        """ Determines weather element 2 of the property area in the GUI needs extension """
        if len(self.program_elements) == self.cursor_position:
            return False
        this_el = self.program_elements[self.cursor_position]
        extend_p2 = isinstance(this_el, EntITyElement.EntITyBlock)
        return extend_p2 # True if current element is an EntITyBlock    

    # The following 4 functions may be combined to one function...
    def delete_current(self):
        """ Removes the current duck from the program code """
        self.program_elements.pop(self.cursor_position)
        self.myEntITGUI.draw_ducks()

    def add_block(self):
        """ Add a new EntITy block element to the program code """
        if not self.init_save_current():
            return
        self.program_elements.insert(self.cursor_position, EntITyElement.EntITyBlock())
        self.myEntITGUI.draw_ducks()       

    def add_control(self):
        """ Add a new EntITy Control to the program code """
        if not self.init_save_current():
            return
        self.program_elements.insert(self.cursor_position, EntITyElement.EntITyControl())
        self.myEntITGUI.draw_ducks()

    def add_loop(self):
        """ Add a new EntITy Loop to the program code """
        if not self.init_save_current():
            return
        self.program_elements.insert(self.cursor_position, EntITyElement.EntITyLoop())
        self.myEntITGUI.draw_ducks()

    def add_end(self):
        """ Add a new EntITy End to the program code """
        if not self.init_save_current():
            return
        self.program_elements.insert(self.cursor_position, EntITyElement.EntITyEnd())
        self.cursor_position += 1
        self.myEntITGUI.draw_ducks()

    def generate_code(self, indent, name=None, index=None):
        """ This function controls the order of code generation """
        print(name, index)
        # pass can be used instead of a jump
        if name == "pass":
            return " "*indent + "pass\n"
        # Search for name of the element to jump to if a jump is planned
        if name:
            for i in range(0, len(self.program_elements)):
                if self.program_elements[i].name == name:
                    # Set the index of the next code block
                    index = i
        # By this point index must either be determined by loop above or function argument
        if index is None:
            messagebox.showerror("Quack", "Code not generated. Name " + name + " not found")
            return ""
        # Stop interpreting at the end of the program automatically
        if index == len(self.program_elements):
            return ""
        # Generate actual code of Element and return indent for next block
        codectrl = self.program_elements[index].generate_code(indent)
        # Stop Duck encountered. Stop linear execution here (go up one recursion lvl)
        if codectrl[1] == "Stop":
            return codectrl[0]
        # Continue Linear code generation
        elif codectrl[1] == "None":
            return codectrl[0] + self.generate_code(indent, index=index+1)
        # Jump to mark
        else:
            return codectrl[0] + self.generate_code(indent, name=codectrl[1])
            

    def run(self, parameters=""):
        """ Invokes code generation and execution """
        if not self.init_save_current():
            return
        self.myEntITGUI.draw_ducks()
        self.code = self.generate_code(0, index=0)
        self.console_printout = "EntITy v0.1 - Executing program... \n\n" # with parameters " + parameters + "\n\n"
        print(self.code)
        # Redirect console output
        # TODO: Redirect Errors as well.
        # TODO: Intermediate prints (during code exection)
        # Possible solution: Redirect all output to a file and read from there
        f = io.StringIO()
        with redirect_stdout(f):
            # Code execution
            exec(self.code)
        # add to console printout
        self.console_printout += f.getvalue()
        self.console_printout += "\n\nExecution terminated.\n"
        # send to GUI
        self.myEntITGUI.update_console_printout(self.console_printout)

    def init_save_current(self):
        """ Initializes the saving of current entered properties if not end of code """
        if self.cursor_position == len(self.program_elements):
            return True
        return self.myEntITGUI.save()

    def save_current(self, name, p1, p2, p3, p4):
        """ Saves the properties of current duck, obtained by GUI """
        if self.program_elements[self.cursor_position].storeValues(name, p1, p2, p3, p4):
            return True
        messagebox.showwarning("Quack", "Current properties not saveable, check syntax")
        return False

    def name_is_unique(self, name):
        """ Checks for the uniqueness of a duck name, in order to avoid ambiguous jumps """
        for el in self.program_elements:
            if el.name == name and not el.name==self.program_elements[self.cursor_position].name:
                return False
        return True

    def load_current_labels(self):
        """ Send labels of current duck properties to the GUI """
        if len(self.program_elements) == self.cursor_position:
            return("Empty Field", None, None, None, None, None)
        else:
            return self.program_elements[self.cursor_position].getLabels()

    def load_current_values(self):
        """ Load the current duck properties """
        return self.load_values(self.cursor_position)

    def load_values(self, i):
        """ Load the values of a duck other than the current """
        print(i)
        if len(self.program_elements) == i:
            return [None, None, None, None, None]
        else:
            return self.program_elements[i].getValues()
                

# Start the program
entITy = EntITy()
# Enter mainloop to wait for user interaction
entITy.myEntITGUI.master.mainloop()
        
