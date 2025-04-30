import csv
import random
from tkinter import *
from functools import partial  # To prevent unwanted windows


# Helper functions go here

def get_gods_name_desc():
    """Retrieves gods from CSV file."""
    with open("gods.csv", "r", newline="", encoding="utf-8") as file:
        all_gods = list(csv.reader(file, delimiter=","))

    # Remove header row
    if all_gods:
        all_gods.pop(0)

    return all_gods


def get_round_gods_desc(game_type):
    """Choose gods depending on the game type."""
    all_gods_list = get_gods_name_desc()

    if game_type == 1:
        round_gods = []
        round_god_description = set()

        while len(round_gods) < 4:
            potential_god = random.choice(all_gods_list)
            if potential_god[3] not in round_god_description:
                round_gods.append(potential_god)
                round_god_description.add(potential_god[3])

        god_description = random.choice(list(round_god_description))
        return round_gods, god_description

    elif game_type == 2:
        potential_god = random.choice(all_gods_list)
        return potential_god[2], potential_god[0]


# Class starts here
class StartGame:

    def __init__(self):

        """
        Gets number of rounds from user
        """

        self.start_frame = Frame(padx=60, pady=30)
        self.start_frame.grid()

        # Strings for labels
        intro_string = "blah blah blah fill this in later"

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
                               wraplength=350, justify="left", pady=10, padx=20)
            make_label.grid(row=count)

            start_label_ref.append(make_label)

        # Extract choice label so that it can be changed into an
        # error message if necessary.
        self.choose_label = start_label_ref[2]

        # Frame so that entry box and button can be in the same row.

        self.entry_area_frame = Frame(self.start_frame)
        self.entry_area_frame.grid(row=3)

        # Value used to find which game is selected
        self.game_type = StringVar()
        self.game_type.set("0")

        # Radio Buttons | Allows user to select whether they play the Greek / Roman Quiz or Gods Name Quiz
        self.greek_roman_quiz_select = Radiobutton(self.entry_area_frame, font=("Arial", "20", "bold"),
                                                   variable=self.game_type,
                                                   value=1, indicator=0, text="Greek / Roman", width=15, height=1,
                                                   bg="#FF9999", fg="#FFFFFF", selectcolor="#f5a3a3")

        self.greek_roman_quiz_select.grid(row=1, column=0, padx=10, pady=10)

        self.god_name_quiz_select = Radiobutton(self.entry_area_frame, font=("Arial", "20", "bold"),
                                                variable=self.game_type,
                                                value=2, indicator=0, text="God Name", width=15,
                                                bg="#96C5F7", fg="#FFFFFF", selectcolor="#bbd8fa")

        self.god_name_quiz_select.grid(row=1, column=1, padx=10, pady=10)

        # Gets number of rounds user wants to play
        self.num_rounds_entry = Entry(self.entry_area_frame, font=("Arial", "20", "bold"),
                                      width=16)

        self.num_rounds_entry.grid(row=2, column=0, padx=10, pady=10)

        # Create play button
        self.play_button = Button(self.entry_area_frame, font=("Arial", "20", "bold"),
                                  fg="#FFFFFF", bg="#0B6E4F", text="Play", width=14, height=1,
                                  command=self.check_rounds_game)
        self.play_button.grid(row=2, column=1)

    def check_rounds_game(self):
        """
        Checks users have entered 1 or more rounds and the game type
        """

        # Retrieves number of rounds to be played
        rounds_wanted = self.num_rounds_entry.get()
        game_type = self.game_type.get()

        # Reset label and entry box (for when users come back to home screen)
        self.choose_label.config(fg="#009900", font=("Arial", "16", "bold"))
        self.num_rounds_entry.config(bg="#FFFFFF")

        rounds_error = "Oops - Please choose a whole number more then zero"
        has_errors = "no"
        game_error = "Oops - Please choose a game type"

        # Checks that game type has been selected
        game_type = int(game_type)
        if game_type == 1 or game_type == 2:
            # Checks that rounds to be player is a number above zero
            try:
                rounds_wanted = int(rounds_wanted)
                if rounds_wanted > 0:
                    # Invoke Player Class (and take across number of rounds)
                    Play(rounds_wanted, game_type)
                    # Hide root window (ie: hide rounds choice window).
                    root.withdraw()

                else:
                    has_errors = "yes"


            except ValueError:
                has_errors = "yes"
            # Display the rounds error if necessary
            if has_errors == "yes":
                self.choose_label.config(text=rounds_error, fg="#990000",
                                         font=("Arial", "10", "bold"))
                self.num_rounds_entry.config(bg="#F4CCCC")
                self.num_rounds_entry.delete(0, END)
        else:
            self.choose_label.config(text=game_error, fg="#990000",
                                     font=("Arial", "10", "bold"))
            self.num_rounds_entry.config(bg="#F4CCCC")
            self.num_rounds_entry.delete(0, END)


