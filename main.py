"""
****************************************************************************************************
Name: Sarah Mckenzie
Date: 2024-01-29

Purpose: This is the main file of the Crossword Generator project. It collects the words, generates the crossword, and runs the interactive crossword-guessing game.
****************************************************************************************************
"""
import key_entry
import crossword_grid
import crossword_turtle
from library import *

import turtle
import random



# The position that is considered a 'corner' in the turtle window. All drawings that anchor to corners of the window rely on this constant
POSITIVE_CORNER = (950, 450)

# The text displayed in a corner of the crossword turtle window, which reminds the user how to tell which word a letter box's number points to
CROSSWORD_INFO_PANEL = """NOTES:
 - VERTICAL words have their numbers in the top LEFT of their boxes.
 - HORIZONTAL words have their numbers in the top RIGHT of their boxes"""






########## Introduces the user and explains the rules of the crossword generator ##########

# Asks the user if they would like to read the user manual
show_rules = easy.get_yes_or_no("Welcome to the crossword generator!\n\n  The Crossword Generator takes the words you enter, and randomly generates a crossword using them. The crossword can then be solved in the interactive crossword game that follows.\n    More information can be found in the User Manual.\n\nWould you like to read the User Manual?", "Welcome")

# If they want to read the user manual, show the user manual
if show_rules:
    show_user_manual()

# Tell the user that the next step is for them to enter words
easy.show_message("Click 'OK' to begin entering words for the crossword.", "Crossword Words")


##################################################  Getting the Words to be used in the Crossword  ##################################################

key = []  # The colection that will hold all of the KeyEntry word objects
word_number = 1  # Tracks which word number is being entered, so the user can know how many they have entered at any given moment



# Takes words from the user, storing them as KeyEntry objects, until the user presses 'cancel'
while True:
        
    # Gets the next word from the user, and stops asking is 'cancel' is clicked
    try:
        new_word_text = easy.get_string(
            f"What will word number {str(word_number)} be?\nClick cancel to finish.",
            "Enter Word",
            None  # Having None as a default value, for when the user clicks 'cancel', is used to detect when the user is finished entering words because it raises an error
        ).lower().strip()

    # Breaks the loop if 'cancel' is clicked
    except (TypeError, AttributeError):  # Since the default value of get_string() above is set to None, clicking cancel will raise an error because of the chained methods, which is how to user finishes entering words
        if word_number > 2:
            break
        
        # Forces the user to enter at least one word
        else:
            easy.show_message("You must have at least two words in the crossword", "Not enough words")
            continue
    


    # Checking if the word is a duplicate of one already present in the key
    if new_word_text in [key[this_word].word for this_word in range(len(key))]:
        easy.show_message("That word has already been entered once.\nPlease do not enter duplicate words.", "Duplicates Not Allowed")
        continue
    


    # Checking if the word contains any prohibited characters (numbers, symbols, spaces)
    for this_char in new_word_text:

        if not new_word_text.isalpha():  # If the word contains something that is not a letter

            if this_char.isdigit():
                bad_char_type = "numbers"

            else:  # if the bad character is a symbol or space
                bad_char_type = "symbols or spaces"
            
            easy.show_message(f"Please do not enter {bad_char_type} in your words.", "Characters Not Allowed")
            
        break
    
    # Goes back up, to make the user input a new word, if their last one included a bad character
    if not new_word_text.isalpha():
        continue
        


    # Asks for a definition for the word, since it has now been confirmed to be valid, and packs the word into the key with its definition    
    key.append(key_entry.KeyEntry(
        new_word_text,
        easy.get_string(f"What is the definition of '{new_word_text}'?", "Definition"),
    ))
    
    # Increments the word number, if the loop has gotten this far and is valid
    word_number += 1

    # Checks if the maximum number of words (99) has been reached
    if word_number > 99:
        easy.show_message("Maximum number of words reached.\nYou cannot enter more than 99 words.")
        break




########## Finishes setting up the key_entry.KeyEntry class ##########

key_entry.KeyEntry.collection = key

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




