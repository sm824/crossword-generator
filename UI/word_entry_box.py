import tkinter as tk
from library import *

class WordEntryBox:

    def __init__(self, x, y):
        
        self.x = x
        self.y = y
        self.is_deleted = False

        self.word_entry = tk.Entry(
            width = 12,
            bg = "white",
            font = UI_FONT,
            borderwidth = UI_BORDERWIDTH
        )

        self.definition_entry = tk.Entry(
            width = 30,
            bg = "white",
            font = UI_FONT,
            borderwidth = UI_BORDERWIDTH
        )

        self.delete_btn = tk.Button(
            text = "x",
            font = ("Arial", 15),
            bg = "#e0604c",
            fg = "black",
            command = self.mark_as_deleted
        )
    
    def mark_as_deleted(self):
        self.is_deleted = True
    