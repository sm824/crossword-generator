"""
****************************************************************************************************
Name: Sarah Mckenzie
Date: 2024-01-29
Class: CS 20
Project: Capstone Project - Crossword Generator

Purpose: This is a file for the class KeyEntry, which is used to store the words that the interactive game and the generator work with
****************************************************************************************************
"""
from library import *



class KeyEntry:

    ALL_LETTER_POSITIONS_FILTER = 0
    SHOWING_LETTER_POSITIONS_FILTER = 1

    collection = None



    def __init__(self, word_text, definition_text):
        """Creates the necessary base attributes for self to function
        
        Arguments:
            word_text = the string text of the word being created
            definition_text = the string definition text of the word being created, which will be displayed to the user when guessing words"""

        # NOTE: grid_number and original_head_position should be removed from the parameter list in the end, since they will only be determined once the words have been placed, and not when the objects are first created

        self.definition = definition_text
        self.word = word_text

        self.original_position = []
        self.full_grid_position = []  # This must be a list, so it can be set to its own value later when the full grid is generated

        self.grid_number = None
        self.orientation = None
        self.hint_indices = []  # Stores the number of letters down in the word each hint for this word can be found

        self.is_guessed = False
    


    def get_compatible_words(self):
        """Returns a list of the indices of words that have at least one letter able to intersect with self, according to self's possible_intersections."""

        compatible_words = []

        # Goes over every letter list in every word list in self.possible_intersections
        for intersection_word in range(len(self.possible_intersections)):
            for intersection_letter in range(len(self.possible_intersections[intersection_word])):

                # If the letter is compatible, add its word's index to the list of compatible words, and skip to the next word
                if len(self.possible_intersections[intersection_word][intersection_letter]) > 0:
                    compatible_words.append(intersection_word)
                    break
    
        return compatible_words



    def get_compatible_letters(self, *letter_word_indices):
        """Returns the indices of all the letters in letter_word_indices that have at least one matching letter in self.
        
        letter_word_indices = the indices of all words in the word object collection that this method is the return the compatible indices for"""

        compatible_letters = []

        # Repeats for every word given to find matching letters with
        for this_word in letter_word_indices:

            # Repeats for every letter in the current word
            for this_letter in range(len(self.__class__.collection[this_word].word)):

                # If the current other letter has at least one intersection possibility listed, add the letter's index to the compatible letters list
                if len(self.possible_intersections[this_word][this_letter]) > 0:
                    compatible_letters.append(this_letter)

        return compatible_letters
        


    
    def create_intersection_options(self):
        """Creates a structure to track which indices in self's word can intersect with which indices inother words.
        The attribute, matching_intersections, is structured like this:

          [OTHER WORDS (each index is the word that index corresponds to)
              [OTHER WORDS' LETTERS (each index is the word that index corresponds to)
                  [SELF'S LETTERS]]] (items are the indices. Note the difference compared with the 2 levels above)

        Note that self's OTHER_WORDS positions in both collections will be completely irrelevent, since self's word will never be required to intersect with itself."""

        self.possible_intersections = []


        ########## Generates the intersection lists for each word in self_collection ##########

        # Repeats for every word
        for other_word_index in range(len(self.__class__.collection)):
            self.possible_intersections.append([])

            # Repeats for every letter in the current word
            for other_letter_index in range(len(self.__class__.collection[other_word_index].word)):
                self.possible_intersections[other_word_index].append([])

                # Repeats for every letter in self
                for self_letter_index in range(len(self.word)):

                    # If the current letter of self matches the current letter of the other word, add self's letter's index to the possible intersections
                    if self.word[self_letter_index] == self.__class__.collection[other_word_index].word[other_letter_index]:
                        self.possible_intersections[other_word_index][other_letter_index].append(self_letter_index)

    


    def get_sim_position(self, sim_orientation, intersection_word_obj, intersection_letter_index, attempt_letter_index):
        """Returns the position that would be held by self if it were to intersect with a certain word.
        
        Arguments:
            sim_orientation = 'vertical' or 'horizontal', this is the orientation used by self in the simulation.
            intersection_word = the word object pointed to by intersection_word_index.
            intersection_letter_index = the index that denotes which letter in the text of the intersection word is supposed to be the site of the intersection.
            attempt_letter_index = the index of self's letter which matches as is to intersect with the letter described by intersection_letter_index"""

        # Copies the position of the intersection word, from which the test position for attempt word will be calculated below
        sim_head_position = intersection_word_obj.original_position.copy()


        
        ########## Adjusting sim_head_position to find the position from which it intersects properly ##########

        if sim_orientation != "vertical":  # If the intersection word is vertical, and the attempt word is horizontal

            # Adjusting sim_head_position to be where the attempt word's 'head' should be to intersect
            sim_head_position[1] += intersection_letter_index
            sim_head_position[0] -= attempt_letter_index

            
        else:  # If the intersection word is vertical, and the attempt word is horizontal

            # Adjusting sim_head_position to be where the attempt word's 'head' should be to intersect
            sim_head_position[0] += intersection_letter_index
            sim_head_position[1] -= attempt_letter_index

        return sim_head_position

    

    @classmethod
    def get_all_showing_letters(cls):
        """Returns the indices of all the letters in the crossword that should be showing.
        Ignores whether they are guessed or filled by hints."""

        # Calculates which positions are hint letters and which positions are the letters of guessed words (initially, showing_letter_positions will only hold the positions taken up by guessed words' letters)
        showing_letter_positions, hint_letter_positions = cls.get_letter_positions(cls.SHOWING_LETTER_POSITIONS_FILTER)
        
        # Appends all the hint letter positions onto the end of the guessed words' letters' position
        showing_letter_positions.extend(hint_letter_positions)

        return showing_letter_positions
    


    @classmethod
    def get_letter_positions(cls, filter):
        """Returns the positions occupied by letters that fit under the category of the given filter. (as a list)

        filter = a factor that determines which letter positions will be returned, and which will not.
                 0 or ALL_LETTER_POSITIONS_FILTER will return every position occupied by a letter.
                 1 or SHOWING_LETTER_POSITIONS_FILTER will return every position occupied by a letter that is a hint, or part of a guessed word"""

        guessed_positions = []
        hint_positions = []

        # Goes over all the words, and finds the words that have been guessed
        for this_position_index in range(len(cls.collection)):
            
            # Adds all the letter indices in the word to guessed_positions, if the current word has already been guessed
            if cls.collection[this_position_index].orientation == "vertical":

                # If the current word is eligible to be shown, according to the given filter
                if filter == cls.SHOWING_LETTER_POSITIONS_FILTER and cls.collection[this_position_index].is_guessed or filter == cls.ALL_LETTER_POSITIONS_FILTER:

                    # Goes over the positions of the letters in the word, adding each to guessed_positions
                    for this_letter_index in range(len(cls.collection[this_position_index].word)):
                        guessed_positions.append((
                            cls.collection[this_position_index].full_grid_position[0],
                            cls.collection[this_position_index].full_grid_position[1] + this_letter_index
                        ))

                # Finds the hints in the word and adds their positions to guessed_positions
                for this_hint_index in cls.collection[this_position_index].hint_indices:
                    hint_positions.append((
                        cls.collection[this_position_index].full_grid_position[0],
                        cls.collection[this_position_index].full_grid_position[1] + this_hint_index,  # after + used to be: cls.collection[this_position_index].hint_indices[this_hint_index]
                    ))
            

            else:  # If the orientation is "horizontal"
                
                # If the current word is eligible to be shown, according to the given filter
                if filter == cls.SHOWING_LETTER_POSITIONS_FILTER and cls.collection[this_position_index].is_guessed or filter == cls.ALL_LETTER_POSITIONS_FILTER:

                    # Goes over the positions of the letters in the word, adding each to guessed_positions
                    for this_letter_index in range(len(cls.collection[this_position_index].word)):
                        guessed_positions.append((
                            cls.collection[this_position_index].full_grid_position[0] + this_letter_index,
                            cls.collection[this_position_index].full_grid_position[1]
                        ))
                
                # Finds the hints in the word and adds their positions to guessed_positions
                for this_hint_index in cls.collection[this_position_index].hint_indices:
                    hint_positions.append((
                        cls.collection[this_position_index].full_grid_position[0] + this_hint_index,  # after + used to be: cls.collection[this_position_index].hint_indices[this_hint_index],
                        cls.collection[this_position_index].full_grid_position[1]
                    ))
            
        return guessed_positions, hint_positions

    
    
    @classmethod
    def format_key(cls):
        """Formats 2 strings, one for vertical and one for horizontal, out of the key.
        Each holds a list of word numbers and their definitions."""

        # Creating the display key with its headers
        display_key = {
            "vertical": "-- Vertical --\n",
            "horizontal": "-- Horizontal --\n"
        }

        # Adds every word's definition to its respective orientation column in display_key, after it has been formatted
        for this_word in range(len(cls.collection)):

            # Creates a list of the characters in the current word's definition
            definition_characters = list(cls.collection[this_word].definition)


            # Finds if the word's number has 1 or 2 digits, and sets the space to be offset accordingly

            if this_word < 9:  # If the word number has 1 digit
                offset_space = 3
            
            else:  # If the word number has 2 digits
                offset_space = 4

            
            # Places a newline character every few characters in the definition characters (influenced by KEY_WIDTH), so the rows line up with the number it will be placed behind
            for this_row in range(KEY_WIDTH - offset_space, len(definition_characters), KEY_WIDTH - offset_space):
                definition_characters.insert(
                    this_row,
                    "\n" + " " * offset_space
                )

            # Concatenates the word number and the definition to the display_key in its respective orientation
            display_key[cls.collection[this_word].orientation] += f"{this_word + 1}. {''.join(definition_characters)}\n"

        return display_key
    


    @classmethod
    def get_guessed_words(cls):
        """Returns the indices of all the words that have been guessed"""

        guessed_word_indices = []

        # Finds every word that is marked as guessed, and add them to guessed_word_indices
        for this_word_index in range(len(cls.collection)):

            # If the current word is guessed, add it to guessed_word_indices
            if cls.collection[this_word_index].is_guessed:
                guessed_word_indices.append(this_word_index)
        
        return guessed_word_indices
    


    @classmethod
    def place_hint(cls, hint_position):
        """Adds hint_position to the hint_indices attribute of all the words that are found to occupy hint_position with their letters in the unified crossword grid.
        
        hint_position = the position where the hint is to be placed in whichever crossword grid it is to be placed in"""

        # Iterates for every letter, in every word in cls.collection
        for this_word_index in range(len(cls.collection)):
            for this_letter_index in range(len(cls.collection[this_word_index].word)):

                # If the current word's current letter position matches the hint_position given, add the current word's current position to its own hint_indices attribute
                if cls.collection[this_word_index].orientation == "vertical" and hint_position == (cls.collection[this_word_index].full_grid_position[0], cls.collection[this_word_index].full_grid_position[1] + this_letter_index) or cls.collection[this_word_index].orientation == "horizontal" and hint_position == (cls.collection[this_word_index].full_grid_position[0] + this_letter_index, cls.collection[this_word_index].full_grid_position[1]):
                    cls.collection[this_word_index].hint_indices.append(this_letter_index)
    