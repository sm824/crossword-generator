import tkinter as tk
from library import *
import UI.word_entry_box

class MainWindow:

    def __init__(self, RGB_colors):

        self.window_mode = "options"
        self.main_color = "#%02x%02x%02x" % RGB_colors  # Converts RGB to HEX colors
        self.entered_words = []

        self.root = tk.Tk()
        self.root.title("Crossword Generator")
        self.root.config(bg = self.main_color)
    
    def run_options(self):

        # Creates the needed UI components
        self.word_entries = []

        # Creates and adds the 'add word entry' button
        self.add_word_btn = tk.Button(
            text = "+",
            font = (UI_FONT[0], 30),
            cursor = "hand2",
            command = self.add_word_entry,
            width = 3
        )
        self.padded_grid(self.add_word_btn, 1, 0)

        # Creates and adds the generate crossword button
        self.generate_btn = tk.Button(
            text = "Generate Crossword",
            font = UI_FONT,
            cursor = "hand2",
            height = 2,
            #command = 
        )
        self.padded_grid(self.generate_btn, 0, 0)

        # Creates and adds the frame for the word entry widgets to sit in
        self.entries_frame = tk.Frame(
            bg = "white",
            cursor = "hand2"
        )
        self.entries_frame.grid(
            column = 0,
            row = 1,
            columnspan = 2,
            padx = UI_PADDING
        )

        UI.word_entry_box.WordEntryBox.box_color = self.main_color
        UI.word_entry_box.WordEntryBox.box_collection = self.entered_words
        UI.word_entry_box.WordEntryBox.box_frame = self.entries_frame

    def run_crossword(self):

        pass

        # Sizes the window to the proper dimensions to fit the crossword
    
    def add_word_entry(self):

        placement_row = len(self.entered_words)
        
        self.entered_words.append(
            UI.word_entry_box.WordEntryBox(
                placement_row = placement_row,
                master = self.entries_frame
            )
        )

        print(self.entered_words)

    def padded_grid(self, widget, column, row):
        widget.grid(
            padx = UI_PADDING,
            pady = UI_PADDING,
            row = row,
            column = column,
        )
