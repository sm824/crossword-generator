"""
****************************************************************************************************
Name: Sarah Mckenzie
Date: 2024-01-29

Purpose: This is a file to hold the class CrosswordTurtle, a subclass of turtle that has added methods and constants to make it more suitable for drawing the generated crossword
****************************************************************************************************
"""
import turtle
import math

from library import *
import key_entry



class CrosswordTurtle(turtle.Turtle):

    FONT_NAME = "OCR A Extended"
    HINT_COLOR = "#7087F9"



    def __init__(self, component_size, window):
        """Sets beginning attributes, creates 2 main fonts, and puts self's pen up
        
        Arguments:
            component_size = the general size of the pictures drawn and words written by this turtle
            window = the turtle.Screen object that will be drawn on by the turtle"""

        # Calling the parent class's (turtle.Turtle's) constructor to ensure that this object is set up properly
        super(turtle.Turtle, self).__init__(window)

        # Determines what font size should be used for the main and small fonts, as well as later drawings
        self.component_size = component_size
        
        # Creates both main font attributes
        self.base_font = (
            CrosswordTurtle.FONT_NAME,
            int(component_size * (11/35))
        )
        self.small_font = (
            CrosswordTurtle.FONT_NAME,
            int(component_size * (8/35))
        )

        self.penup()



    def write_box_number(self, number, orientation):
        """Moves the turtle to write a small number in the corner of the letter box it is currently drawing.
        Numbers for vertical words will rest in the top LEFT corner.
        Numbers for horizontal words will rest in the top RIGHT corner.
        
        Arguments:
            number = the number to be written in the box corner (should correspond to the word that uses this box as its head)
            orientation = the orientation fo the word that the number is for"""

        header_travel_distance = self.component_size * 0.6  # Calculates how many pixels will go between the square's bottom and its header number, based off of the square's size
        offset_distance = self.component_size / 3.5  # Calculates how far back the header numbers must be placed in order to fit into the letter boxes

        # Sets the proper values to send header numbers for vertical words to the left corner of the letter box, and the numbers for horizontal words to the right corner. This prevents words that share a 'head' from having overlapping header numbers
        if orientation == "vertical":
            angle = 90

        else:  # If the orientation is horizontal
            angle = 45
            header_travel_distance = math.sqrt(header_travel_distance**2 * 2)  # Gets the hypotnuse of a triangle whose other sides are each the distance from the square's bottom to where the header numbers should go
    
        # Getting into the box's corner
        self.backward(offset_distance)
        self.left(angle)
        self.forward(header_travel_distance)

        # Writes the number in the corner
        self.write(number, font=(self.small_font[0], 8))

        # Getting back into position to continue drawing, now that the number is placed
        self.backward(header_travel_distance)
        self.right(angle)
        self.forward(offset_distance)



    def draw_square(self):
        """Draws a square with the self turtle, using self.component_size as the side length is pixels."""

        # Calculating the distance back that the square should be offset to center the square around the letters
        offset = self.component_size/3

        # Preparing to begin the square
        self.backward(offset)
        self.pendown()
        self.begin_fill()

        # Drawing the square's 4 sides
        for sides in range(4):
            self.forward(self.component_size)
            self.left(90)
    
        # Setting the turtle back to the way it was before it drew the square, so the program can continue seemlessly
        self.end_fill()
        self.penup()
        self.forward(offset)



    def draw_whole_crossword(self, unified_crossword, grid_anchor_position, word_key, action):
        """Draws the unified crossword on self's win attribute.
        This method should be called while self has its pen up, for best results.
        
        Arguments:
            unified_crossword = the formatted crossword produced by crossword_grid.CrosswordGrid.unify_crosswords method
            grid_anchor_position = the position that is considered to be the very top left corner of the window
            word_key = the collection that holds the word objects
            action = the string action selected by the user (should be one of the items in library.USER_ACTIONS)"""

        # Sets the showing letters to all letters, as an ANSWER KEY
        if action == USER_ACTIONS[1]:
            guessed_letter_positions, hint_letter_positions = key_entry.KeyEntry.get_letter_positions(key_entry.KeyEntry.ALL_LETTER_POSITIONS_FILTER)
        
        # Sets the showing letters to only hints and guessed words, as an INTERACTIVE CROSSWORD
        else:
            guessed_letter_positions, hint_letter_positions = key_entry.KeyEntry.get_letter_positions(key_entry.KeyEntry.SHOWING_LETTER_POSITIONS_FILTER)



        # Sets the beginning attributes
        self.speed(0)
        self.goto(grid_anchor_position)

        # Drawing the crossword
        for y in range(len(unified_crossword)):  # Repeats for every row in the crossword
            for x in range(len(unified_crossword[y])):  # Repeats for every individual value in the current row

                # Draws a square, if the position holds a letter
                if unified_crossword[y][x].isalpha():

                    self.draw_square()

                    # Checks the full_grid_position of every word, to determine if a header number is needed here
                    for this_word_index in range(len(word_key)):

                        # Draws a header number in the box, if the current full_grid_position is a word's head
                        if [x, y] == word_key[this_word_index].full_grid_position:
                            
                            self.write_box_number(
                                this_word_index + 1,  # The word's number
                                word_key[this_word_index].orientation,
                            )

                    # If the unifieid grid position holds a letter that should be shown
                    if (x, y) in guessed_letter_positions:

                        # Set the pen color to HINT_COLOR (light blue) if the user shose to see the ANSWER KEY
                        if action == USER_ACTIONS[1]:  # Index 1 is "View Answer Key"
                            self.pencolor(self.__class__.HINT_COLOR)
                        
                        # Writes the letter at the current position in the unified crossword
                        self.write(
                            unified_crossword[y][x],
                            font = self.base_font
                        )

                        # Sets the pen color back to default, in case it had been changed above
                        self.pencolor("black")



                    # If the position is a hint letter
                    elif (x, y) in hint_letter_positions:

                        # Set the pen color to HINT_COLOR (light blue) if it is a hint
                        self.pencolor(self.__class__.HINT_COLOR)

                        # Writes the letter in HINT_COLOR
                        self.write(
                            unified_crossword[y][x],
                            font = self.base_font,
                        )

                        # Changes the color back to black
                        self.pencolor("black")

                    
                # Moves up to the next grid position
                self.forward(self.component_size)

            # Moves to draw the next row, 1 space below the previous
            self.goto(grid_anchor_position[0], self.pos()[1] - self.component_size)
