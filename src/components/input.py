import customtkinter as ctk

class Input(ctk.CTkEntry):
    def __init__(self, master, width:int = 140, height:int = 28, text_color:str = None, placeholder_text:str = None, font = ("Arial", 12), state:str = "normal", **kwargs):
        super().__init__(master, width = width, height = height, text_color = text_color, placeholder_text = placeholder_text, font = font, state = state, **kwargs)
        self.font = font
        self.height = height
        self.placeholder_text = placeholder_text
        self.state = state
        self.text_color = text_color
        self.width = width
