"""
****************************************************************************************************
Name: Sarah Mckenzie
Date: 2024-01-29

Purpose: This is a file to hold the classes CrosswordGrid and CrossowrdList, which is a subclass of list that has been made more suitable for storing the crossword grids generated in this project
****************************************************************************************************
"""
from library import *



class CrosswordGrid(list):

    def __init__(self, key, first_word_index, first_orientation, placed_word_indices, self_collection_index):
        """Adds the first word to self, with the orientation specified by first_orientation.
        The word added is put into placed_word_indices, and its grid_number and original_position attributes are set.
        
        Arguments:
            key = the collection in which the word objects are stored
            crosswords = the collection in which self can be found
            first_word_index = the index of the word that will be placed into self as the first word
            first_orientation = the orientation attribute of the first word, which is described by the above index
            placed_word_indices = the collection that holds the indices of the words that have already been placed
            self_collection_index = self's index in its own collection (the crosswords parameter)"""

        # Calls the list class's constructor to ensure the proper set-up of this child class's objects
        super(CrosswordGrid, self).__init__()

        self.crosswords_index = self_collection_index



        # Enters the first word into the crossword grid
        if first_orientation == "vertical":

            # Appends each character of the word to the first column, as its own row
            for char in key[first_word_index].word:
                self.append([char])

        else:  # If orientation is horizontal
            self.append([])
            
            # Appends each character of the word to the first row
            for char in key[first_word_index].word:
                self[0].append(char)
        
        # Sets the attributes for the first word, so it will work properly with all other words
        key[first_word_index].grid_number = self.crosswords_index
        key[first_word_index].original_position = [0, 0]  # The initial position will always be zero for a first word
        key[first_word_index].orientation = first_orientation

        placed_word_indices.append(first_word_index)
    


    def get_space_at(self, position):
        """Returns the item in self that can be found at the position entered. Raises IndexErrors
        
        position = formatted (x, y), this is the position of self that will be returned"""
        
        # Forces negative values to raise errors, rather than point to positions from the back
        if position[1] < 0 or position[0] < 0:
            raise IndexError
        
        return self[position[1]][position[0]]



    def place_word(self, word_obj):
        """Places the word into self.
        The word's orientation and original_position must be set prior to this method call.
        This method is not responsible for checking for clashes with other words, or for ensuring the grid's edge will not be met.

        word_obj is the word object being placed."""

        # Goes along the crossword, from word_obj's head position to its last letter
        for this_letter_space in range(len(word_obj.word)):

            # Places the word vertically
            if word_obj.orientation == "vertical":
                self[word_obj.original_position[1] + this_letter_space][word_obj.original_position[0]] = word_obj.word[this_letter_space]
            
            # Places the word horizontally
            else:
                self[word_obj.original_position[1]][word_obj.original_position[0] + this_letter_space] = word_obj.word[this_letter_space]



    def expand(self, space_ammount, orientation, key):
        """Expands the crossword the number of spaces specified by ammount.
        Positive values for ammount indicate the number of spaces to be added the right or bottom, while negatives will result in spaces added to the left or top of the crossword respectively.
        The latter will upset the original_position attributes of the words already placed, so this method will also change those positions to remain accurate.

        Arguments:
            orientation = "vertical" for orientation expands vertically, while "horizontal" expands horizontally.
            key = the collection that the key_entry objects are located in."""

        # Finds the direction the expansion should go, and makes the necessary changes for that direction to work (adjusting word position)
        if space_ammount > 0:
            direction = 1
    
        else:  # If ammount is a negative number or 0
            direction = -1
            space_ammount *= -1  # Makes space_ammount positive

            # Adjusts the positions of all the words located in self
            for this_word in self.get_present_words(key):

                if orientation == "vertical":
                    key[this_word].original_position[1] += space_ammount

                else:  # If it is horizontal
                    key[this_word].original_position[0] += space_ammount

    
        
        # Adding the spaces to self
        for added_line_space in range(space_ammount):

            # Adding rows to the top or bottom of self
            if orientation == "vertical":

                adding_row = [BLANK_CHAR for i in range(len(self[0]))]  # A row template to be copied onto self

                # Adding rows to the BOTTOM of self
                if direction == 1:
                    self.append(adding_row.copy())
                
                # If the direction is -1 (meaning the rows should be added to the TOP)
                else:
                    self.insert(0, adding_row.copy())
    

            # If orientation is "horizontal", add columns to the left or right of self
            else:

                rows = len(self)  # Calculates the height of self
                    
                # Repeats until the added column is as tall as the rest of the crossword
                for this_column in range(rows):

                    # Adding rows to the RIGHT of self
                    if direction == 1:
                        self[this_column].append(BLANK_CHAR)
            
                    # Adding rows to the LEFT of self
                    else:
                        self[this_column].insert(0, BLANK_CHAR)

    


    def get_present_words(self, key):
        """Returns the indices of the words that have been placed in self
        
        key = the collection tht the key_entry.KeyEntry word objects are stored in"""

        present_words = []

        # Checks the grid_number attribute of every word
        for this_word_index in range(len(key)):

            # If the current word's grid_number matches the index of self, add the word's index to the list of present words
            if key[this_word_index].grid_number == self.crosswords_index:
                present_words.append(this_word_index)
        
        return present_words



    def check_wings(self, current_position, word_orientation):
        """Returns True if there are no letters in the 'wings' of the current position, taking up the space to the top/bottom, or the left/right of current_position in self.
        Returns False if there are letters in either wing.
        
        Arguments:
            current_position = the position of the current letter (not either of the wing positions)
            word_orientation = the orientation of the word that the current letter is part of"""

        positions_empty = True

        # Test for the negative wing, then the positive wing
        for this_wing_offset in (-1, 1):
            try:

                # If the current wing (denoted by this_wing_offset) is occupied by a letter, set the positions_empty tracking variable to False
                if word_orientation == "vertical" and self.get_space_at((current_position[0] + this_wing_offset, current_position[1])).isalpha() or word_orientation == "horizontal" and self.get_space_at([current_position[0], current_position[1] + this_wing_offset]).isalpha():
                    positions_empty = False
                    break

            # If the wing position if off the grid, ignore it, because there cannot be letters there to clash with anyway
            except IndexError:
                pass

        return positions_empty
        


    def check_ends(self, sim_word_obj, sim_head_position, sim_orientation):
        """Checks the 'head tip' (position before the first letter) and the 'tail' (position after the last letter) for letters that may be placed there.
        Returns True if there are no clashes in the head or tail.
        Returns False if there is at least one clash in either.
        
        Arguments:
            sim_word_obj = the key_entry.KeyEntry object for the word having its ends checked
            sim_head_position = the position that the simulation word is being tested for
            sim_orientation = the orientation that the simulation word is being tested for"""

        ends_clear = True



        # Goes over the head tip, then tail position, to determine if they clash
        for this_tip_addition in (-1, len(sim_word_obj.word)):

            try:
                # If there is a clash at the current tip position, mark the ends as un-clear
                if sim_orientation == "vertical" and self.get_space_at((sim_head_position[0], sim_head_position[1] + this_tip_addition)).isalpha() or sim_orientation == "horizontal" and self.get_space_at((sim_head_position[0] + this_tip_addition, sim_head_position[1])).isalpha():
                    ends_clear = False

            # If the tip position is off of the grid, ignore it (other letters cannot be located off of the grid, so those positions cannot have clashes)
            except IndexError:
                pass



        return ends_clear



    @staticmethod
    def unify_crossword(crossword_grids, key):
        """Formats the list of crossword grids into a 2D string containing all of them, and returns it
        
        Arguments:
            crossword_grids = the collection that the crossword_grid.CrosswordGrid objects are stored in
            key = the collection that the key_entry.Key_Entry objects are stored in"""

        string_padding = " "
        added_x = 0  # Tracks how much should be added to each word's position to find its position in the unified grid

        # Finding the minimum height required to fit the largest of the crosswords
        height = 0

        for this_grid in crossword_grids:
            height = max(height, len(this_grid))

        # Create the container for the list of strings to represent each row
        full_crossword = [[] for i in range(height)]

        # Packs each grid into the full_crossword
        for this_grid_number in range(len(crossword_grids)):

            # Puts a column of empty spaces between the crossword grids so that the words do not touch
            for spacer in range(height):
                full_crossword[spacer].append(string_padding)

            # Adds to calculate what should be added to the x value of the new words' positions, to make up for the empty column added above
            added_x += 1

            # Places the items of this_grid_number's position in crossword_grids into full_crossword
            for y in range(len(crossword_grids[this_grid_number])):
                for x in range(len(crossword_grids[this_grid_number][y])):

                    if crossword_grids[this_grid_number][y][x] == BLANK_CHAR:  # If this space is empty (BLANK_CHAR is used to denote an empty space)
                        full_crossword[y] += string_padding

                    else:  # If this position holds a letter
                        full_crossword[y] += crossword_grids[this_grid_number][y][x]
                
                    # Assigns a full_grid_position to the current word
                    for this_grid_word in crossword_grids[this_grid_number].get_present_words(key):
                        key[this_grid_word].full_grid_position = key[this_grid_word].original_position.copy()  # Copies the word's original position onto the word's full_grid_position
                        key[this_grid_word].full_grid_position[0] += added_x  # Adds the required adjustment values to full_grid_position

            # Adds to calculate what should be added to the x value of the new words' positions, to make up for the new grid added above
            added_x += len(crossword_grids[this_grid_number][0])


            # Fills any gaps left in full_crossword beneath the crossword grid entered above, by working from the bottom up
            for y in range(height - len(crossword_grids[this_grid_number])):  # This expression determines how many rows were left blank with the insertion of the last crossword grid
                for x in range(len(crossword_grids[this_grid_number][0])):
                    full_crossword[height - y - 1] += string_padding  # Adds in each blank space
        
        return full_crossword
