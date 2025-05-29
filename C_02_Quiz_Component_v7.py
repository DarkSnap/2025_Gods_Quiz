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


def get_round_gods_desc(quiz_type):
    """Choose gods depending on the game type."""
    all_gods_list = get_gods_name_desc()

    if quiz_type == 1:
        potential_god = random.choice(all_gods_list)
        return potential_god[2], potential_god[0]

    elif quiz_type == 2:
        round_gods = []
        round_god_description = set()

        while len(round_gods) < 4:
            potential_god = random.choice(all_gods_list)
            if potential_god[3] not in round_god_description:
                round_gods.append(potential_god)
                round_god_description.add(potential_god[3])

        god_description = random.choice(list(round_god_description))
        return round_gods, god_description

# Class starts here
class StartQuiz:

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

        self.quiztype_area_frame = Frame(self.start_frame)
        self.quiztype_area_frame.grid(row=3)

        self.entry_area_frame = Frame(self.start_frame)
        self.entry_area_frame.grid(row=4)

        # Value used to find which game is selected
        self.quiz_type = StringVar()
        self.quiz_type.set("0")

        # Radio Buttons | Allows user to select whether they play the Greek / Roman Quiz or Gods Name Quiz
        self.greek_roman_quiz_select = Radiobutton(self.quiztype_area_frame, font=("Arial", "20", "bold"),
                                                   variable=self.quiz_type,
                                                   value=1, indicator=0, text="Greek / Roman", width=11, height=1,
                                                   bg="#FF9999", fg="#FFFFFF", selectcolor="#f5a3a3")

        self.greek_roman_quiz_select.grid(row=1, column=0, padx=10, pady=10)

        self.god_name_quiz_select = Radiobutton(self.quiztype_area_frame, font=("Arial", "20", "bold"),
                                                variable=self.quiz_type,
                                                value=2, indicator=0, text="God Name", width=11,
                                                bg="#96C5F7", fg="#FFFFFF", selectcolor="#bbd8fa")

        self.god_name_quiz_select.grid(row=1, column=1, padx=10, pady=10)

        self.mixed_quiz_select = Radiobutton(self.quiztype_area_frame, font=("Arial", "20", "bold"),
                                                variable=self.quiz_type,
                                                value=3, indicator=0, text="Mixed", width=11,
                                                bg="#96C5F7", fg="#FFFFFF", selectcolor="#bbd8fa")

        self.mixed_quiz_select.grid(row=1, column=2, padx=10, pady=10)

        # Gets number of rounds user wants to play
        self.num_rounds_entry = Entry(self.entry_area_frame, font=("Arial", "20", "bold"),
                                      width=19)

        self.num_rounds_entry.grid(row=2, column=0, padx=10, pady=10)

        # Create play button
        self.play_button = Button(self.entry_area_frame, font=("Arial", "20", "bold"),
                                  fg="#FFFFFF", bg="#0B6E4F", text="Play", width=19, height=1,
                                  command=self.check_rounds_quiz)
        self.play_button.grid(row=2, column=1)

    def check_rounds_quiz(self):
        """
        Checks users have entered 1 or more rounds and the game type
        """

        # Retrieves number of rounds to be played
        rounds_wanted = self.num_rounds_entry.get()
        quiz_type = self.quiz_type.get()

        # Reset label and entry box (for when users come back to home screen)
        self.choose_label.config(fg="#009900", font=("Arial", "16", "bold"))
        self.num_rounds_entry.config(bg="#FFFFFF")

        rounds_error = "Oops - Please choose a whole number more then zero"
        has_errors = False
        quiz_error = "Oops - Please choose a game type"

        # Checks that game type has been selected
        quiz_type = int(quiz_type)
        if quiz_type == 1 or quiz_type == 2 or quiz_type == 3:
            # Checks that rounds to be player is a number above zero
            try:
                rounds_wanted = int(rounds_wanted)
                if rounds_wanted > 0:
                    # Invoke Player Class (and take across number of rounds)
                    Play(rounds_wanted, quiz_type)
                    # Hide root window
                    root.withdraw()

                else:
                    has_errors = True

            except ValueError:
                has_errors = True
            # Display the rounds error if necessary
            if has_errors:
                self.choose_label.config(text=rounds_error, fg="#990000",
                                         font=("Arial", "10", "bold"))
                self.num_rounds_entry.config(bg="#F4CCCC")
                self.num_rounds_entry.delete(0, END)
        else:
            self.choose_label.config(text=quiz_error, fg="#990000",
                                     font=("Arial", "10", "bold"))
            self.num_rounds_entry.config(bg="#F4CCCC")
            self.num_rounds_entry.delete(0, END)



