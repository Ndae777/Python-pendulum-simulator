import turtle
import random
import math
import time
import tkinter as tk
from tkinter import ttk, messagebox

 

# Global Constants

g = 9.81  # Gravity
initial_angle = math.pi / 4  # Initial angle (45 degrees in radians)
damping = 0.995  # Damping factor

 
pendulum_colors = ["red", "blue", "green", "yellow", "orange", "purple"]

 

def setup_screen():
    """Initializes the screen settings."""
    screen = turtle.Screen()
    screen.title("Multi-Pendulum Simulator")
    screen.bgcolor("black")
    screen.setup(width=800, height=600)  # Increased screen size for better visibility
    screen.tracer(0)  # Turn off auto screen updates for smoother animation
    return screen

 

def create_pendulum(angle, length, color):
    pendulum = {
        "angle": angle,
        "angular_velocity": 0,
        "angular_acceleration": 0,
        "cycles": 0,
        "previous_direction": 1 if angle > 0 else -1,
        "length": length,
        "color": color,
        "rod": turtle.Turtle(),
        "bob": turtle.Turtle()
    }

 

    # Configure rod

    pendulum["rod"].hideturtle()
    pendulum["rod"].color("white")
    pendulum["rod"].speed(0)
    pendulum["rod"].width(4)
     

    # Configure bob

    pendulum["bob"].shape("circle")
    pendulum["bob"].color(color)
    pendulum["bob"].shapesize(1.5, 1.5)
    pendulum["bob"].penup()

    return pendulum

 

def calculate_position(pendulum):
    bob_x = pendulum["length"] * math.sin(pendulum["angle"])
    bob_y = -pendulum["length"] * math.cos(pendulum["angle"])
    return bob_x, bob_y

 

def update_physics(pendulum):
    pendulum["angular_acceleration"] = (-g / pendulum["length"]) * math.sin(pendulum["angle"])
    pendulum["angular_velocity"] += pendulum["angular_acceleration"]
    pendulum["angle"] += pendulum["angular_velocity"]

 

def apply_damping(pendulum):
    pendulum["angular_velocity"] *= damping

 

def draw_pendulum(pendulum):
    bob_x, bob_y = calculate_position(pendulum)

 

    # Draw rod
    pendulum["rod"].clear()
    pendulum["rod"].penup()
    pendulum["rod"].goto(0, 0)  # Pivot point
    pendulum["rod"].pendown()
    pendulum["rod"].goto(bob_x, bob_y)  # Draw rod to bob position

 

    # Position the bob

    pendulum["bob"].goto(bob_x, bob_y)

 

def check_cycle(pendulum):

    current_direction = 1 if pendulum["angle"] > 0 else -1
    if current_direction != pendulum["previous_direction"]:
        pendulum["cycles"] += 0.5  # Half cycle each time it crosses
        pendulum["previous_direction"] = current_direction
    return pendulum["cycles"]

 

def update_hands(minute_hand, second_hand):

    current_time = time.localtime()
    minutes = current_time.tm_min
    seconds = current_time.tm_sec

 

    # Update second hand
    second_angle = 360 * (seconds / 60)
    second_hand.setheading(90 - second_angle)

 

    # Update minute hand
    minute_angle = 360 * (minutes / 60)
    minute_hand.setheading(90 - minute_angle)

 
def clock_centre():

    center = turtle.Turtle()
    center.speed(0)
    center.penup()
    center.goto(0, 135)
    center.shape("circle")
    center.color("green")

 
def create_clock():

    face = turtle.Turtle()
    face.ht()
    face.speed(0)
    face.color("white")
    face.width(4)
    face.circle(135)
    clock_centre()

 
def start_simulation():

    global maxPendulums
    maxPendulums = int(slider.get())-1

 

    # Validate the lengths input
    try:
        

        min_len = int(min_length_entry.get())
        max_len = int(max_length_entry.get())
        if min_len < 130 or min_len > 300 or max_len < 130 or max_len > 300:
            raise ValueError("Length values must be between 130 and 300.")

        if min_len >= max_len:
            raise ValueError("Minimum length must be less than maximum length.")

    except ValueError as e:
        messagebox.showerror("Invalid Input", f"Error: {e}")

        return

 

    screen = setup_screen()
    pendulums = [create_pendulum(initial_angle, random.randint(min_len, max_len), random.choice(pendulum_colors))]
    num_added_pendulums = 0
    
    create_clock()

 

    # Creating arms
    arm1 = turtle.Turtle()
    arm1.speed(0)
    arm1.penup()
    arm1.goto(0, 135)
    arm1.color("red")
    arm1.shape("arrow")
    arm1.shapesize(stretch_wid=0.2, stretch_len=6)
    arm1.setheading(90)
    arm1.pendown()

 

    arm2 = turtle.Turtle()
    arm2.speed(0)
    arm2.penup()
    arm2.goto(0, 135)
    arm2.color("yellow")
    arm2.shape("arrow")
    arm2.shapesize(stretch_wid=0.2, stretch_len=8)
    arm2.setheading(90)
    arm2.pendown()

 

    while True:

        for pendulum in pendulums:
            update_physics(pendulum)
            apply_damping(pendulum)
            draw_pendulum(pendulum)

 

            if num_added_pendulums < maxPendulums and check_cycle(pendulums[0]) >= 4:
                pendulums.append(create_pendulum(initial_angle, random.randint(min_len, max_len), random.choice(pendulum_colors)))
                num_added_pendulums += 1
                pendulums[0]["cycles"] = 0

 

        update_hands(arm1, arm2)  # For the clock
        screen.update()
        time.sleep(0.02)

    turtle.exitonclick()

 

def update_slider_label(value):
    slider_value_label.config(text=f"Number of Pendulums: {int(float(value))}")

 

# GUI Setup

window = tk.Tk()
window.title("Multi-Pendulum Simulator")
window.geometry("300x300")
window.configure(bg="black")


style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=10)
style.configure("TLabel", background="black", foreground="white", font=("Arial", 12))
style.configure("TFrame", background="black")

 
title_label = ttk.Label(window, text="Multi-Pendulum Simulator", font=("Arial", 16, "bold"))
title_label.pack(pady=10)
 
frame = ttk.Frame(window, padding=10)
frame.pack()
 
slider_label = ttk.Label(frame, text="Select Number of Pendulums:")
slider_label.pack()
 
slider = ttk.Scale(frame, from_=1, to=10, orient=tk.HORIZONTAL, command=update_slider_label)
slider.pack()

slider_value_label = ttk.Label(frame, text="Number of Pendulums: 1")  # Initial label value
slider_value_label.pack()

 

# Min and Max Length Entry
min_length_label = ttk.Label(frame, text="Enter Minimum Length (130 - 300):")
min_length_label.pack()

min_length_entry = ttk.Entry(frame)
min_length_entry.insert(0, "130")  # Default minimum length
min_length_entry.pack()

max_length_label = ttk.Label(frame, text="Enter Maximum Length (130 - 300):")
max_length_label.pack() 

max_length_entry = ttk.Entry(frame)
max_length_entry.insert(0, "300")  # Default maximum length
max_length_entry.pack()

start_button = ttk.Button(frame, text="Start Simulation", command=start_simulation)
start_button.pack(pady=10)

window.mainloop()

if __name__ == "__main__":
    window.mainloop()
