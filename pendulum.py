import tkinter as tk
from enum import Enum
import math
    
class Pendulum:
    def __init__(self):
        # Set up window
        self.window = tk.Tk() 
        self.window.title("Pendulum Simulation") 

        self.G = 9800
        self.canvas_width = 500
        self.canvas_height = 500

        self.pivot_r = 10
        self.pivot_x = None
        self.pivot_y = None

        self.bob_r = 20
        self.bob_x = None
        self.bob_y = None

        self.delta_time_millis = 10
        self.fill_color = 'red'

        self.vel_x = None
        self.vel_y = None
        self.velocity = None
        self.pendulum_length = None

        self.state = State.WAITING_FOR_PIVOT

        # Place canvas in window
        self.canvas = tk.Canvas(self.window, 
                width = self.canvas_width,
                height = self.canvas_height,
                bg = 'white') 
        self.canvas.grid(row = 1, column = 1)

        # Set up mouse click handlers for user
        # to specify the two balls
        self.canvas.bind("<ButtonRelease-1>", self.mouse_click_handler)

        # Button frame in window
        self.button_frame = tk.Frame(self.window)
        self.button_frame.grid(row = 2, column = 1)

        self.clear_button = tk.Button(self.button_frame,
                text = "Clear", command = self.clear)
        self.clear_button.grid(row = 1, column = 1)

        self.quit_button = tk.Button(self.button_frame,
                text = "Quit", command = self.quit)
        self.quit_button.grid(row = 1, column = 2)

        # Start event loop
        self.window.mainloop() 

    def mouse_click_handler(self, event):
        """ Handle mouse click. """
        if self.state == State.WAITING_FOR_PIVOT:
            # Get the pivot point
            self.pivot_x = event.x
            self.pivot_y = event.y
            self.canvas.create_oval(
                self.pivot_x - self.pivot_r,
                self.pivot_y - self.pivot_r,
                self.pivot_x + self.pivot_r,
                self.pivot_y + self.pivot_r,
                fill = self.fill_color, tags = ("all", "pivot"))
            self.state = State.WAITING_FOR_BOB
        elif self.state == State.WAITING_FOR_BOB:
            # Get the Bob point
            self.bob_x = event.x
            self.bob_y = event.y
            self.canvas.create_line(
                self.pivot_x, self.pivot_y,
                self.bob_x, self.bob_y,
                fill = self.fill_color, tags = ("all", "line"))
            self.canvas.create_oval(
                self.bob_x - self.bob_r,
                self.bob_y - self.bob_r,
                self.bob_x + self.bob_r,
                self.bob_y + self.bob_r,
                fill = self.fill_color, tags = ("all", "bob"))
            self.vel_x = 0
            self.vel_y = 0
            self.velocity = 0
            self.pendulum_length = math.sqrt(
                (self.pivot_x - self.bob_x)**2 + (self.pivot_y - self.bob_y)**2)
            print("Pendulum length =", self.pendulum_length, "millimeters")
            self.state = State.PAUSED
        elif self.state == State.PAUSED:
            # restart the simulation
            self.timer = self.window.after(
                self.delta_time_millis, self.step_handler)
            self.state = State.RUNNING
        else: # self.state == State.RUNNING
            # Pause the simulation
            self.window.after_cancel(self.timer)
            self.state = State.PAUSED

    def step_handler(self):
        """ Perform one step of the simulation. """

        # Get current angle
        cur_angle = math.acos((self.bob_x - self.pivot_x) / self.pendulum_length)

        # Compute acceleration.
        acceleration = math.cos(cur_angle) * self.G

        # Update velocity
        self.velocity += acceleration * self.delta_time_millis / 1000

        # Compute distance traveled
        distance = self.velocity * self.delta_time_millis / 1000

        # Compute change of angle, and update cur_angle
        delta_angle = math.atan(distance / self.pendulum_length)
        cur_angle += delta_angle

        # Update location
        self.bob_x = self.pivot_x + math.cos(cur_angle) * self.pendulum_length
        self.bob_y = self.pivot_y + math.sin(cur_angle) * self.pendulum_length

        # Redraw
        self.canvas.delete("bob")
        self.canvas.delete("line")
        self.canvas.create_line(
                self.pivot_x, self.pivot_y,
                self.bob_x, self.bob_y,
                fill = self.fill_color, tags = ("all", "line"))
        self.canvas.create_oval(
                self.bob_x - self.bob_r,
                self.bob_y - self.bob_r,
                self.bob_x + self.bob_r,
                self.bob_y + self.bob_r,
                fill = self.fill_color, tags = ("all", "bob"))

        # Schedule next event
        self.timer = self.canvas.after(
                self.delta_time_millis, self.step_handler)

    def quit(self):
        """ Quit the simulation. """
        self.window.destroy()

    def clear(self):
        self.canvas.delete("all")
        if self.state == State.RUNNING:
            self.window.after_cancel(self.timer)
        self.state = State.WAITING_FOR_PIVOT

class State(Enum):
    WAITING_FOR_PIVOT = 1
    WAITING_FOR_BOB = 2
    PAUSED = 3
    RUNNING = 4

        
if __name__ == "__main__":
    # Create GUI
    Pendulum() 