class Play:
    def __init__(self, how_many, quiz_type):

        # Create lists and set info
        self.original_quiz_type = quiz_type
        self.quiz_type = quiz_type
        self.target_description = StringVar()

        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(how_many)

        self.rounds_won = IntVar()
        self.rounds_won.set(0)

        self.all_score_list = []
        self.all_origin_list = []
        self.all_description_list = []
        self.round_gods_list = []

        self.play_box = Toplevel()
        self.quiz_frame = Frame(self.play_box)
        self.quiz_frame.grid(padx=10, pady=10)

        body_font = ("Arial", 12)

        self.heading_label = Label(self.quiz_frame, text="Round # of #", font=("Arial", 16, "bold"))
        self.heading_label.grid(row=0, pady=10)

        self.target_label = Label(self.quiz_frame, text="", font=body_font, bg="#FFF2CC", wraplength=300, justify="left")
        self.target_label.grid(row=1, pady=10, padx=10)

        self.results_label = Label(self.quiz_frame, text="", font=body_font, bg="#D5E8D4", wraplength=300)
        self.results_label.grid(row=3, pady=10)

        # Button frame
        self.answer_frame = Frame(self.quiz_frame)
        self.answer_frame.grid(row=4)

        # Greek/Roman (quiz type 1 buttons)
        self.greek_roman_button_ref = []
        self.greek_button = Button(self.answer_frame, font=("Arial", 11, "bold"), text="Greek", width=23,
                                   bg="#ff9999", fg="white", command=partial(self.rounds_results, "Greek", 1))
        self.greek_roman_button_ref.append(self.greek_button)
        self.roman_button = Button(self.answer_frame, fg="white", font=("Arial", 11, "bold"), text="Roman", width=23,
                                   bg="#96c5f7", command=partial(self.rounds_results, "Roman", 1))
        self.greek_roman_button_ref.append(self.roman_button)

        self.greek_button.grid(row=0, column=0, padx=5, pady=5)
        self.roman_button.grid(row=0, column=1, padx=5, pady=5)

        # Gods name (quiz type 2 buttons)
        self.gods_name_frame = Frame(self.answer_frame)
        self.gods_button_ref = []
        button_colors = ["#ff9999", "#96c5f7", "#a18eb3", "#9ac7bf"]
        for i in range(4):
            gods_button = Button(self.gods_name_frame, font=("Arial", 12, "bold"),
                                 text="Gods Name", width=20,
                                 bg=button_colors[i], fg="white",
                                 command=partial(self.rounds_results, i, 2))
            gods_button.grid(row=i // 2, column=i % 2, padx=5, pady=5)
            self.gods_button_ref.append(gods_button)

        # info, stats and next Buttons
        self.info_stats_frame = Frame(self.quiz_frame)
        self.info_stats_frame.grid(row=6)

        self.next_button = Button(self.info_stats_frame, text="Next Round", bg="#0057D8",
                                  command=self.next_quiz_type, font=("Arial", 16, "bold"),
                                  fg="#FFFFFF", width=10)
        self.next_button.grid(row=0, column=2, padx=5, pady=5)

        self.info_button = Button(self.info_stats_frame, text="Info", bg="#FF8000", command=self.to_info, font=("Arial", 16, "bold"),
                                   fg="#FFFFFF", width=10)
        self.info_button.grid(row=0, column=0, padx=5, pady=5)

        self.stats_button = Button(self.info_stats_frame, text="Stats", bg="#333333", command=self.to_stats, font=("Arial", 16, "bold"),
                                   fg="#FFFFFF", width=10)
        self.stats_button.grid(row=0, column=1, padx=5, pady=5)

        self.end_quiz_button = Button(self.quiz_frame, text="End", bg="#990000", font=("Arial", 16, "bold"),
                                      fg="#FFFFFF", width=33, command=self.close_play)
        self.end_quiz_button.grid(row=7, pady=10)

        self.next_quiz_type()

    def next_quiz_type(self):
        # Checks if quiz type is mixed
        if self.original_quiz_type == 3:
            self.quiz_type = random.choice([1, 2])
        self.new_round(self.quiz_type)

    def new_round(self, current_quiz_type):
        rounds_played = self.rounds_played.get() + 1
        self.rounds_played.set(rounds_played)
        rounds_wanted = self.rounds_wanted.get()

        if current_quiz_type == 1:
            self.round_god, round_god_origin = get_round_gods_desc(1)
            self.target_description = round_god_origin

            self.heading_label.config(text=f"Round {rounds_played} of {rounds_wanted}")
            self.target_label.config(text=f"Is {self.round_god} a Greek or Roman god?", font=("Arial", 14, "bold"))
            self.results_label.config(text=f"{'=' * 7}", bg="#F0F0F0")

            for item in self.greek_roman_button_ref:
                item.config(state=NORMAL)
            self.greek_button.grid(row=0, column=0, padx=5, pady=5)
            self.roman_button.grid(row=0, column=1, padx=5, pady=5)
            self.gods_name_frame.grid_forget()

        elif current_quiz_type == 2:
            self.round_gods_list, description = get_round_gods_desc(2)
            self.target_description = description

            self.heading_label.config(text=f"Round {rounds_played} of {rounds_wanted}")
            self.target_label.config(text=f"Who is the God of {description}?", font=("Arial", 14, "bold"))
            self.results_label.config(text=f"{'=' * 7}", bg="#F0F0F0")

            for count, item in enumerate(self.gods_button_ref):
                item.config(text=self.round_gods_list[count][2], state=NORMAL)

            self.greek_button.grid_forget()
            self.roman_button.grid_forget()
            self.gods_name_frame.grid(row=0, column=0, columnspan=2)

        self.next_button.config(state=DISABLED)

    def rounds_results(self, user_choice, quiz_type):
        rounds_won = self.rounds_won.get()

        if quiz_type == 1:
            # Get user score on button press...
            score = user_choice

            # Retrieve target and compare with user score to find round results
            target = self.target_description
            self.all_origin_list.append(target)

            if score == target:
                result_text = f"Success!! {user_choice} was correct!!"
                result_bg = "#82B366"
                self.all_score_list.append(score)

                rounds_won += 1
                self.rounds_won.set(rounds_won)
            else:
                result_text = f"Oops {user_choice} was incorrect. The Correct Answer was {target}"
                result_bg = "#F8CECC"
                self.all_score_list.append(0)

            self.results_label.config(text=result_text, bg=result_bg)

            for item in self.greek_roman_button_ref:
                item.config(state=DISABLED)

        if quiz_type == 2:
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

                rounds_won += 1
                self.rounds_won.set(rounds_won)

            else:
                result_text = f"Oops {gods_name} was incorrect."
                result_bg = "#F8CECC"
                self.all_score_list.append(0)

            self.results_label.config(text=result_text, bg=result_bg)

            for item in self.gods_button_ref:
                item.config(state=DISABLED)

        # Enable stats & next buttons, disable color buttons
        self.next_button.config(state=NORMAL)
        self.stats_button.config(state=NORMAL)

        # Check to see if game is over
        rounds_played = self.rounds_played.get()
        rounds_wanted = self.rounds_wanted.get()

        if rounds_played == rounds_wanted:
            self.next_button.config(state=DISABLED, text="Game Over")
            self.end_quiz_button.config(text="Play Again", bg="#006600")

    def to_info(self):
        """
        Displays info for playing game
        """
        rounds_played = self.rounds_played.get()
        DisplayInfo(self, rounds_played)

    def close_play(self):
        # Reshow root (ie: choose rounds) and end current
        # game / allow new game to start
        root.deiconify()
        self.play_box.destroy()

    def to_stats(self):
        """
        Displays stats for playing game
        """
        rounds_won = self.rounds_won.get()
        stats_bundle = [rounds_won, self.all_score_list]
        print(stats_bundle)
        Stats(self, stats_bundle)


class DisplayInfo:
    """
    Interface for playing the Colout Quest Game
    """
    """
    Displays info dialogue box
    """

    def __init__(self, partner, rounds_played):

        self.rounds_played = rounds_played

        # Setup dialogue box and background colour
        background = "#ffe6cc"
        self.info_box = Toplevel()

        # Disable info box
        partner.info_button.config(state=DISABLED)
        partner.end_quiz_button.config(state=DISABLED)
        partner.stats_button.config(state=DISABLED)

        # If users press cross at top, closes info and
        # 'releases' info button
        self.info_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_info, partner))

        self.info_frame = Frame(self.info_box, width=300,
                                height=200)
        self.info_frame.grid()

        self.info_heading_label = Label(self.info_frame,
                                        text="info",
                                        font=("Arial", "14", "bold"))
        self.info_heading_label.grid(row=0)

        info_text = ("Gods \n\n"
                      "Good luck!")

        self.info_text_label = Label(self.info_frame,
                                     text=info_text,
                                     wraplength=350, justify="left")
        self.info_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.info_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_info, partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

        # List and loop to set background colour on
        # everything except the buttons.
        recolour_list = [self.info_frame, self.info_heading_label,
                         self.info_text_label]

        for item in recolour_list:
            item.config(bg=background)

    def close_info(self, partner):
        """
        Closes info dialogue box (and enables info button
        """
        # Put help button back to normal...
        partner.info_button.config(state=NORMAL)
        partner.end_quiz_button.config(state=NORMAL)

        # Put info button back to normal...
        if self.rounds_played >=1:
            partner.info_button.config(state=NORMAL)
        self.info_box.destroy()

