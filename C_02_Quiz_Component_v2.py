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


def get_round_gods_desc():
    """Choose four gods ensuring unique descriptions."""
    all_gods_list = get_gods_name_desc()

    round_gods = []
    round_god_description = []

    while len(round_gods) < 4:
        potential_gods = random.choice(all_gods_list)

        # Ensure unique description selection
        if potential_gods[3] not in round_god_description:
            round_gods.append(potential_gods)
            round_god_description.append(potential_gods[3])

    god_description = random.choice(round_god_description)
    return round_gods, god_description



# Class starts here
class StartGame:

    def __init__(self):

        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # Create play button
        self.play_button = Button(
            self.start_frame,
            font=("Arial", 16, "bold"), fg="#FFFFFF", bg="#0057D8",
            text="Play", width=10, command=self.check_rounds
        )
        self.play_button.grid(row=0, column=1)

    def check_rounds(self):
        """Starts the game with predefined rounds"""
        Play(5)
        root.withdraw()


class Play:
    """Interface for playing the God Quest Game"""

    def __init__(self, how_many):
        get_round_gods_desc()

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
                                        command=partial(self.rounds_results, item))
            self.gods_button.grid(row=item // 2,
                                    column=item % 2,
                                    padx=5, pady=5)

            self.gods_button_ref.append(self.gods_button)


        # Frame to hold hints and stats buttons
        self.hints_stats_frame = Frame(self.game_frame)
        self.hints_stats_frame.grid(row=6)

        # List for buttons (frame | text | bg | command | width | row | column )
        control_button_list = [
            [self.hints_stats_frame, "Next Round", "#0057D8", self.new_round, 10, 0, 2],
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

        self.new_round()


    def new_round(self):
        # Retrieve number of rounds played, add one to it and configure heading
        rounds_played = self.rounds_played.get()
        rounds_played += 1
        self.rounds_played.set(rounds_played)
        rounds_wanted = self.rounds_wanted.get()

        # Get round colours and median score...
        self.round_gods_list, description = get_round_gods_desc()

        self.target_description = description

        self.heading_label.config(text=f"Round {rounds_played} of {rounds_wanted}")
        self.target_label.config(text=f"Who is the God of {description}?", font="Arial" "14" "bold")
        self.results_label.config(text=f"{'=' * 7}", bg="#F0F0F0")

        for count, item in enumerate(self.gods_button_ref):
            item.config(text=self.round_gods_list[count][2], state=NORMAL)

        self.next_button.config(state=DISABLED)

    def rounds_results(self, user_choice):
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

        # Enable stats & next buttons, disable color buttons
        self.next_button.config(state=NORMAL)
        self.stats_button.config(state=NORMAL)

        # Check to see if game is over
        rounds_played = self.rounds_played.get()
        rounds_wanted = self.rounds_wanted.get()

        if rounds_played == rounds_wanted:
            self.next_button.config(state=DISABLED, text="Game Over")
            self.end_game_button.config(text="Play Again", bg="#006600")

        for item in self.gods_button_ref:
            item.config(state=DISABLED)




    def close_play(self):
        print("")
if __name__ == "__main__":
    root = Tk()
    root.title("God Quest")
    StartGame()
    root.mainloop()
