from CTkMessagebox import CTkMessagebox

class Message(CTkMessagebox):
    def __init__(self, master = None, width:int = 400, height:int = 200, title:str = "title_name", message:str = "description_message", option_1:str = "OK", option_2:str = None, option_3:str = None, options = [], icon:str = "info", icon_size:int = None, font = ("Arial", 12), header:bool = False, option_focus = None):
        super().__init__(master, width = width, height = height, title = title, message = message, option_1 = option_1, option_2 = option_2, option_3 = option_3, options = options, icon = icon, icon_size = icon_size, font = font, header = header, option_focus = option_focus)
