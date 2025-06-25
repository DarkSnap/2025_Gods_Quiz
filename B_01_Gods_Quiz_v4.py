import csv
import random
from tkinter import *
from functools import partial


def get_gods_name_desc():
    """Retrieves gods from CSV file."""
    with open("gods.csv", "r", newline="", encoding="utf-8") as file:
        all_gods = list(csv.reader(file, delimiter=","))

    all_gods.pop(0) # Separates each row of the csv into separate lists of items
    return all_gods

def get_round_gods_desc(quiz_type):
    """Choose gods depending on the quiz type."""
    all_gods_list = get_gods_name_desc()

    if quiz_type == 1: # Greek / Roman Quiz, returns a God/Goddess's name and their origin
        potential_god = random.choice(all_gods_list) # Selects random God/Goddess from list
        return potential_god[2], potential_god[0]

    elif quiz_type == 2: # Gods Name Quiz, Selects 4 Gods
        round_gods = []
        round_god_description = set()

        while len(round_gods) < 4: # Randomly selects 4 gods
            potential_god = random.choice(all_gods_list)
            if potential_god[3] not in round_god_description: # Skips if the same god is selected
                round_gods.append(potential_god)
                round_god_description.add(potential_god[3])

        god_description = random.choice(list(round_god_description)) # Selects a god/goddess's description from available gods
        return round_gods, god_description # Returns their names and one of their descriptions

