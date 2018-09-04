__author__ = "Alex Hunziker"
__email__ = "alexhunziker@sunrise.ch"
__licence__ = "GPL v3"

import tkinter as tk
from tkinter import messagebox
from contextlib import redirect_stdout
import io

import EntITyElement

class EntITyGUI(object):
    def __init__(self, entITy):
        """ Initializes a EntITy GUI Window and prepares the necessary objects """
        # Initialize TK Window
        self.master = tk.Tk()
        self.master.state('zoomed')
        self.master.title("EntITy - Entlich Programmieren")
        self.master.columnconfigure(9, weight=1)
        self.master.rowconfigure(1, weight=1)
        self.entITy = entITy

        # Generate UI Widgets
        self.create_navigation_buttons()
        self.create_delete_button()
        self.create_insert_buttons()
        self.create_run_button()
        self.create_duck_canvas()
        self.create_property_area()
        self.create_console_area()

        # Load Pictures
        self.load_duck_pictures()

        self.draw_ducks()

    def create_navigation_buttons(self):
        """ Generates navigation and element exchange buttons """
        self.next_icon = tk.PhotoImage(file="icn/next.png")
        self.previous_icon = tk.PhotoImage(file="icn/previous.png")
        self.master.previous = tk.Button(self.master, activebackground="red",
                                         image=self.previous_icon, height=32, width=32,
                                         command=self.entITy.cursor_backward)
        self.master.next = tk.Button(self.master, activebackground="green",
                                         image=self.next_icon, height=32, width=32,
                                         command=self.entITy.cursor_forward)
        self.master.previous.grid(row=0, column=0)
        self.master.next.grid(row=0, column=1)

        self.left_icon = tk.PhotoImage(file="icn/left.png")
        self.right_icon = tk.PhotoImage(file="icn/right.png")
        self.master.left = tk.Button(self.master, activebackground="red",
                                         image=self.left_icon, height=32, width=32,
                                         command=self.entITy.move_backward)
        self.master.right = tk.Button(self.master, activebackground="green",
                                         image=self.right_icon, height=32, width=32,
                                         command=self.entITy.move_forward)
        self.master.left.grid(row=0, column=2)
        self.master.right.grid(row=0, column=3)

    def create_delete_button(self):
        """" Generates the delete Element button """
        self.delete_icon = tk.PhotoImage(file="icn/delete.png")
        self.master.delete = tk.Button(self.master, activebackground="black",
                                         image=self.delete_icon, height=32, width=32,
                                         command=self.entITy.delete_current)
        self.master.delete.grid(row=0, column=4, padx=20)

    def create_insert_buttons(self):
        """ Generates the buttons to insert the various kinds of ducks """
        self.function_icon = tk.PhotoImage(file="icn/duck_blue_icn.png")
        self.control_icon = tk.PhotoImage(file="icn/duck_green_icn.png")
        self.loop_icon = tk.PhotoImage(file="icn/duck_pink_icn.png")
        self.end_icon = tk.PhotoImage(file="icn/duck_yello_icn.png")
        self.master.function = tk.Button(self.master,
                                         image=self.function_icon, height=32, width=32,
                                         command=self.entITy.add_block)
        self.master.control = tk.Button(self.master,
                                         image=self.control_icon, height=32, width=32,
                                         command=self.entITy.add_control)
        self.master.loop = tk.Button(self.master,
                                         image=self.loop_icon, height=32, width=32,
                                         command=self.entITy.add_loop)
        self.master.end = tk.Button(self.master,
                                         image=self.end_icon, height=32, width=32,
                                         command=self.entITy.add_end)
        self.master.function.grid(row=0, column=5)
        self.master.control.grid(row=0, column=6)
        self.master.loop.grid(row=0, column=7)
        self.master.end.grid(row=0, column=8)

    def create_run_button(self):
        """ Generates the button to run the EntITy Script """
        self.run_icon = tk.PhotoImage(file="icn/run.png")
        self.run = tk.Button(self.master, background="white",
                             image=self.run_icon, height=32, width=32,
                                         command=self.entITy.run)
        self.run.grid(row=0, column=10, sticky=(tk.W, tk.E))

    def create_duck_canvas(self):
        """ Generates the Canvas on which the program will be visually drawn """
        # TODO: Whilst scrolling works, the scrollbar does not indicate the lenghth nor position of the site
        self.duck_canvas = tk.Canvas(self.master, background="white", scrollregion=(0,0,50000,50000), height=50000)
        self.duck_canvas.grid(row=1, column=0, columnspan=10, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.vbar = tk.Scrollbar(self.master, orient=tk.VERTICAL)
        self.vbar.grid(row=1, column=9, sticky=(tk.N, tk.S, tk.E))
        self.vbar.config(command=self.duck_canvas.yview)

    def create_property_area(self):
        """ Creates the Widgets to display the properties for the different ducks """
        self.element_kind = tk.Label(master=self.master, text="Nothing selected")
        self.element_kind.grid(row=2, column=0, columnspan=10)

        self.prop_name = tk.Label(master=self.master, text="Duck Name")
        self.prop_name.grid(row=3, column=0, columnspan=4, sticky=tk.W, padx=10)
        self.prop_name_val = tk.Entry(master=self.master)
        self.prop_name_val.grid(row=3, column=4, columnspan=6, sticky=(tk.W, tk.E))

        # This is a tk.Text Widget in order to allow for multi Line entry in case of the Block Duck
        self.prop_1 = tk.Label(master=self.master, text="Prop 1")
        self.prop_1.grid(row=4, column=0, columnspan=4, sticky=tk.W, padx=10)
        self.prop_1_val = tk.Text(master=self.master, height=1)
        self.prop_1_val.grid(row=4, column=4, columnspan=6, sticky=(tk.W, tk.E))

        self.prop_2 = tk.Label(master=self.master, text="Prop 2")
        self.prop_2.grid(row=5, column=0, columnspan=4, sticky=tk.W, padx=10)
        self.prop_2_val = tk.Entry(master=self.master)
        self.prop_2_val.grid(row=5, column=4, columnspan=6, sticky=(tk.W, tk.E))

        self.prop_3 = tk.Label(master=self.master, text="Prop 3")
        self.prop_3.grid(row=6, column=0, columnspan=4, sticky=tk.W, padx=10)
        self.prop_3_val = tk.Entry(master=self.master)
        self.prop_3_val.grid(row=6, column=4, columnspan=6, sticky=(tk.W, tk.E))

        self.prop_4 = tk.Label(master=self.master, text="prop4")
        self.prop_4.grid(row=7, column=0, columnspan=4, sticky=(tk.W, tk.N), padx=10)
        self.prop_4_val = tk.Entry(master=self.master)
        self.prop_4_val.grid(row=7, column=4, columnspan=6, sticky=(tk.W, tk.E))

    def create_console_area(self):
        """ Generates the console area """
        # TODO: Enable scrolling (switch from Label to canvas?)
        self.console_print = tk.Label(master=self.master, width=60, background="black",
                                      foreground="light green",
                                      text="EntITy - Entlich Programmieren (v0.1)\nReady\n",
                                      font=("Courier", 11), anchor=tk.NW, justify=tk.LEFT)
        self.console_print.grid(column=10, row=1, rowspan=7, sticky=(tk.N, tk.S))

    def load_duck_pictures(self):
        """ Preloads the Images of the ducks to be shown on the duck_canvas """
        self.function = tk.PhotoImage(file="img/duck_blue.gif")
        self.control = tk.PhotoImage(file="img/duck_green.gif")
        self.loop = tk.PhotoImage(file="img/duck_pink.gif")
        self.end = tk.PhotoImage(file="img/duck_yello.gif")

    def draw_ducks(self):
        """ This function updates the duck_canvas, displaying the current programm by redrawing all elements """
        # TODO: Beautify code...
        self.duck_canvas.delete(tk.ALL)
        for i in range(0,len(self.entITy.program_elements)):
            values = self.entITy.load_values(i)
            pos = self.get_pos(i)
            if i == self.entITy.cursor_position:
                self.duck_canvas.create_rectangle(pos[0], pos[1], pos[0]+330, pos[1]+330, fill="light grey")
            if type(self.entITy.program_elements[i]) is EntITyElement.EntITyBlock:
                self.duck_canvas.create_image(pos[0], pos[1], anchor=tk.NW, image=self.function)
                self.duck_canvas.create_text(pos[0]+90, pos[1]+150, anchor=tk.NW, text=values[1], width=250)
                self.duck_canvas.create_text(pos[0]+250, pos[1]+120, anchor=tk.NW, text=values[4])
            elif type(self.entITy.program_elements[i]) is EntITyElement.EntITyControl:
                self.duck_canvas.create_image(pos[0], pos[1], anchor=tk.NW, image=self.control)
                self.duck_canvas.create_text(pos[0]+50, pos[1]+170, anchor=tk.NW, text=values[1], width=99)
                self.duck_canvas.create_text(pos[0]+150, pos[1]+230, anchor=tk.NW, text=values[2], width=99)
                self.duck_canvas.create_text(pos[0]+250, pos[1]+120, anchor=tk.NW, text=values[3], width=99)
            elif type(self.entITy.program_elements[i]) is EntITyElement.EntITyLoop:
                self.duck_canvas.create_image(pos[0], pos[1], anchor=tk.NW, image=self.loop)
                self.duck_canvas.create_text(pos[0]+50, pos[1]+170, anchor=tk.NW, text=values[1], width=99)
                self.duck_canvas.create_text(pos[0]+150, pos[1]+230, anchor=tk.NW, text=values[2], width=99)
            elif isinstance(self.entITy.program_elements[i], EntITyElement.EntITyEnd):
                self.duck_canvas.create_image(pos[0], pos[1], anchor=tk.NW, image=self.end)
            else:
                print(type(self.entITy.program_elements[i]))
            self.duck_canvas.create_text(pos[0]+80, pos[1]+20, anchor=tk.NW, text=values[0])

        # In case the cursor is at the end of the script, i.e. not underneath a duck    
        if self.entITy.cursor_position == len(self.entITy.program_elements):
            pos = self.get_pos(self.entITy.cursor_position)
            self.duck_canvas.create_rectangle(pos[0], pos[1], pos[0]+330, pos[1]+330, fill="light grey")
        self.load_properties()

    def load_properties(self):
        """ Getting the properties and labels of the current duck, adjusting propertie area and displaying it """
        labels = self.entITy.load_current_labels()
        print(labels)
        # Set not needed Labels to "" and the rest to the obtained values
        self.element_kind.config(text=labels[0]) if (labels[0] is not None) else self.element_kind.config(text="No selection")
        self.prop_name.config(text=labels[1]) if (labels[1] is not None) else self.prop_name.config(text="")
        self.prop_1.config(text=labels[2]) if (labels[2] is not None) else self.prop_1.config(text="")
        self.prop_2.config(text=labels[3]) if (labels[3] is not None) else self.prop_2.config(text="")
        self.prop_3.config(text=labels[4]) if (labels[4] is not None) else self.prop_3.config(text="")
        self.prop_4.config(text=labels[5]) if (labels[5] is not None) else self.prop_4.config(text="")

        # Make unavailable fields non editable, clear fields and display current properties
        values = self.entITy.load_current_values()
        print(values)
        self.prop_name_val.delete(0, tk.END)
        if values[0]:
            self.prop_name_val.config(state=tk.NORMAL)
            self.prop_name_val.insert(0, values[0])
        else:
            self.prop_name_val.config(state=tk.DISABLED)
        self.prop_1_val.delete(1.0, tk.END)
        if values[1]:
            self.prop_1_val.config(state=tk.NORMAL)
            self.prop_1_val.insert(1.0, values[1])
        else:
            self.prop_1_val.config(state=tk.DISABLED)
        self.prop_2_val.delete(0, tk.END)
        if values[2]:
            self.prop_2_val.config(state=tk.NORMAL)
            self.prop_2_val.insert(0, values[2])
        else:
            self.prop_2_val.config(state=tk.DISABLED)
        self.prop_3_val.delete(0, tk.END)
        if values[3]:
            self.prop_3_val.config(state=tk.NORMAL)
            self.prop_3_val.insert(0, values[3])
        else:
            self.prop_3_val.config(state=tk.DISABLED)
        self.prop_4_val.delete(0, tk.END)
        if values[4]:
            self.prop_4_val.config(state=tk.NORMAL)
            self.prop_4_val.insert(0, values[4])
        else:
            self.prop_4_val.config(state=tk.DISABLED)

        # This part extends property 1 for multi line commands for the block duck, and reverts for anything else
        if self.entITy.extend_2():
            self.prop_1_val.config(height=4)
            self.prop_1_val.grid(row=4, column=4, columnspan=6, rowspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
            self.prop_2_val.grid_remove()
            self.prop_3_val.grid_remove()
        else:
            self.prop_1_val.grid_forget()
            self.prop_1_val.config(height=1)
            self.prop_1_val.grid(row=4, column=4, columnspan=6, sticky=(tk.W, tk.E))
            self.prop_2_val.grid()
            self.prop_3_val.grid()  

    def get_pos(self, i):
        """ Gets the position on where to place the i-th duck """
        cols = self.duck_canvas.winfo_width() // 330
        row = i % cols if cols!=0 else 0
        col = i//cols if cols!=0 else 0
        return [row*330, col*330]

    def save(self):
        """ Get the current property values and send them to the entITy object for saving """
        name = self.prop_name_val.get()
        p1 = self.prop_1_val.get(1.0, tk.END).rstrip()
        p2 = self.prop_2_val.get()
        p3 = self.prop_3_val.get()
        p4 = self.prop_4_val.get()
        return self.entITy.save_current(name, p1, p2, p3, p4)

    def update_console_printout(self, printout):
        """ Updates the console to whatever output is generated """
        self.console_print.configure(text=printout)