class Play:
    """Interface for playing the God Quest Game"""

    def __init__(self, how_many, game_type):
        get_round_gods_desc(game_type)

        if game_type == 1:
            self.target_description = StringVar

            # Rounds played | start with zero
            self.rounds_played = IntVar()
            self.rounds_played.set(0)

            self.rounds_wanted = IntVar()
            self.rounds_wanted.set(how_many)

            # Gods lists and score list
            self.round_gods_list = []
            self.all_score_list = []
            self.all_description_list = []

            self.play_box = Toplevel()

            self.game_frame = Frame(self.play_box)
            self.game_frame.grid(padx=10, pady=10)

            # Body font for most labels...
            body_font = ("Arial", "12")

            # Lists for label details (text | font | background | row)
            play_labels_list = [
                ["Round # of #", ("Arial", "16", "bold"), None, 0],
                ["Who is the God of: ", body_font, "#FFF2CC", 1],
                ["Choose a God below. Good luck!", body_font, "#D5E8D4", 2],
                ["You choose, result", body_font, "#D5E8D4", 3]
            ]

            play_labels_ref = []
            for item in play_labels_list:
                self.make_label = Label(self.game_frame, text=item[0], font=item[1],
                                        bg=item[2], wraplength=300, justify="left")
                self.make_label.grid(row=item[3], pady=10, padx=10)

                play_labels_ref.append(self.make_label)

            # Retrieve labels so they can be configured later
            self.heading_label = play_labels_ref[0]
            self.target_label = play_labels_ref[1]
            self.results_label = play_labels_ref[3]

            # Set up colour buttons...
            self.gods_name_frame = Frame(self.game_frame)
            self.gods_name_frame.grid(row=4)

            self.gods_button_ref = []

            # Colours for buttons in grid
            button_colors = ["red", "blue", "green", "yellow"]

            # Create four buttons in a 2 x 2 grid
            for item in range(4):
                self.gods_button = Button(self.gods_name_frame, font=body_font,
                                            text="Gods Name", width=23,
                                            bg=button_colors[item],
                                            fg="white",
                                            command=partial(self.rounds_results, item, game_type))
                self.gods_button.grid(row=item // 2,
                                        column=item % 2,
                                        padx=5, pady=5)

                self.gods_button_ref.append(self.gods_button)


            # Frame to hold hints and stats buttons
            self.hints_stats_frame = Frame(self.game_frame)
            self.hints_stats_frame.grid(row=6)

            # List for buttons (frame | text | bg | command | width | row | column )
            control_button_list = [
                [self.hints_stats_frame, "Next Round", "#0057D8", lambda: self.new_round(1), 10, 0, 2],
                [self.hints_stats_frame, "Hints", "#FF8000", "", 10, 0, 0],
                [self.hints_stats_frame, "Stats", "#333333", "", 10, 0, 1],
                [self.game_frame, "End", "#990000", self.close_play, 33, 7, None]
            ]

            # Create buttons and add to list
            control_ref_list = []
            for item in control_button_list:
                make_control_button = Button(item[0], text=item[1], bg=item[2],
                                             command=item[3], font=("Arial", "16", "bold"),
                                             fg="#FFFFFF", width=item[4])
                make_control_button.grid(row=item[5], column=item[6], padx=5, pady=5)

                control_ref_list.append(make_control_button)

            # Retrieve next, stats and end button so that they can be configured.
            self.next_button = control_ref_list[0]
            self.stats_button = control_ref_list[2]
            self.end_game_button = control_ref_list[3]

            self.new_round(1)

        if game_type == 2:
            self.target_description = StringVar

            # Rounds played | start with zero
            self.rounds_played = IntVar()
            self.rounds_played.set(0)

            self.rounds_wanted = IntVar()
            self.rounds_wanted.set(how_many)

            # Gods lists and score list
            self.round_god, round_god_origin = get_round_gods_desc(2)
            self.all_score_list = []
            self.all_origin_list = []

            self.play_box = Toplevel()

            self.game_frame = Frame(self.play_box)
            self.game_frame.grid(padx=10, pady=10)

            # Body font for most labels...
            body_font = ("Arial", "12")

            # Lists for label details (text | font | background | row)
            play_labels_list = [
                ["Round # of #", ("Arial", "16", "bold"), None, 0],
                ["Is # a Greek or Roman god? ", body_font, "#FFF2CC", 1],
                ["Choose below. Good luck!", body_font, "#D5E8D4", 2],
                ["You choose, result", body_font, "#D5E8D4", 3]
            ]

            play_labels_ref = []
            for item in play_labels_list:
                self.make_label = Label(self.game_frame, text=item[0], font=item[1],
                                        bg=item[2], wraplength=300, justify="left")
                self.make_label.grid(row=item[3], pady=10, padx=10)

                play_labels_ref.append(self.make_label)

            # Retrieve labels so they can be configured later
            self.heading_label = play_labels_ref[0]
            self.target_label = play_labels_ref[1]
            self.results_label = play_labels_ref[3]

            # Set up colour buttons...
            self.greek_roman_name_frame = Frame(self.game_frame)
            self.greek_roman_name_frame.grid(row=4)

            self.greek_roman_button_ref = []

            # Greek and Roman Option frames
            self.greek_button = Button(self.greek_roman_name_frame, font=body_font,
                                        text="Greek", width=23,
                                        bg="#FFFFFF",
                                        command=partial(self.rounds_results, "Greek", game_type))
            self.greek_button.grid(row=0,column=0, padx=5, pady=5)

            self.greek_roman_button_ref.append(self.greek_button)

            self.roman_button = Button(self.greek_roman_name_frame, font=body_font,
                                       text="Roman", width=23,
                                       bg="#FFFFFF",
                                       command=partial(self.rounds_results, "Roman", game_type))
            self.roman_button.grid(row=0, column=1, padx=5, pady=5)
            self.greek_roman_button_ref.append(self.roman_button)

            # Frame to hold hints and stats buttons
            self.hints_stats_frame = Frame(self.game_frame)
            self.hints_stats_frame.grid(row=6)

            # List for buttons (frame | text | bg | command | width | row | column )
            control_button_list = [
                [self.hints_stats_frame, "Next Round", "#0057D8", lambda: self.new_round(2), 10, 0, 2],
                [self.hints_stats_frame, "Hints", "#FF8000", "", 10, 0, 0],
                [self.hints_stats_frame, "Stats", "#333333", "", 10, 0, 1],
                [self.game_frame, "End", "#990000", self.close_play, 33, 7, None]
            ]

            # Create buttons and add to list
            control_ref_list = []
            for item in control_button_list:
                make_control_button = Button(item[0], text=item[1], bg=item[2],
                                             command=item[3], font=("Arial", "16", "bold"),
                                             fg="#FFFFFF", width=item[4])
                make_control_button.grid(row=item[5], column=item[6], padx=5, pady=5)

                control_ref_list.append(make_control_button)

            # Retrieve next, stats and end button so that they can be configured.
            self.next_button = control_ref_list[0]
            self.stats_button = control_ref_list[2]
            self.end_game_button = control_ref_list[3]

            self.new_round(2)

    def new_round(self, game_type):
        # Retrieve number of rounds played, add one to it and configure heading
        rounds_played = self.rounds_played.get()
        rounds_played += 1
        self.rounds_played.set(rounds_played)
        rounds_wanted = self.rounds_wanted.get()

        if game_type == 1:
            # Get round colours and median score...
            self.round_gods_list, description = get_round_gods_desc(1)

            self.target_description = description

            self.heading_label.config(text=f"Round {rounds_played} of {rounds_wanted}")
            self.target_label.config(text=f"Who is the God of {description}?", font="Arial" "14" "bold")
            self.results_label.config(text=f"{'=' * 7}", bg="#F0F0F0")

            for count, item in enumerate(self.gods_button_ref):
                item.config(text=self.round_gods_list[count][2], state=NORMAL)

        if game_type == 2:
            # Get round colours and median score...
            self.round_god, round_god_origin = get_round_gods_desc(2)

            self.target_description = round_god_origin

            self.heading_label.config(text=f"Round {rounds_played} of {rounds_wanted}")
            self.target_label.config(text=f"Is {self.round_god} a Greek or Roman god?", font="Arial" "14" "bold")
            self.results_label.config(text=f"{'=' * 7}", bg="#F0F0F0")

            for count, item in enumerate(self.greek_roman_button_ref):
                item.config(state=NORMAL)

        self.next_button.config(state=DISABLED)

    def rounds_results(self, user_choice, game_type):
        if game_type == 1:
            # Get user score and colour based on button press...
            score = self.round_gods_list[user_choice][3]

            # Alternate way to get button name. Good for if buttons have been scrambled!
            gods_name = self.gods_button_ref[user_choice].cget('text')

            # Retrieve target and compare with user score to find round results
            target = self.target_description
            self.all_description_list.append(target)

            if score == target:
                result_text = f"Success!! {gods_name} was correct!!"
                result_bg = "#82B366"
                self.all_score_list.append(score)

            else:
                result_text = f"Oops {gods_name} was incorrect."
                result_bg = "#F8CECC"
                self.all_score_list.append(0)

            self.results_label.config(text=result_text, bg=result_bg)

        if game_type == 2:
            # Get user score on button press...
            score = user_choice

            # Alternate way to get button name. Good for if buttons have been scrambled!
            gods_name, round_gods_origin = get_round_gods_desc(2)

            # Retrieve target and compare with user score to find round results
            target = self.target_description
            self.all_origin_list.append(target)

            if score == target:
                result_text = f"Success!! {user_choice} was correct!!"
                result_bg = "#82B366"
                self.all_score_list.append(score)

            else:
                result_text = f"Oops {user_choice} was incorrect."
                result_bg = "#F8CECC"
                self.all_score_list.append(0)

            self.results_label.config(text=result_text, bg=result_bg)

        # Enable stats & next buttons, disable color buttons
        self.next_button.config(state=NORMAL)
        self.stats_button.config(state=NORMAL)

        # Check to see if game is over
        rounds_played = self.rounds_played.get()
        rounds_wanted = self.rounds_wanted.get()

        if rounds_played == rounds_wanted:
            self.next_button.config(state=DISABLED, text="Game Over")
            self.end_game_button.config(text="Play Again", bg="#006600")

        for item in self.greek_roman_button_ref:
            item.config(state=DISABLED)



    def close_play(self):
        print("")

if __name__ == "__main__":
    root = Tk()
    root.title("God Quest")
    StartGame()
    root.mainloop()