# Class starts here
class StartQuiz:

    def __init__(self):

        """
        Gets number of rounds from user
        """

        # Creates gui frame
        self.start_frame = Frame(padx=60, pady=30)
        self.start_frame.grid()

        # Strings for labels

        # Game Description String
        intro_string = ("Greek/Roman - By selecting Greek/Roman you will get a god/goddess's name, "
                     "you have pick whether the god/goddess is of greek or roman origin.\n\n"
                     "God's Name - By selecting God's Name you will get a description for a god/goddess "
                     "you will be given 4 options, 1 of them is the correct god.\n\n"
                     "Mixed - Takes questions from both Greek/Roman and God's Name Quiz randomly.")

        # Quiz Choice Selection String
        choose_string = "How many rounds do you want to play?"

        # List of labels to be made (text | font | fg)
        start_labels_list = [
            ["Gods Quiz", ("Arial", "16", "bold"), None],
            [intro_string, ("Arial", "12"), None],
            [choose_string, ("Arial", "20", "bold"), "#009900"]
        ]

        # Create labels and add them to the reference list...
        start_label_ref = []
        for count, item in enumerate(start_labels_list):
            make_label = Label(self.start_frame, text=item[0], font=item[1],
                               fg=item[2],
                               wraplength=600, justify="left", pady=10, padx=20, bg="#ffe6cc")
            make_label.grid(row=count)

            start_label_ref.append(make_label)

        self.choose_label = start_label_ref[2]

        # Frame for Quiz Type Radio Buttons
        self.quiztype_area_frame = Frame(self.start_frame)
        self.quiztype_area_frame.grid(row=3)

        # Frame for entry box and start button.
        self.entry_area_frame = Frame(self.start_frame)
        self.entry_area_frame.grid(row=4)

        # Value used to find which quiz is selected
        self.quiz_type = StringVar()
        self.quiz_type.set("0")

        # Quiz Type radio button items list
        quiz_type_list = [[self.quiztype_area_frame, ("Arial", "20", "bold"), self.quiz_type, 1, 0, "Greek / Roman", 12, 1, "#FF9999", "black", "#f5a3a3", 1, 0, 7, 10],
                          [self.quiztype_area_frame, ("Arial", "20", "bold"), self.quiz_type, 2, 0, "God Name", 12, 1, "#96C5F7", "black", "#bbd8fa", 1, 1, 7, 10],
                          [self.quiztype_area_frame, ("Arial", "20", "bold"), self.quiz_type, 3, 0, "Mixed", 12, 1, "#97F79C", "black", "#7cc580", 1, 2, 7, 10]]
        quiz_type_ref_list = []

        # Indicator being set to 0 is expected as without being on zero it adds an unwanted dot for selection.
        for item in quiz_type_list: # Creates radio buttons for quiz types [Frame | Font | Variable | Value | Indicator | text | Width | Height | Bg | Fg | Selectcolor | Row | Column | Pad X | Pad Y ]
            make_quiz_type_buttons = Radiobutton(item[0], font=item[1], variable=item[2], value=item[3], indicator=0, text=item[5], width=item[6], height=item[7], bg=item[8], fg=item[9], selectcolor=item[10])
            make_quiz_type_buttons.grid(row=item[11], column=item[12], padx=item[13], pady=item[14])
            quiz_type_ref_list.append(make_quiz_type_buttons) # Adds Radio buttons to list

        # Gets number of rounds user wants to play
        self.num_rounds_entry = Entry(self.entry_area_frame, font=("Arial", "20", "bold"),
                                      width=21)

        self.num_rounds_entry.grid(row=2, column=0, padx=10, pady=10)

        # Create play button
        self.play_button = Button(self.entry_area_frame, font=("Arial", "20", "bold"),
                                  fg="#FFFFFF", bg="#0B6E4F", text="Play", width=19,
                                  command=self.check_rounds_quiz)
        self.play_button.grid(row=2, column=1)

        recolour_list = [self.start_frame, self.quiztype_area_frame, self.entry_area_frame, self.choose_label]

        for item in recolour_list:
            item.config(bg="#ffe6cc")

    def check_rounds_quiz(self):
        """
        Checks users have entered 1 or more rounds and the quiz type
        """

        has_errors = False

        # Retrieves number of rounds to be played
        rounds_wanted = self.num_rounds_entry.get()
        quiz_type = self.quiz_type.get()

        # Reset label and entry box (for when users come back to home screen)
        self.choose_label.config(fg="#009900", font=("Arial", "16", "bold"))
        self.num_rounds_entry.config(bg="#FFFFFF")

        # Strings for the 2 error types, round_error: Quiz Type selected, invalid rounds, quiz_error: No Quiz Type selected.
        rounds_error = "Oops - Please choose a whole number more then zero, and less than 50"
        quiz_error = "Oops - Please choose a quiz type"

        # Checks that quiz type has been selected
        quiz_type = int(quiz_type)

        try: # Checks if rounds wanted is valid
            rounds_wanted = int(rounds_wanted)
            if 1 <= rounds_wanted <= 50: # Starts Game if rounds wanted is valid
                # Stats Quiz with Quiz Type
                Play(rounds_wanted, quiz_type)
                root.withdraw()

            else: # Sends error if invalid rounds
                has_errors = True

        except ValueError: # Sends error if ValueError
            has_errors = True

        # Display the rounds error if necessary
        if has_errors: # Edits Label with rounds_error string
            self.choose_label.config(text=rounds_error, fg="#990000",
                                     font=("Arial", "10", "bold"))
            self.num_rounds_entry.config(bg="#F4CCCC")
            self.num_rounds_entry.delete(0, END)

        else: # Edits Label with quiz_error
            self.choose_label.config(text=quiz_error, fg="#990000",
                                     font=("Arial", "10", "bold"))
            self.num_rounds_entry.config(bg="#F4CCCC")
            self.num_rounds_entry.delete(0, END)



