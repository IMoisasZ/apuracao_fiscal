import customtkinter as ctk

class Container(ctk.CTkFrame):
    def __init__(self, master, width:int = 200, height:int = 200, **kwargs):
        super().__init__(master, width = width, height = height, **kwargs)
        self.width = width
        self.height = height