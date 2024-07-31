"""
****************************************************************************************************
Name: Sarah Mckenzie
Date: 2024-01-29

Purpose: This is a library of functions and constants, the uses of which cannot limited to within a single file
****************************************************************************************************
"""
import easygui_qt as easy



ORIENTATION_OPTIONS = ("vertical", "horizontal")  # The options to choose from for each word, when its orientation is being decided

BLANK_CHAR = "*"  # The character used in the CrosswordGrid objects to denote a space that is not part of a word

KEY_WIDTH = 40  # The number of characters long each row of definition text is allowed to be in the formatted key


# The options for the user to choose from when prompted to perform an action on the generated crossword
USER_ACTIONS = (
    "Guess a Word",
    "View Answer Key",
    "View Interactive Crossword",
    "View User Manual",
    "Get Hint",
    "Quit"
)


# The text displayed when the user is shown the user manual
USER_MANUAL = f"""---  USING THE CROSSWORD GENERATOR  ---

-- Entering Words and Definitions --
    When prompted to enter words to make up the crossword, please avoid entering any numbers, symbols, or spaces, as these sorts of characters are not permitted in the crossword. The definition text, however, can have any number of special characters. You must enter at least 2 words for the crossword generation to begin, but you cannot enter more than 99.

-- Choosing an Action --
    The possible actions in the interactive crossword game are as follows:

       - \"{USER_ACTIONS[0]}\": Allows to to guess a word, provided you
                                 know its word number

       - \"{USER_ACTIONS[1]}\": Displays the crossword, with ALL
                                      the letters filled in
                                      
       - \"{USER_ACTIONS[2]}\": Displays the crossword
                                                    with ONLY guessed and
                                                    hint letters filled in

       - \"{USER_ACTIONS[3]}\": Displays this manual

       - \"{USER_ACTIONS[4]}\": Inserts a random letter, which will
                          show as blue, into an unfound word in
                          the crossword
                          
       - \"{USER_ACTIONS[5]}\": Stops the program

-- Viewing the Generated Crossword --
    Vertical words' numbers are shown in the top LEFT of their 'head' boxes (the box with that word's beginning letter). Horizontal words' numbers are shown in the top RIGHT of their 'head' boxes. This is important to note for words that intersect by their 'head' positions, as it is the only way to tell which number points to which word.
    Hint letters are in blue, as are the letters of the answer key. The letters you have guessed, however, are black in contrast.
    The window that is created when you choose to 'View Interactive Crossword' or 'View Answer Key' will take some time to be drawn. You must wait until the drawing is finished to move on. When you have finished looking at the crossword grid window, simply click on it to close it."""







def get_difference(coll1, coll2):
    """Returns all items present in coll1 that are absent from coll2 as a tuple.
    Note that the order of the items may be changed.
    
    Arguments:
        coll1 = the collection being subtracted from
        coll2 = the collection being subtracted"""

    return tuple(set(coll1) - set(coll2))



def show_user_manual():
    """Displays a dialog that explains how to use the crossword generator."""

    easy.show_message(USER_MANUAL, "User Manual")