class Play:
    def __init__(self, how_many, quiz_type):

        # Create lists and set info
        self.round_god = ""
        self.stats_state = None # stat of the stats tab
        self.original_quiz_type = quiz_type # original quiz type to make sure questions type stay randomized in mixed quiz
        self.quiz_type = quiz_type # current round quiz type for greek/roman and gods description questions type
        self.correct_answer = StringVar() # Makes the self.correct_answer to a string variable

        # Makes Rounds Played, Wanted and Won to integers
        self.rounds_played = IntVar()
        self.rounds_wanted = IntVar()
        self.rounds_correct = IntVar()

        # Sets Rounds Played to 0, Wanted to user's input, Won to 0
        self.rounds_played.set(0)
        self.rounds_wanted.set(how_many)
        self.rounds_correct.set(0)

        # Lists for round results, Gods origins, Gods descriptions, Gods Names for labels/buttons, Each Round Number for Stats
        self.all_selected_answer_list = []
        self.all_origin_list = []
        self.all_description_list = []
        self.round_gods_list = []
        self.current_round = []

        self.play_box = Toplevel() # Creates Quiz GUI
        self.quiz_frame = Frame(self.play_box) # Creates Frame in GUI
        self.quiz_frame.grid(padx=10, pady=10)

        self.play_box.protocol('WM_DELETE_WINDOW', root.destroy) # Closes all other open tabs if main tab is closed

        body_font = ("Arial", 12)

        # Creates Labels for quiz questions and result [Frame | Text | Font | Bg | Wrap length | row | pady | padx ]
        self.main_labels_list = [[self.quiz_frame, "Round # of #", ("Arial", 16, "bold"), "#FFFFFF", 300, 0, 10, 0],
                                  [self.quiz_frame, "", body_font, "#FFF2CC", 300, 1, 10, 10],
                                  [self.quiz_frame, "", body_font, "#D5E8D4", 300, 2, 10, 0 ]]
        self.main_labels_ref_list = []

        for item in self.main_labels_list: # Makes labels from list information
            make_main_labels = Label(item[0], text=item[1], font=item[2], bg=item[3], wraplength=item[4])
            make_main_labels.grid(row=item[5], pady=item[6], padx=item[7])
            self.main_labels_ref_list.append(make_main_labels)

        # Separates list items to config
        self.heading_label = self.main_labels_ref_list[0]
        self.question_label = self.main_labels_ref_list[1]
        self.results_label = self.main_labels_ref_list[2]


        # Button frame
        self.answer_frame = Frame(self.quiz_frame)
        self.answer_frame.grid(row=4)

        # list of items for making greek and roman quiz type buttons [frame/master | font | text | width | bg colour | fg colour | command | row | column]
        self.greek_roman_button_list = [[self.answer_frame, ("Arial", 12, "bold"), "Greek", 20, "#ff9999", "black", partial(self.rounds_results, "Greek", 1), 0, 0],
                                        [self.answer_frame, ("Arial", 12, "bold"), "Roman", 20, "#96c5f7", "black", partial(self.rounds_results, "Roman", 1), 0 ,1]]
        self.greek_roman_button_ref_list = []

        for item in self.greek_roman_button_list: # creates buttons and adds them to ref list
            make_greek_roman_button = Button(item[0], font=item[1], text=item[2], width=item[3], bg=item[4], fg=item[5], command=item[6])
            make_greek_roman_button.grid(row=item[7], column=item[8], padx=5, pady=5)
            self.greek_roman_button_ref_list.append(make_greek_roman_button)

        # sets buttons from ref list for config
        self.greek_button = self.greek_roman_button_ref_list[0]
        self.roman_button = self.greek_roman_button_ref_list[1]

        # Gods name (quiz type 2 buttons)
        self.gods_name_frame = Frame(self.answer_frame)
        self.gods_button_ref = []
        button_colors = ["#ff9999", "#96c5f7", "#a18eb3", "#9ac7bf"]
        for i in range(4): # sets colours for buttons and sets them to the buttons in a 2x2 grid
            gods_button = Button(self.gods_name_frame, font=("Arial", 12, "bold"),
                                 text="Gods Name", width=20,
                                 bg=button_colors[i], fg="black", disabledforeground="#404040",
                                 command=partial(self.rounds_results, i, 2))
            gods_button.grid(row=i // 2, column=i % 2, padx=5, pady=5)
            self.gods_button_ref.append(gods_button)

        # info, stats and next Buttons
        self.info_stats_frame = Frame(self.quiz_frame)
        self.info_stats_frame.grid(row=6)

        # List for buttons (frame | text | bg | command | width | row | column )
        control_button_list = [
            [self.info_stats_frame, "Next Round", "#00D31C", self.next_quiz_type, 10, 0, 2],
            [self.info_stats_frame, "Info", "#FF8000", self.to_info, 10, 0, 0],
            [self.info_stats_frame, "Stats", "#A1FFFC", self.to_stats, 10, 0, 1],
        ]

        # Create buttons and add to list
        control_ref_list = [] # List of buttons
        for item in control_button_list:
            make_control_button = Button(item[0], text=item[1], bg=item[2],
                                         command=item[3], font=("Arial", "16", "bold"), disabledforeground="#404040",
                                         fg="black", width=item[4])
            make_control_button.grid(row=item[5], column=item[6], padx=5, pady=5)

            control_ref_list.append(make_control_button)

        # Sets Next, Stats and End button from list so that they can be configured.
        self.next_button = control_ref_list[0]
        self.info_button = control_ref_list[1]
        self.stats_button = control_ref_list[2]

        self.end_quiz_button = Button(self.quiz_frame, text="End", bg="#990000",font=("Arial", "16", "bold"), fg="white",
                                      command=self.close_play, width=33) # Ends quiz when pressed
        self.end_quiz_button.grid(row=7, padx=5, pady=5)

        self.stats_button.config(state=DISABLED)

        self.next_quiz_type()

        recolour_list = [self.info_stats_frame, self.gods_name_frame, self.quiz_frame, self.answer_frame, self.play_box, self.heading_label, self.results_label]

        for item in recolour_list: # sets background colour for items in recolour list
            item.config(bg="#ffe6cc")

    def next_quiz_type(self):
        # Checks if quiz type is mixed
        if self.original_quiz_type == 3:
            self.quiz_type = random.choice([1, 2])
        self.new_round(self.quiz_type) # Starts random quiz type question

    def new_round(self, current_quiz_type):
        
        self.stats_button.config(state=DISABLED) # Disable stats button
        self.stats_state = None
        rounds_played = self.rounds_played.get() + 1 # Increases rounds played by 1
        self.rounds_played.set(rounds_played)
        rounds_wanted = self.rounds_wanted.get() # gets rounds wanted
        button_colors = ["#ff9999", "#96c5f7", "#a18eb3", "#9ac7bf"] # button colours for buttons in quiz types

        self.heading_label.config(text=f"Round {rounds_played} of {rounds_wanted}")
        self.results_label.config(text=f"{'=' * 7}", bg="#ffe6cc") 

        if current_quiz_type == 1:
            # Gets god's name and answer
            self.round_god, round_god_origin = get_round_gods_desc(1)
            self.correct_answer = round_god_origin

            # Edits label
            self.question_label.config(text=f"Is {self.round_god} a Greek or Roman god?", font=("Arial", 14, "bold"))


            for item in self.greek_roman_button_ref_list:
                item.config(state=NORMAL) # Makes buttons interactable

            self.greek_button.config(bg="#ff9999") # Sets buttons colours 
            self.roman_button.config(bg="#96c5f7")
            self.greek_button.grid(row=0, column=0, padx=5, pady=5) # Sets buttons in grid area
            self.roman_button.grid(row=0, column=1, padx=5, pady=5)
            self.gods_name_frame.grid_forget() # Removes gods names buttons if mixed quiz

        elif current_quiz_type == 2:
            # Gets gods description and answer options
            self.round_gods_list, description = get_round_gods_desc(2)
            self.correct_answer = description

            # Edits labels
            self.question_label.config(text=f"Who is the God of {description}?", font=("Arial", 14, "bold"))

            for count, item in enumerate(self.gods_button_ref): # Sets buttons text and colours 
                item.config(text=self.round_gods_list[count][2], bg=button_colors[count], state=NORMAL)

            self.greek_button.grid_forget() # Removes greek/roman buttons if mixed quiz
            self.roman_button.grid_forget()
            self.gods_name_frame.grid(row=0, column=0, columnspan=2)

        self.next_button.config(state=DISABLED)

    def rounds_results(self, user_choice, quiz_type):
        rounds_correct = self.rounds_correct.get() # Gets rounds correct
        rounds_played = self.rounds_played.get() # Gets total rounds
        self.current_round.append(rounds_played)

        if quiz_type == 1:
            selected_answer = user_choice
            correct_answer = self.correct_answer
            round_god = self.round_god
            self.all_origin_list.append(correct_answer)

            if selected_answer == correct_answer:
                result_text = f"{user_choice} was correct!!"
                result_bg = "#82B366"  # green
                self.all_selected_answer_list.append(result_text)

                rounds_correct += 1
                self.rounds_correct.set(rounds_correct)
            else:
                result_text = f"Oops {user_choice} was the incorrect origin for {round_god}. The correct answer was {correct_answer}"
                result_bg = "#F8CECC"  # red
                self.all_selected_answer_list.append(result_text)

            self.results_label.config(text=result_text, bg=result_bg)

            # Update button colors
            if user_choice == "Greek":
                self.roman_button.config(bg="#D9D9D9")
                if user_choice != correct_answer:
                    self.greek_button.config(bg="#FF6961")
                else:
                    self.greek_button.config(bg="#82B366")
            else:
                self.greek_button.config(bg="#D9D9D9")
                if user_choice != correct_answer:
                    self.roman_button.config(bg="#FF6961")
                else:
                    self.roman_button.config(bg="#82B366")




        elif quiz_type == 2:
            selected_answer = self.round_gods_list[user_choice][3]
            gods_name = self.gods_button_ref[user_choice].cget('text')
            correct_answer = self.correct_answer
            self.all_description_list.append(correct_answer)

            if selected_answer == correct_answer:
                result_text = f"{gods_name} was correct!!"
                result_bg = "#82B366"  # green
                self.all_selected_answer_list.append(result_text)

                rounds_correct += 1
                self.rounds_correct.set(rounds_correct)
            else:
                correct_god_name = ""
                for god_data in self.round_gods_list:
                    if god_data[3] == correct_answer:
                        correct_god_name = god_data[2]
                result_text = f"Oops {gods_name} was incorrect. The correct god was {correct_god_name}"
                result_bg = "#F8CECC"  # red
                self.all_selected_answer_list.append(result_text)

            self.results_label.config(text=result_text, bg=result_bg)

            for button, item in enumerate(self.gods_button_ref):
                item.config(state=DISABLED)  # disable all buttons

                # Only change color for the selected button
                if button == user_choice:
                    if self.round_gods_list[user_choice][3] != correct_answer:
                        item.config(bg="#FF6961")  # red
                    else:
                        item.config(bg="#82B366") # green
                else:
                    item.config(bg="#D9D9D9") # grey

        # Enable next/stats buttons
        self.next_button.config(state=NORMAL)
        self.stats_button.config(state=NORMAL)
        self.stats_state = "on"

        # Check for quiz end
        if rounds_played == self.rounds_wanted.get():
            self.next_button.config(state=DISABLED, text="Quiz Over")
            self.end_quiz_button.config(text="Play Again?", bg="#006600")

    def to_info(self):
        """
        Displays info for playing quiz
        """
        rounds_played = self.rounds_played.get()
        DisplayInfo(self, rounds_played)

    def close_play(self):
        """
        Reshow root and end current
        quiz / allow new quiz to start
        """
        root.deiconify()
        self.play_box.destroy()

    def to_stats(self):
        """
        Displays stats for playing quiz
        """
        rounds_correct = self.rounds_correct.get()
        rounds_wanted = self.rounds_wanted.get()
        stats_bundle = [rounds_correct, self.all_selected_answer_list, self.current_round, rounds_wanted]
        Stats(self, stats_bundle)


class DisplayInfo:
    """
    Displays info dialogue box
    """

    def __init__(self, partner, rounds_played):

        self.rounds_played = rounds_played

        # Setup info box
        background = "#ffe6cc"
        self.info_box = Toplevel()

        # Disable info box
        partner.stats_button.config(state=DISABLED)
        partner.info_button.config(state=DISABLED)
        partner.end_quiz_button.config(state=DISABLED)
        partner.next_button.config(state=DISABLED)

        # Disable selection buttons
        for item in partner.greek_roman_button_ref_list:
            item.config(state=DISABLED)

        for item in partner.gods_button_ref:
            item.config(state=DISABLED)

        # If users press cross at top, closes info and
        # 'releases' info button
        self.info_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_info, partner))

        self.info_frame = Frame(self.info_box, width=300,
                                height=200)
        self.info_frame.grid() # Create frame for info

        self.info_heading_label = Label(self.info_frame,
                                        text="Info",
                                        font=("Arial", "14", "bold"))
        self.info_heading_label.grid(row=0) # Adds heading label to grid

        info_text = ("Gods Quiz\n\n"
                     "Greek/Roman:\n"
                     "In this quiz you will be given a god's name, \n"
                     "you have the option to select whether the god is of greek or roman origin.\n\n"
                     "God's Name\n"
                     "In this quiz you will be shown the description for a god\n"
                     "you have 4 options to select from, 1 of them is the correct god.\n\n"
                     "After each question you can press the stats button to look at\n"
                     "how many questions you have correct and see the history of which questions you got wrong and right, along with what the correct answer was.")

        self.info_text_label = Label(self.info_frame,
                                     text=info_text,
                                     wraplength=350, font=("Arial", "12"), justify="left")
        self.info_text_label.grid(row=1, padx=10) # Adds info next to grid

        self.dismiss_button = Button(self.info_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_info, partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10) # Adds close/dismiss button to grid

        recolour_list = [self.info_frame, self.info_heading_label,
                         self.info_text_label]

        for item in recolour_list:
            item.config(bg=background) # Changes background color of items in list

    def close_info(self, partner):
        """
        Closes info dialogue box (and enables info button
        """

        # Put help button back to normal
        partner.info_button.config(state=NORMAL)
        partner.end_quiz_button.config(state=NORMAL)

        # Sets option buttons in greek/roman and gods quiz to normal
        for item in partner.greek_roman_button_ref_list:
            item.config(state=NORMAL)

        for item in partner.gods_button_ref:
            item.config(state=NORMAL)

        if partner.stats_state == "on": # Checks if round has ended enabling stats button else leaves it disabled
            partner.stats_button.config(state=NORMAL)
            for item in partner.greek_roman_button_ref_list:
                item.config(state=DISABLED)

            for item in partner.gods_button_ref:
                item.config(state=DISABLED)

        # Put info button back to normal
        if self.rounds_played >=1:
            partner.info_button.config(state=NORMAL)
        self.info_box.destroy()



