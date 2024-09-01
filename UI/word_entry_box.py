import tkinter as tk
from library import *

class WordEntryBox:

    BOX_WIDTH = 375
    BOX_HEIGHT = 100

    box_color = "white"
    reduced_font = (UI_FONT[0], 12)

    def __init__(self, master, placement_row):

        # Creates the background bounds frame for this word entry box
        self.frame = tk.Frame(
            master = master,
            bg = WordEntryBox.box_color,  # Makes the background match the class's set color
            width = WordEntryBox.BOX_WIDTH,
            height = WordEntryBox.BOX_HEIGHT
        )

        self.is_deleted = False

        # Creates the components inside the word entry box

        # TITLE
        self.word_prompt = tk.Label(
            master = self.frame,
            font = UI_FONT,
            text = f"Word Entry #{placement_row + 1}"
        )
        self.word_prompt.grid(
            column = 0,
            row = 0
        )

        # WORD ENTRY PROMPT LABEL
        self.word_prompt = tk.Label(
            master = self.frame,
            font = WordEntryBox.reduced_font,
            text = "Word: "
        )
        self.word_prompt.grid(
            column = 0,
            row = 1
        )

        # WORD ENTRY
        self.word_entry = tk.Entry(
            master = self.frame,
            width = 12,
            bg = "white",
            font = WordEntryBox.reduced_font,
            borderwidth = UI_BORDERWIDTH
        )
        self.word_entry.grid(
            column = 1,
            row = 1
        )

        # DEFINITION PROMPT LABEL
        self.definition_prompt = tk.Label(
            master = self.frame,
            font = WordEntryBox.reduced_font,
            text = "Definition: "
        )
        self.definition_prompt.grid(
            column = 0,
            row = 2
        )

        # DEFINITION ENTRY
        self.definition_entry = tk.Text(
            master = self.frame,
            width = 20,
            height = 3,
            bg = "white",
            font = WordEntryBox.reduced_font,
            borderwidth = UI_BORDERWIDTH
        )
        self.definition_entry.grid(
            column = 1,
            row = 2
        )

        # WORD ENTRY DELETION BUTTON
        self.delete_btn = tk.Button(
            master = self.frame,
            text = " x ",
            font = ("Arial", 15),
            bg = "#e0604c",
            fg = "black",
            command = self.mark_as_deleted
        )
        self.delete_btn.grid(
            column = 2,
            row = 0,
            padx = UI_PADDING,
            pady = UI_PADDING
        )

        # Adds the frame box to the window
        self.frame.grid(
            padx = UI_PADDING,
            pady = UI_PADDING,
            row = placement_row,
            column = 0
        )

        self.frame.configure(
            height = WordEntryBox.BOX_HEIGHT,
            width = WordEntryBox.BOX_WIDTH
        )
    
    def mark_as_deleted(self):
        self.is_deleted = True
    