# Tells the user that their crossword has been generated
easy.show_message("Your crossword has been generated.", "Generation Finished")




############################################################ Allows the user to perform actions and view the generated crossword ############################################################

unified_crossword = crossword_grid.CrosswordGrid.unify_crossword(crossword_grids, key)
completed = False
selected_option = None

# While the user hasn't chosen to quit, ask them to select an action and perform it
while selected_option != USER_ACTIONS[-1]:  # The last index is "Quit"

    # Takes in an action from the user
    selected_option = easy.get_choice("Choose the action you would like to perform on the crossword:", "Choose Action", USER_ACTIONS)


    ########## Guessing a word ##########
    
    # Allows the user to guess a word
    if selected_option == USER_ACTIONS[0]:  # Index 0 is "Guess a Word"

        # Gets a word number from the user, and converts it into a word index by subtracting 1
        try:

            # Displays the unguessed word numbers to the user, so they can choose one to guess
            word_index = int(easy.get_choice("What is the number of the word\nyou would like to guess?", "Word Number", [str(i + 1) for i in get_difference(range(len(key)),
                                                                                                                                                            key_entry.KeyEntry.get_guessed_words()
                                                                                                                                                            )])) - 1
            
            # Gets the guess for the word from the user
            guessed_word_text = easy.get_string(f"Word definition:\n{key[word_index].definition}\n\nEnter your guess for this word:", "Word Text").lower().strip()

        # If the user clicked 'cancel' on either of the above dialogs, go back up, and ask for an action again
        except (TypeError, AttributeError):
            continue



        # If the guess was correct, mark the word as guessed
        if key[word_index].word == guessed_word_text:
            key[word_index].is_guessed = True
            result_message = f"'{guessed_word_text}' was correct!\nView the interactive crossword to see your progress."
        
        # If the guess was incorrect
        else:
            result_message = f"'{guessed_word_text}' was incorrect.\nClick 'Get Hint' in the actions menu, if you need help.\nClick 'View Answer Key' if you give up."

        # Show the user if they were correct or not, based off of the calculations above
        easy.show_message(result_message, "Result")



        # Checks if the above word was the last word in the crossword, and sets triggers to conclude the program if it was
        if len(key_entry.KeyEntry.get_letter_positions(key_entry.KeyEntry.ALL_LETTER_POSITIONS_FILTER)[0]) == len(key_entry.KeyEntry.get_all_showing_letters()):

            easy.show_message(f"Your guessed word '{guessed_word_text}' was the last unguessed word\nin the crossword.\n\nClick 'OK' to view the finished crossword")
            selected_option = USER_ACTIONS[2]
            completed = True  # A trigger that tells the program to put up a departure message, and close



    ########## Placing a hint ##########
        
    elif selected_option == USER_ACTIONS[4]:  # Index 4 is "Get Hint"

        # Gets the positions of all letters, hidden or shown
        all_letter_positions = key_entry.KeyEntry.get_letter_positions(key_entry.KeyEntry.ALL_LETTER_POSITIONS_FILTER)[0]
        
        showing_letter_positions = key_entry.KeyEntry.get_all_showing_letters()

        # Gets the positions of still-hidden letters, for use below
        hidden_letter_positions = get_difference(
            all_letter_positions,
            showing_letter_positions
        )

        # Gets a random position that is not already showing
        full_hint_position = random.choice(hidden_letter_positions)

        # Adds the hint index to every word whose letters occupies full_hint_position in the unified grid, creating a list of all showing words
        key_entry.KeyEntry.place_hint(full_hint_position)

        # If the last space was filled by hints
        if len(hidden_letter_positions) <= 1:
            
            easy.show_message("The last remaining spcae in the crossword\nwas filled by this hint.\n\nClick 'OK' to see the crossword.", "Crossword Finished")
            completed = True  # Trigger tells the program to put up a departure message, and close

            # Forces the program to show the unified crossword grid
            selected_option = USER_ACTIONS[2]

        # If there are still more hidden letter positions in the crossword
        else:
            easy.show_message(f"A new hint letter, '{unified_crossword[full_hint_position[1]][full_hint_position[0]]}', has been successfully added to the crossword.\n(hint letters are in blue when the crossword is displayed)\n\nClick 'View Interactive Crossword' to see it.", "Added Hint")

    

    ########## Showing the full crossword ##########
        
    # Shows the answer key, or the interactive crossword
    if selected_option == USER_ACTIONS[1] or selected_option == USER_ACTIONS[2]:  # Index 1 is "View Answer Key". Index 2 is "View Interactive Crossword"

        # Sets a trigger to draw the ANSWER KEY
        if selected_option == USER_ACTIONS[1]:
            guessed_letter_positions, hint_letter_positions = key_entry.KeyEntry.get_letter_positions(key_entry.KeyEntry.ALL_LETTER_POSITIONS_FILTER)
        
        # Sets a trigger to draw the INTERACTIVE CROSSWORD
        else:
            guessed_letter_positions, hint_letter_positions = key_entry.KeyEntry.get_letter_positions(key_entry.KeyEntry.SHOWING_LETTER_POSITIONS_FILTER)
        

        # Forces the crossword turtle to run after it is created, so it is not destroyed if it detects that it has run before
        turtle.TurtleScreen._RUNNING = True

        # Sets up the components used in the drawing of the crossword window
        win = turtle.Screen()
        win.title(selected_option.replace("View ", ""))  # Makes the title of the turtle window match the name of the action that was selected
        win.setup(width=1.0, height=1.0, startx=None, starty=None)  # Makes the window go fullscreen

        tl = crossword_turtle.CrosswordTurtle(35, win)
        tl.fillcolor("#F6F6F6")  # Sets the pale grey background color of the boxes in the crossword


        # Drawing the crossword
        tl.draw_whole_crossword(
            unified_crossword = unified_crossword,
            grid_anchor_position = (-POSITIVE_CORNER[0], POSITIVE_CORNER[1]),
            word_key = key,
            action = selected_option
        )



        # Drawing the key, which anchors to the bottom right of the window

        formatted_key = key_entry.KeyEntry.format_key()  # Creates a neat string copy of the key, to display definitions and word numbers
        
        # Getting into the bottom right corner, where the formatted key will be drawn
        tl.goto(
            POSITIVE_CORNER[0],
            -POSITIVE_CORNER[1]
        )

        # Draws the vertical, then horizontal key columns
        for this_key_column in formatted_key.values():

            # Moves to the position the current column should go
            tl.backward(KEY_WIDTH * tl.base_font[1])

            # Writes the current column
            tl.write(
                this_key_column,
                font=tl.base_font
            )
        


        # Drawing the info panel, which anchors to the bottom left of the screen
        
        # Going to the bottom left of the screen
        tl.goto(
            -POSITIVE_CORNER[0],
            -POSITIVE_CORNER[1]
        )

        # Writing the info panel
        tl.write(
            CROSSWORD_INFO_PANEL,
            font = tl.base_font
        )
            


        # Performing the last actions needed to make the window appear neat and work properly
        tl.hideturtle()
        win.exitonclick()



    ########## Viewing the user manual ##########
        
    elif selected_option == USER_ACTIONS[3]:  # Index 3 is "View User Manual"
        show_user_manual()

    

    ########## Shows a departure message, if the crossword was completely filled in ##########
    
    # completed is set to true when the user guesses the last word, or it is filled in entirely by hints
    if completed:
        easy.show_message("Crossword has been completed.\nClosing now.", "Departure Message")
        break



    ########## Asks the user if they really mean to quit, after they have pressed 'Quit' ##########

    if selected_option == USER_ACTIONS[-1]:  # "Quit" is at the last index in USER_ACTIONS

        confirmed_quit = easy.get_yes_or_no("Are you sure yous want to quit?\nThis crossword and its progress will be deleted.", "Confirm Quit")
        
        # Stops the loop from being broken, if they do not really want to quit
        if not confirmed_quit:
            selected_option = None

