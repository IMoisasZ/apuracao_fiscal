import customtkinter as ctk

class BaseScreen(ctk.CTk):
    def __init__(self, titulo: str = "Apuração fiscal", min_width:int = 600, min_height:int = 420):
        super().__init__()
        # Construtor
        self.title(titulo)
        self.min_width = min_width
        self.min_height = min_height

        # Definindo tamanho da tela
        self.default_sreen = f'{self.min_width}x{self.min_height}'
        self.geometry(self.default_sreen)