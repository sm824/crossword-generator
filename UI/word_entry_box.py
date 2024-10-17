import tkinter as tk
from tkinter import messagebox
from library import *

class WordEntryBox:

    BOX_WIDTH = 375
    BOX_HEIGHT = 100

    box_color = "white"
    reduced_font = (UI_FONT[0], 12)
    box_collection = None
    box_frame = None

    def __init__(self, master, placement_row):

        # Creates the background bounds frame for this word entry box
        self.frame = tk.Frame(
            master = master,
            bg = WordEntryBox.box_color,  # Makes the background match the class's set color
            width = WordEntryBox.BOX_WIDTH,
            height = WordEntryBox.BOX_HEIGHT
        )

        # Stores this box's index in the collection it is located
        self.collection_index = placement_row

        # Creates the components inside the word entry box

        # TITLE
        self.box_title = tk.Label(
            master = self.frame,
            font = UI_FONT,
            text = ""
        )
        self.update_title_string()

        self.box_title.grid(
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
            command = self.confirm_delete_box
        )
        self.delete_btn.grid(
            column = 2,
            row = 0,
            padx = UI_PADDING,
            pady = UI_PADDING
        )

        # Adds the frame box to the window
        self.refresh_pos()

        self.frame.configure(
            height = WordEntryBox.BOX_HEIGHT,
            width = WordEntryBox.BOX_WIDTH
        )
    
    def refresh_pos(self):
        
        self.frame.grid(
            padx = UI_PADDING,
            pady = UI_PADDING,
            row = self.collection_index,
            column = 0
        )
    
    def update_title_string(self):

        self.box_title.config(
            text = f"Word Entry #{self.collection_index + 1}"
        )

        self.refresh_pos()

    def confirm_delete_box(self):
        """Pops up a dialog confirming that a word box is to be deleted.
        Deletes the box by calling self.delete_box() if the user agrees"""
            
        if (messagebox.askokcancel(
            "Confirm Deletion",
            "Deleting this box cannot be undone. Do you want to proceed?"
        )):
            self.delete_box()

    def delete_box(self):

        # Destroys this box's main frame
        self.frame.destroy()
        
        # Removes this box from the collection its object is stored in
        WordEntryBox.box_collection.pop(self.collection_index)

        # Updates the remaining boxes to have accurate numberings
        for this_box in range(len(WordEntryBox.box_collection)):
            WordEntryBox.box_collection[this_box].collection_index = this_box
            WordEntryBox.box_collection[this_box].update_title_string()

        print(f"Deleting entry #{self.collection_index + 1}")
