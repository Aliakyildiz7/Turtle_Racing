import turtle
# turtle is the name of the library. turtle.Turtle is the class in the library that represents the "turtle"
import time
import random
import tkinter as tk
from tkinter import messagebox

"""
This code simulates a turtle racing in turtle library, with the user interaction through tkinter screen.
All the attributes and methods other than tkinter widgets are encapsulated in Tosbaga class, inherited from turtle.Turtle class.
It includes:
-User Input through tkinter turtle numbers
_Validation of the input with tkinter warnings
_Setting up the turtle screen for racing dimensions, equally spacing them laterally.
_Setting up necessary attributes and boolean conditions for racing.
_Simulating the race in turtle screen with random increments in each iteration.
_Printing the results with regards to time attribute of Tosbaga instances, which saves the  race times.

"""


# Creation of Tosbaga Class with inheritance
class Tosbaga(turtle.Turtle):
    """
    Tosbaga means turtle in Turkish.
    """
    all = []  # The class attribute list to save all the instances intialized

    #These are attributes that will be used in multiple methods.
    #These attributes are initialized here to make them accessible for all methods, they are not assigned to their intended values.
    n = 0 #Number of Tosbagas
    finish_length = 0 #Distance of race


    def __init__(self, no, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Calling the initializer of the parent class to prevent overwriting

        #Assign to self object
        self.no = len(Tosbaga.all)

        #Setting the initial value
        self.tr = 0  # total road a Tosbaga went

        # Saving the initialized instance
        Tosbaga.all.append(self)

    def __repr__(self): #Identifying each instance created by a unique name
        return str(f"Tosbaga{self.no}")

    def is_finished(self): #Will check if a Tosbaga has finished the race
        if self.tr >= Tosbaga.finish_length:
            return True
        return False



    @staticmethod
    def start_prep():
        """
        Will get user input through tkinter entry, create tosbagas, assign needed attributes and initialize Tosbagas.
        """

        #User Input Validation Loop. Restricts the user to only type in integers in the range[2-10]
        while True:
            try:
                Tosbaga.n = int(number_of_tosbagas_entry.get())

                if Tosbaga.n < 2 or Tosbaga.n > 10:
                    tk.messagebox.showwarning(title="Warning", message="Please enter an integer between 2 and 10")
                    return root.mainloop()
                else:
                    break

            except ValueError:
                tk.messagebox.showwarning(title="Warning", message="Please enter an integer")
                return root.mainloop()

        number_of_tosbagas_entry.config(state="disabled") #Disabled the user to type anything afterwards.
        button.config(state="disabled") #The button will be disabled in the beginning of each function.
        #And then will be enabled again at the end. This will prevent accidental clicking.

        # Setting up the screen
        turtle.bgcolor("black")
        sc_width = 600  # Total width of the graphics screen
        sc_height = 800  # Total height of the graphic screen
        turtle.setup(width=sc_width, height=sc_height)

        # Dimensioning
        upward_blank = 50  # The blank space between the upper edge of the screen and the finish line
        Tosbaga.finish_length = sc_height / 2 - upward_blank  # The length between the finish line and the start

        side_blank = 50  # The blank space between the lateral edge of the screen and the first (or last) turtle
        horizontal_bottom = -sc_width / 2  # x Coordination of leftmost lateral edge
        race_line_bottom = horizontal_bottom + side_blank  # x Coordination of leftmost turtle
        race_line_top = -race_line_bottom  # x coordination of the rightmost turtle

        race_line_length = race_line_top - race_line_bottom  # The lateral distance between the first  and the last turtle

        # Creating the Finish Line
        line_drawer = turtle.Turtle()
        line_drawer.color("black")
        line_drawer.penup()
        line_drawer.speed(0)
        line_drawer.pensize(20)

        line_drawer.setpos(race_line_bottom, Tosbaga.finish_length)
        line_drawer.color("white")
        line_drawer.hideturtle()
        line_drawer.pendown()
        line_drawer.forward(race_line_length)

        # Setting up the color matrice
        color_matrix = ["blue", "red", "yellow", "green", "turquoise", "purple", "brown"]

        #Creation of Tosbagas
        for x in range(Tosbaga.n):
            dummy = Tosbaga(Tosbaga.n)

            dummy.speed(10)
            dummy.turtlesize(2)
            dummy.shape("turtle")
            dummy.left(90)
            dummy.color(random.choice(color_matrix))
            dummy.pensize(4)

            dummy.total_road = 0
            dummy.turtle_time = 0
            dummy.finish_boolean = False

        #Setting the starting positions
        s = race_line_length / (Tosbaga.n - 1) #Lateral distance between two Tosbagas.

        for tosbaga in Tosbaga.all:
            tosbaga.penup()
            tosbaga.setpos(race_line_bottom + s * tosbaga.no, 0)
            tosbaga.pendown()

        # Introducing Tosbagas to User
        message_2 = f"Racing is about to start. The contestant Tosbagas are:\n\n"
        for tosbaga in Tosbaga.all:
            message_2 = message_2 + f"Number {tosbaga.no} with the color {tosbaga.color()[0]}\n"
        message_2 = message_2 + "\nClick the button to start the race\n"

        announcement_text.config(state="normal")
        announcement_text.insert(0.0, message_2)
        announcement_text.config(state="disabled")

        button.config(state="normal", command=Tosbaga.start_race)



    @staticmethod
    def start_race():
        """
        This will be executed after tosbagas  are ready.
        """

        button.config(state="disabled")


        #Racing Condition
        def is_racing_going_on():
            """
            Will turn false when all the tosbagas finish race and end the following while loop
            """
            finish_count = 0
            for x in Tosbaga.all:
                if x.is_finished() == True:
                    finish_count += 1

            if finish_count == len(Tosbaga.all):
                return False
            else:
                return True

        #Racing
        i = 0  #Cycle Count

        while is_racing_going_on():

            for x in Tosbaga.all:

                if i == 0: #Initializing the start time
                    x.time_start = time.time()

                if x.is_finished() == False:

                    if str(x) == "Tosbaga0":  #rigged Tosbaga
                        r = 25

                    else:
                        r = random.randint(1, 5)

                        # Gives 1 / n probability that a tosbaga is supercharged.
                        # That makes the deviation of the results wider, thus making a more race_like animation
                        luck = random.randint(1, Tosbaga.n)
                        if luck == 1:
                            r = 20

                    # Prevents tosbagas from overshooting the finish line
                    if Tosbaga.finish_length - x.tr < r:
                        r = Tosbaga.finish_length - x.tr

                    x.forward(r)
                    x.tr = x.tr + r

                    if x.is_finished() == True: #Creating an attribute to save times
                        x.time = time.time() - x.time_start

            i += 1



        else:
            announcement_text.config(state="normal")
            announcement_text.insert(tk.END, "\nRace is over!!!  Click the button to see the results\n\n")
            announcement_text.config(state="disabled")

        button.config(state="normal", command=Tosbaga.print_results)


    @staticmethod
    def print_results():
        """
        Prints the results into tkinter screen
        """
        button.config(state="disabled")

        # Post Processing
        result_list = Tosbaga.all.copy()
        result_list.sort(key=lambda x: x.time) #Sorts the list with respect to time atttribute

        final_message = ""
        for x in range(len(result_list)):

            if x == 0: #Rigged Tosbaga
                final_message = final_message + (
                    f"Tosbaga Number {result_list[x].no} with the color {result_list[x].color()[0]} "
                    f"has been disqualified due to the detection of steroid use.\n\n")


            elif x == 1: #Winner Tosbaga
                final_message = final_message + (
                    f"Tosbaga Number {result_list[x].no} with the color {result_list[x].color()[0]} "
                    f"has won the race  with the total time of {result_list[x].time: .3f} seconds\n")
                final_message = final_message + (f"Congratulations Tosbaga {result_list[x].no} !!!\n\n")


            elif x == len(result_list) - 1: #Last Tosbaga

                final_message = final_message + (
                    f"Tosbaga Number {result_list[x].no} with the color {result_list[x].color()[0]} "
                    f"has finished the race in the very last position with the total time of {result_list[x].time: .3f} seconds\n")
                final_message = final_message + (f"You gotta do better Tosbaga {result_list[x].no} !!!\n\n")


            else: #Other Tosbagas
                final_message = final_message + (
                    f"Tosbaga Number {result_list[x].no} with the color {result_list[x].color()[0]} "
                    f"has finished the race in the {x}. position with the total time of {result_list[x].time: .3f} seconds\n\n")

        final_message = final_message + "Click the button for another race!!!"

        announcement_text.config(state="normal")
        announcement_text.insert(tk.END, final_message)
        announcement_text.config(state="disabled")
        button.config(state="normal", command=lambda: (turtle.Screen().reset(), Tosbaga.reload()))


    @staticmethod
    def reload():
        """
        Prepares the tkinter and turtle screens for another race
        """

        announcement_text.config(state="normal")
        announcement_text.delete(0.0, tk.END)
        announcement_text.config(state="disabled")

        number_of_tosbagas_entry.config(state="normal")
        number_of_tosbagas_entry.delete(0, tk.END)

        Tosbaga.all.clear()
        button.config(command=Tosbaga.start_prep)



#Setting up the Tkinter GUI
root = tk.Tk()
root.title("Turtle Racing")

master_frame = tk.Frame(root, bg="lightblue")
master_frame.pack(padx=20, pady=20)

welcome_frame = tk.Frame(master_frame, bg="lightblue")
welcome_frame.grid(row=0, column=0, sticky="w")


message_1 = "Welcome to the tosbaga racing!!!\n"
message_1 = message_1 + "How many tosbagas would  you like to see racing today?\n"
message_1 = message_1 + "There are total of 10 tosbagas and at least 2  tosbagas must race.\n"


entry_label = tk.Label(welcome_frame, text=message_1, font=("Arial, 12"), anchor="w", justify="left", bg="lightblue")
entry_label.grid(row=0, column=0, sticky="w")

start_prep_frame = tk.Frame(master_frame, bg="lightblue")
start_prep_frame.grid(row=1, column=0, sticky="w")

number_of_tosbagas_entry = tk.Entry(start_prep_frame, font=("Arial, 12"))
number_of_tosbagas_entry.grid(row=1, column=0, sticky="w")

button = tk.Button(start_prep_frame, command=Tosbaga.start_prep, text="Click me", bg="red")
button.grid(row=1, column=1, padx=10, sticky="e")

announcement_frame = tk.Frame(master_frame, bg="lightblue")
announcement_frame.grid(row=2, column=0, pady=30)

announcement_text = tk.Text(announcement_frame, wrap=tk.WORD, font=("Arial, 12"), bg="lightblue", borderwidth=0, state="disabled")
announcement_text.grid(row=0, column=0)

scrollbar = tk.Scrollbar(announcement_frame, command=announcement_text.yview)
scrollbar.grid(row=0, column=1)


root.mainloop()




