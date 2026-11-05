from tkinter.constants import NORMAL

import customtkinter as ctk

class Switch(ctk.CTkSwitch):
    def __init__(self, master, text:str = "txt_switch", font = ("Arial", 12), command = None, state:str = "normal", **kwargs):
        super().__init__(master, text = text, font = font, command = command, state = state, **kwargs)
        self.text = text
        self.font = font
        self.command = command
        self.state = state