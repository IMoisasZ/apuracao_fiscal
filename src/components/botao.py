import customtkinter as ctk

class Botao(ctk.CTkButton):
    def __init__(self, master, width:int = 140, height:int = 28, bg_color:str = "transparent", fg_color:str = None, text_color:str = None, text:str = "nome_btn", font = ("Arial", 12), state:str = "normal", command = None, anchor:str = "center", **kwargs):
        super().__init__(master, width = width, height = height, bg_color = bg_color, fg_color = fg_color, text_color = text_color, text = text, font = font, state = state, command = command, anchor = anchor, **kwargs)
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.text_color = text_color
        self.text = text
        self.font = font
        self.state = state
        self.command = command
        self.anchor = anchor