class Stats:

    def __init__(self, partner, all_stats_info):

        background = "#ffe6cc"

        # Disable buttons to prevent programs crashing
        partner.next_button.config(state=DISABLED)
        partner.info_button.config(state=DISABLED)
        partner.end_quiz_button.config(state=DISABLED)
        partner.stats_button.config(state=DISABLED)

        for item in partner.greek_roman_button_ref_list:
            item.config(state=DISABLED)

        for item in partner.gods_button_ref:
            item.config(state=DISABLED)

        # Unpack all_stats_info
        rounds_correct = all_stats_info[0]
        user_selected_answers = all_stats_info[1]
        round_number = all_stats_info[2]
        self.rounds_wanted = all_stats_info[3]

        # Create the stats window
        self.stats_box = Toplevel()

        # If the user closes the stats window, restore the stats button
        self.stats_box.protocol('WM_DELETE_WINDOW',
                                partial(self.close_stats, partner))

        # Create frame for the stats window
        self.stats_frame = Frame(self.stats_box, width=450)
        self.stats_frame.grid()

        # Calculate success rate
        self.rounds_played = len(user_selected_answers)
        success_rate = rounds_correct / self.rounds_played * 100 if self.rounds_played > 0 else 0

        # Stats strings
        success_string = f"Success Rate: {rounds_correct} / {self.rounds_played} ({success_rate:.0f}%)"

        if rounds_correct == 0:
            comment_string = "Oops - You've got every round incorrect!"
            comment_colour = "#ff0000"
            comment_bg_colour = "#ffcdcd"
        else:
            comment_string = ""
            comment_colour = "#F0F0F0"
            comment_bg_colour = "#ffe6cc"

        heading_font = ("Arial", "16", "bold")
        normal_font = ("Arial", "14")
        comment_font = ("Arial", "15", "bold")

        # List of all stats strings for the labels
        all_stats_strings = [
            ["Statistics", heading_font, ""],
            [success_string, normal_font, "W"],
            [comment_string, comment_font, "W"],
            ["\nRound Stats", heading_font, ""],
        ]

        # Create labels for the stats window
        stats_label_ref_list = []
        for count, item in enumerate(all_stats_strings):
            self.stats_label = Label(self.stats_frame, text=item[0], font=item[1],
                                     anchor="nw", justify="left",
                                     padx=30, pady=5, bg="#ffe6cc")
            self.stats_label.grid(row=count, sticky=item[2], padx=10)
            stats_label_ref_list.append(self.stats_label)

        # Background color for comment label
        stats_comment_label = stats_label_ref_list[2]
        stats_comment_label.config(fg=comment_colour, bg=comment_bg_colour)

        # Create canvas
        self.results_frame = Frame(self.stats_frame)
        self.results_frame.grid()
        canvas = Canvas(self.results_frame, width=450, height=300)
        canvas.grid(row=4, column=0)

        # Function for scrolling up/down the canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        # Create inner frame inside canvas
        results_frame = Frame(canvas)
        canvas.create_window((0, 0), window=results_frame, anchor='nw')


        # Add result labels
        for i in range(self.rounds_played):
            text = f"Round: {round_number[i]} | Result: {user_selected_answers[i]}"

            if "oops" in user_selected_answers[i].lower():  # Sets bg for label to red
                label = Label(results_frame, text=text, font=("arial", 12, "bold"),
                              justify="left", wraplength=400, padx=25, fg="red")
            else: # Sets bg for label to green
                label = Label(results_frame, text=text, font=("arial", 12, "bold"),
                              justify="left", wraplength=400, padx=25, fg="green")

            label.pack(anchor="w")

        # Update layout so bbox gets more recent dimensions
        results_frame.update_idletasks()

        # Set scroll region using bbox
        bbox = canvas.bbox("all")
        if bbox:
            canvas.config(scrollregion=bbox)

            # Get content height, if greater than canvas height add scrollbar
            if bbox[3] - bbox[1] > 300:
                canvas.bind_all("<MouseWheel>", _on_mousewheel)
                scrollbar = Scrollbar(self.results_frame, orient=VERTICAL, command=canvas.yview)
                scrollbar.grid(row=4, column=1, sticky=NS)
                canvas.config(yscrollcommand=scrollbar.set)

        # Dismiss button
        self.dismiss_button = Button(self.stats_frame,
                                     font=("Arial", "16", "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF", width=20,
                                     command=partial(self.close_stats, partner))
        self.dismiss_button.grid(row=8, padx=10, pady=10)

        recolour_list = [self.results_frame ,self.stats_label, self.stats_box, self.stats_frame]

        for item in recolour_list: # Recolours backgrounds for items in list
            item.config(bg=background)

    def close_stats(self, partner):
        """
        Closes stats dialogue box and enables the stats button again
        """
        # Enable buttons back to normal
        partner.info_button.config(state=NORMAL)
        partner.end_quiz_button.config(state=NORMAL)
        partner.stats_button.config(state=NORMAL)
        self.stats_box.destroy()

        if self.rounds_played != self.rounds_wanted:
            partner.next_button.config(state=NORMAL)

# Runs Program
if __name__ == "__main__":
    root = Tk()
    root.title("God Quiz")
    StartQuiz()
    root.mainloop()
