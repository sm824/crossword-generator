import tkinter as tk
from library import *
import UI.word_entry_box
import key_entry

class MainWindow:

    def __init__(self, RGB_colors):

        self.window_mode = "options"
        self.main_color = "#%02x%02x%02x" % RGB_colors  # Converts RGB to HEX colors
        self.entered_word_boxes = []
        self.entered_word_objects = []

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
            command = self.run_crossword
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
        UI.word_entry_box.WordEntryBox.box_collection = self.entered_word_boxes
        UI.word_entry_box.WordEntryBox.box_frame = self.entries_frame

    def run_crossword(self):

        # Saves word entries as key_entry objects before their boxes are destroyed
        for this_word_entry in self.entered_word_boxes:
            self.entered_word_objects.append(
                key_entry.KeyEntry(
                    this_word_entry.word_entry.get(),
                    this_word_entry.definition_entry.get("1.0")  # Argument required for text box (tk.Text)
                )
            )

        # Iterates over and deletes all the previous widgets
        for this_widget in self.root.winfo_children():
            this_widget.destroy()
        
        for i in self.entered_word_objects:
            print(f"{i.word} = {i.definition}")

        # Sets up the new UI, where the generated crossword will be displayed

        # Sizes the window to the proper dimensions to fit the crossword
        self.root.geometry("800x800")
    
    def add_word_entry(self):

        placement_row = len(self.entered_word_boxes)
        
        self.entered_word_boxes.append(
            UI.word_entry_box.WordEntryBox(
                placement_row = placement_row,
                master = self.entries_frame
            )
        )

        print(self.entered_word_boxes)

    def padded_grid(self, widget, column, row):
        widget.grid(
            padx = UI_PADDING,
            pady = UI_PADDING,
            row = row,
            column = column,
        )
