import customtkinter as ctk

class Label(ctk.CTkLabel):
    def __init__(self, master, width:int = 0, height:int = 28, text_color:str = None, text:str = "CTkLabel", font = ("Arial", 12), anchor:str = "center", **kwargs):
        super().__init__(master, width = width, height = height, text_color = text_color, text = text, font = font, anchor = anchor, **kwargs)
        self.width=width
        self.height=height
        self.text_color=text_color
        self.text=text
        self.font=font
        self.anchor=anchor
