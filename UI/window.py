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
            cursor = "hand2",
            relief = "sunken",
            borderwidth = UI_BORDERWIDTH
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

    def create_option_btn(self, text, command):

        return tk.Button(
            master = self.options_frame,
            text = text,
            command = command,
            font = (UI_FONT[0], 12)
        )

    def export_pdf(self):
        pass

    def edit_words():
        pass

    def get_hint():
        pass
    
    def view_answer_key():
        pass

    def run_crossword(self):

        # Saves word entries as key_entry objects before their boxes are destroyed
        for this_word_entry in self.entered_word_boxes:
            self.entered_word_objects.append(
                key_entry.KeyEntry(
                    this_word_entry.word_entry.get(),
                    this_word_entry.definition_entry.get("1.0", "end-1c")  # Argument required for text box (tk.Text)
                )
            )

        # Iterates over and deletes all the previous widgets
        for this_widget in self.root.winfo_children():
            this_widget.destroy()
        
        for i in self.entered_word_objects:
            print(f"{i.word} = {i.definition}")

        # Sets up the new UI, where the generated crossword will be displayed
        self.options_frame = tk.Frame(
            master = self.root,
            bg = "grey",
            relief = "sunken",
            width = 250,
            height = 70,
            borderwidth = UI_BORDERWIDTH
        )
        self.options_frame.grid(row=0, column=0)

        # Creates the option buttons that sit at the window's top
        self.option_buttons = {
            "Export PDF": self.create_option_btn("Export PDF", self.export_pdf),
            "Edit Words": self.create_option_btn("Edit Words", self.edit_words),  # This requires the crossword be re-generated, and it may look different
            "Get Hint": self.create_option_btn("Get Hint", self.get_hint),
            "View Answer Key": self.create_option_btn("View Answer Key", self.view_answer_key)
        }

        # Adds the above created option buttons to the window
        for this_button_obj in range(len(self.option_buttons)):
            list(
                self.option_buttons.items())[this_button_obj][1].grid(
                    column = this_button_obj,
                    row = 0,
                    padx =  UI_PADDING / 2,
                    pady = UI_PADDING / 2
                )

        # The canvas widget that holds the generated crossword
        self.crossword_canvas = tk.Canvas(
            master = self.root,
            bg = "white",
            relief = "sunken",
            borderwidth = UI_BORDERWIDTH,
            width = 1000,
            height = 800
        )
        self.crossword_canvas.grid(
            column = 0,
            row = 1,
            pady = UI_PADDING,
            padx = UI_PADDING
        )

        # The frame widget to hold the key (word definitions)
        self.definitions_frame = tk.Frame(
            master = self.root,
            relief = "sunken",
            borderwidth = UI_BORDERWIDTH,
            width = 200,
            height = 865
        )
        self.definitions_frame.grid(
            column = 2,
            row = 0,
            rowspan = 2,
            pady = UI_PADDING,
            padx = UI_PADDING
        )

        # Sizes the window to the proper dimensions to fit the crossword
        self.root.geometry("1256x888")
    
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
