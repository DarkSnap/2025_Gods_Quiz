from tkinter import *
from functools import partial  # To prevent unwanted windows


class StartGame:
    """
    Initial Game interface (Asks users how many rounds they
    would like to play
    """

    def __init__(self):

        """
        Gets number of rounds from user
        """

        self.start_frame = Frame(padx=60, pady=30)
        self.start_frame.grid()

        # Strings for labels
        intro_string = "blah blah ablh fill this in later"

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


        self.greek_roman_game_select = Button(self.entry_area_frame, font=("Arial", "20"), text="Greek/Roman",
                                           width=15, fg="#FFFFFF", bg="#FF9999")
        self.greek_roman_game_select.grid(row=1, column=0, padx=10, pady=10)

        self.god_name_game_select = Button(self.entry_area_frame, font=("Arial", "20") , text="God Name",
                                           width=15, fg="#FFFFFF", bg="#96C5F7")
        self.god_name_game_select.grid(row=1, column=1, padx=10, pady=10)


        self.num_rounds_entry = Entry(self.entry_area_frame, font=("Arial", "20", "bold"),
                                      width=16)

        self.num_rounds_entry.grid(row=2, column=0, padx=10, pady=10)

        # Create play button
        self.play_button = Button(self.entry_area_frame, font=("Arial", "20", "bold"),
                                  fg="#FFFFFF", bg="#0B6E4F", text="Play", width=14,
                                  command=self.check_rounds)
        self.play_button.grid(row=2, column=1)

    def check_rounds(self):
        """
        Checks users have entered 1 or more rounds
        """

        # Retrieves number of rounds to be played
        rounds_wanted = self.num_rounds_entry.get()
        game_selected = self.god_name_game_select.get()

        # Reset label and entry box (for when users come back to home screen)
        self.choose_label.config(fg="#009900", font=("Arial", "16", "bold"))
        self.num_rounds_entry.config(bg="#FFFFFF")

        error = "Oops - Please choose a whole number more then zero"
        has_errors = "no"

        # Checks that rounds to be player is a number above zero
        try:
            rounds_wanted = int(rounds_wanted)
            if rounds_wanted > 0:
                # Invoke Player Class (and take across number of rounds)
                Play(rounds_wanted)
                # Hide root window (ie: hide rounds choice window).
                root.withdraw()

            else:
                has_errors = "yes"

        except ValueError:
            has_errors = "yes"

        # Display the error if necessary
        if has_errors == "yes":
            self.choose_label.config(text=error, fg="#990000",
                                     font=("Arial", "10", "bold"))
            self.num_rounds_entry.config(bg="#F4CCCC")
            self.num_rounds_entry.delete(0, END)


class Play:
    """
    Interface for playing the Colout Quest Game
    """

    def __init__(self, how_many):
        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        self.game_heading_label = Label(self.game_frame, text=f"Round 0 of {how_many}",
                                        font=("Arial", "16", "bold"))
        self.game_heading_label.grid(row=0)

        self.end_game_button = Button(self.game_frame, text="End Game",
                                      font=("Arial", "16", "bold",),
                                      fg="#FFFFFF", bg="#990000", width="10",
                                      command=self.close_play)
        self.end_game_button.grid(row=1)

    def close_play(self):
        # Reshow root (ie: choose rounds) and end current
        # game / allow new game to start
        root.deiconify()
        self.play_box.destroy()


# Main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Gods Quiz")
    StartGame()
    root.mainloop()
