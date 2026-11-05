import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import customtkinter as ctk
from src.views.layout import LayoutSystem

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

if __name__ == "__main__":
    app = LayoutSystem()

    app.mainloop()