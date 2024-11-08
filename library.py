"""
****************************************************************************************************
Name: Sarah Mckenzie
Date: 2024-01-29

Purpose: This is a library of functions and constants, the uses of which cannot limited to within a single file
****************************************************************************************************
"""
import easygui_qt as easy
import random
import crossword_grid

ORIENTATION_OPTIONS = ("vertical", "horizontal")  # The options to choose from for each word, when its orientation is being decided

BLANK_CHAR = "*"  # The character used in the CrosswordGrid objects to denote a space that is not part of a word

KEY_WIDTH = 40  # The number of characters long each row of definition text is allowed to be in the formatted key

UI_FONT = ("Cascadia Mono", 18)
UI_BORDERWIDTH = 4
UI_PADDING = 10
UI_BORDERWIDTH = 4

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



def generate_crossword(key):

    # adds an attribute called possible_intersections to each word that tracks what positions in every other word hold the same letter as which positions in themselves
    for this_word in range(len(key)):
        key[this_word].create_intersection_options()



    ##########  Preparing to generate the crossword  ##########

    currently_unplacable_words = []  # The words that cannot be placed in the current crossword, due to there being no possible intersection point, in every letter
    placed_word_indices = []
    crossword_grids = []
    current_grid = 0

    # Places the first word and creates the first crossword_grid.CrosswordGrid object to go in crossword_grids
    crossword_grids.append(crossword_grid.CrosswordGrid(
        key = key,
        placed_word_indices = placed_word_indices,
        first_orientation = random.choice(ORIENTATION_OPTIONS),
        first_word_index = random.choice(range(len(key))),
        self_collection_index = 0
    ))





    ############################################################  Generating the crossword  ############################################################

    # Places all other words until all are in a crossword grid
    while len(placed_word_indices) < len(key):



        ########## Choosing an unplaced word to focus on placing ##########

        # Locates a random word that has not been placed or declared currently un-placable yet
        try:
            attempt_word_index = random.choice(get_difference(

                # Gets the unplaced words
                get_difference(
                    range(len(key)),
                    placed_word_indices
                ),
                currently_unplacable_words
            ))
        
        

        ########## Create a new grid, if there are no more words to test ##########

        except IndexError:  # An IndexError is raised above if there are no words left that are compatible with the current grid

            # Create a new crossword grid, and use it as the current one
            current_grid += 1

            crossword_grids.append(crossword_grid.CrosswordGrid(
                key,
                random.choice(currently_unplacable_words),
                random.choice(ORIENTATION_OPTIONS),
                placed_word_indices,
                current_grid
            ))

            # Resets the unplacable words, so they can try to intersect with the new crossword's words
            currently_unplacable_words = []

            # Forces a new attempt word to be chosen, so the attempt word selection cannot become faulty
            continue

        


        ########## Choosing a placed word to focus on intersecting with ##########

        # While the attempt word is not considered un-placable yet. Breaks if attempt word has been placed
        while attempt_word_index not in currently_unplacable_words:

            # Finding an intersection (placed) word. Note that the word chosen here may still be unavailable, if it is nested in a place where the attempt word cannot intersect without clashing into other placed words
            try:
                intersection_word_index = random.choice(

                    # Finds all the words that are marked compatible with attempt word, which are also present in the current crossword grid
                    get_difference(

                        key[attempt_word_index].get_compatible_words(),

                        # Gets the words that are NOT placed yet, to remove from the word indices list above
                        get_difference(
                            range(len(key)),
                            placed_word_indices
                        )
                ))
        
            # Goes back to find a new attempt word, if the current one cannot intersect anywhere in the current crossword grid
            except IndexError:
                currently_unplacable_words.append(attempt_word_index)
                continue



            ########## Attempting to intersect the words ##########

            # Repeats until the attempt word is discovered to have no compatible intersection positions. Breaks if it is placed
            while len(key[attempt_word_index].get_compatible_letters(intersection_word_index)) > 0:



                # Finds a letter that matches at least one of the letters in the attempt word
                try:

                    # A choice of the intersection word letters marked compatible with the attempt word
                    intersection_letter_index = random.choice(key[attempt_word_index].get_compatible_letters(intersection_word_index))

                # If there are no remaining letters in the intersection word to test for compatibility
                except IndexError:
                    continue
                


                ########## Repeats until all the letters in attempt word have been checked to intersect with the current letter in intersection word, or one letter is found to work ##########

                # Repeats until the attempt word's matching_indices attribute lists the intersection word's current letter as un-intersectable. Breaks if attempt word is placed
                while len(key[attempt_word_index].possible_intersections[intersection_word_index][intersection_letter_index]) > 0:
            


                    ########## Preparing the test attributes for the simulation ##########

                    # Chooses a random letter index in the attempt word, to focus on, which is not marked as impossible yet
                    attempt_letter_index = random.choice(key[attempt_word_index].possible_intersections[intersection_word_index][intersection_letter_index])

                    # Sets the test orientation for the attempt word to be the oppsite of the intersection word's, because that is the only way they can intersect
                    sim_orientation = get_difference(ORIENTATION_OPTIONS, (key[intersection_word_index].orientation,))[0]

                    # Getting a test position for the attempt word, from which it would intersect
                    sim_head_position = key[attempt_word_index].get_sim_position(
                        sim_orientation,
                        key[intersection_word_index],
                        intersection_letter_index,
                        attempt_letter_index
                    )



                    ########## Testing if the word clashes when using the attributes calculated above ##########

                    clash = False
                    required_expansions = []


                    # Checks for clashes from the intersection position, outwards to either side (this way it is easy to find the grid edge, if the grid needs to be expanded to fit the word)

                    # Stores two sequence of addition factors for the simulation word's positions, one going from the intersection point to the word's end (positive), the other from the intersection point to the word's beginning (negative)
                    side_sequences = [range(attempt_letter_index + 1, len(key[attempt_word_index].word)), range(attempt_letter_index - 1, -1, -1)]

                    # Checks for clashes with the first side_sequence (positive side), then the second (negative side)
                    for position_factor_sequence in side_sequences:

                        # Performs the clash checking. IndexErrors mean the grid edge has been met
                        try:

                            # Checks if the word clashes, moving down/up from the intersection point
                            if sim_orientation == "vertical":

                                # Iterates over every letter in attempt word that comes after/before the intersection, EXCLUDING the letter of the intersection itself
                                for this_position_increment in position_factor_sequence:

                                    # Tests if the word clashes at the current position, and that that clash site has a DIFFERENT letter than the one in attempt word (if it was the same, the site could be allowed to intersect as a second intersection)
                                    if crossword_grids[current_grid].get_space_at((sim_head_position[0], sim_head_position[1] + this_position_increment)).isalpha() and crossword_grids[current_grid].get_space_at((sim_head_position[0], sim_head_position[1] + this_position_increment)) != key[attempt_word_index].word[attempt_letter_index]:
                                        clash = True
                                        break


                                    # If the position is not a letter, check its side positions (or 'wings') for clashes
                                    else:
                                    
                                        # Check the wings of the position for clashes
                                        if not crossword_grids[current_grid].check_wings((sim_head_position[0], sim_head_position[1] + this_position_increment), "vertical"):
                                            clash = True
                                            break



                            # Tests if the word clashes moving right/left from the intersection point
                            else:

                                # Iterates over every letter in attempt word that comes AFTER the intersection, EXCLUDING the letter of the intersection itself
                                for this_position_increment in position_factor_sequence:

                                    # Tests if the word clashes at the current position, and that that clash site has a DIFFERENT letter than the one in attempt word (if it was the same, the site could be allowed to intersect as a second intersection)
                                    if crossword_grids[current_grid].get_space_at((sim_head_position[0] + this_position_increment, sim_head_position[1])).isalpha() and crossword_grids[current_grid].get_space_at((sim_head_position[0] + this_position_increment, sim_head_position[1])) != key[attempt_word_index].word[attempt_letter_index]:
                                        clash = True
                                        break

                                
                                    # If the position is not a letter, check its wings for clashes
                                    else:
                                    
                                        # Check the wings of the position for clashes
                                        if not crossword_grids[current_grid].check_wings((sim_head_position[0] + this_position_increment, sim_head_position[1]), "horizontal"):
                                            clash = True
                                            break
                

                        # If the edge of the crossword grid was met, mark that it will need to be exapnded for the attempt word to be added (it will only be added if there are NO letter clashes whatsoever)
                        except IndexError:

                            # Calculates the number of positions there needs to be beyond the crossword grid's POSITIVE edge
                            if this_position_increment > attempt_letter_index:
                                required_expansions.append(len(key[attempt_word_index].word) - this_position_increment)

                            # Calculates the number of positions there needs to be past the crossword grid's NEGATIVE edge
                            else:
                                required_expansions.append(-this_position_increment - 1)





                    # Checks the positions before the head, and after the first word ('head tip' and 'tail') for clashes         
                    if not crossword_grids[current_grid].check_ends(key[attempt_word_index], sim_head_position, sim_orientation):
                        clash = True
                


                    # Removes the incompatible letter from the list of intersection options, if it was discovered to be un-intersectable with the setup of the current crossword
                    # If any one clash accured above, mark the simulated intersection as impossible and go back up to select a new letter in attempt word
                    if clash:
                        key[attempt_word_index].possible_intersections[intersection_word_index][intersection_letter_index].remove(attempt_letter_index)
                        continue



                    ########## Adds the word to the current crossword, since it does not clash ##########

                    # Setting the attempt words's attributes, which are required for it to be placed, and for its position to be accurate if the grid needs to be expanded before
                    key[attempt_word_index].original_position = sim_head_position
                    key[attempt_word_index].orientation = sim_orientation
                    key[attempt_word_index].grid_number = current_grid


                    # Expands the crossword the required ammount to fit the attempt word
                    for this_expansion in required_expansions:

                        crossword_grids[current_grid].expand(
                            this_expansion,
                            sim_orientation,
                            key
                        )
        
                    
                    # Puts the attempt word into the crossword
                    crossword_grids[current_grid].place_word(key[attempt_word_index])

                    # Preparing tracking variables for the next attempt word
                    currently_unplacable_words = []
                    placed_word_indices.append(attempt_word_index)

                    # Ending the loop, because the word was placed above
                    break


                # If the attempt word was placed, move on to choose a new attempt word
                if attempt_word_index in placed_word_indices:
                    break


            # If the attempt word was placed, move on to choose a new attempt word
            if attempt_word_index in placed_word_indices:
                break
    


    return crossword_grids


