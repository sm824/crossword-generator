import tkinter as tk
from library import *
import UI.word_entry_box

class MainWindow:

    def __init__(self, RGB_colors):

        self.window_mode = "options"
        self.main_color = "#%02x%02x%02x" % RGB_colors

        self.root = tk.Tk()
        self.root.title("Crossword Generator")
        self.root.config(bg = self.main_color)
    
    def run_options(self):

        # Sizes the window to the proper dimensions for starting to set options
        self.root.geometry("600x400")

        # Creates the needed UI components
        self.added_words = []

        self.add_word_btn = tk.Button(
            text = "Add\nWord",
            font = UI_FONT,
            fg = self.main_color,
            command = lambda: self.added_words.append(tk.Label())
                              #
        )
        
    def run_crossword(self):

        pass

        # Sizes the window to the proper dimensions to fit the crossword
