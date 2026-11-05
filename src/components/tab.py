import customtkinter as ctk

class Tabview(ctk.CTkTabview):
    def __init__(self, master, width:int = 300, height:int = 250, command = None, anchor:str = "center", state:str = "normal", **kwargs):
        super().__init__(master, width = width, height = height, command = command, anchor = anchor, state = state, **kwargs)
        self.width = width
        self.width = width
        self.height = height
        self.command = command
        self.anchor = anchor
        self.state = state