class Stats:

    def __init__(self, partner, all_stats_info):

        # disable buttons to prevent programs crashing
        partner.info_button.config(state=DISABLED)
        partner.end_quiz_button.config(state=DISABLED)
        partner.stats_button.config(state=DISABLED)

        # Extract information form master list...
        rounds_won = all_stats_info[0]
        user_scores = all_stats_info[1]


        # sort user scores to find high score...
        user_scores.sort()

        background = "#ffe6cc"
        self.stats_box = Toplevel()

        # disable help button
        partner.stats_button.config(state=DISABLED)

        # If users press cross at top, closes help and
        # 'releases' help button
        self.stats_box.protocol('WM_DELETE_WINDOW',
                                partial(self.close_stats, partner))

        self.stats_frame = Frame(self.stats_box, width=350)
        self.stats_frame.grid()

        # math to populate Stats dialogue...
        rounds_played = len(user_scores)

        success_rate = rounds_won / rounds_played * 100
        total_score = sum(user_scores)


        best_score = user_scores[-1]
        average_score = total_score / rounds_played

        # Strings for Stats labels...
        success_string = (f"Success Rate: {rounds_won} / {rounds_played}"
                          f" ({success_rate:.0f}%)")
        total_score_string = f"Total Score: {total_score}"

        best_score_string = f"Best Score: {best_score}"


        if total_score == 0:
            comment_string = ("Oops - You've got every question wrong!")
            comment_colour = "#F9CECC"
            best_score_string = f"best Score: n/a"
        else:
            comment_string = ""
            comment_colour = "#F0F0F0"

        average_score_string = f"Average Score: {average_score:.0f}\n"

        heading_font = ("Arial", "16", "bold")
        normal_font = ("Arial", "14")
        comment_font = ("Arial", "13")

        # Label list (text | fnt | 'Sticky')
        all_stats_strings = [
            ["Statistics", heading_font, ""],
            [success_string, normal_font, "W"],
            [total_score_string, normal_font, "W"],
            [comment_string, comment_font, "W"],
            ["\nRound Stats", heading_font, ""],
            [best_score_string, normal_font, "W"],
            [average_score_string, normal_font, "W"]
        ]

        stats_label_ref_list = []
        for count, item in enumerate(all_stats_strings):
            self.stats_label = Label(self.stats_frame, text=item[0], font=item[1],
                                     anchor="w", justify="left",
                                     padx=30, pady=5)
            self.stats_label.grid(row=count, sticky=item[2], padx=10)
            stats_label_ref_list.append(self.stats_label)

        # Configure command label background (for all won / all lost)
        stats_comment_label = stats_label_ref_list[4]
        stats_comment_label.config(bg=comment_colour)

        self.dismiss_button = Button(self.stats_frame,
                                     font=("Arial", "16", "bold"),
                                     text="Dismiss", bg="#333333",
                                     fg="#FFFFFF", width=20,
                                     command=partial(self.close_stats,
                                                     partner))
        self.dismiss_button.grid(row=8, padx=10, pady=10)


    def close_stats(self, partner):
        """
        Closes stats dialogue box (and enables stats button
        """
        # Put stats button back to normal...
        partner.info_button.config(state=NORMAL)
        partner.end_quiz_button.config(state=NORMAL)
        partner.stats_button.config(state=NORMAL)
        self.stats_box.destroy()


if __name__ == "__main__":
    root = Tk()
    root.title("God Quiz")
    StartQuiz()
    root.mainloop()
