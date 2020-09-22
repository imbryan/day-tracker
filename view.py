import tkinter as tk
from tkinter import ttk  # More native looking widgets


class View(tk.Tk):

    def __init__(self, controller):
        super().__init__()  # Call Tk constructor
        self.controller = controller

        self.title("Day Tracker")

    def main(self):
        self.mainloop()

