import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import threading
import cv2

class MenuApp:
    def __init__(self, master):
        self.master = master
        master.title("Menu App")

        # Create a Canvas widget
        self.canvas = tk.Canvas(master, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)

        # Load the background image
        self.original_bg_image = Image.open("/Users/kierreog/Desktop/FinalProject/_.jpeg")

        # Bind canvas resize event to update image
        self.canvas.bind("<Configure>", self.on_resize)

        # Create a Frame for buttons
        self.button_frame = tk.Frame(master, bg="light grey")
        self.button_frame.pack(side="bottom", fill="x", pady=10)

        # Define button properties for larger buttons
        button_font = ('Helvetica', 14, 'bold')  # Larger font size and bold
        button_padx = 20  # Increase horizontal padding
        button_pady = 10  # Increase vertical padding

        # Creating buttons for each application within the Frame
        self.create_button("Chatty", self.open_chatty, "red")
        self.create_button("Image Generation", self.open_image_generation, "gold")
        self.create_button("Snake Game", self.open_snake_game, "purple")
        self.create_button("Weather App", self.open_weather_app, "red")
        self.create_button("Vision", self.open_vision_app, "green")  # Added new button
        self.create_button("Exit", self.exit_application, "red")
        self.create_button("Contact", self.show_contact_info, "blue")

        # Initialize contact info label and image label
        self.contact_info_label = tk.Label(self.canvas, bg="white", fg="black", font=button_font, padx=10, pady=10, wraplength=400)
        self.contact_info_label.place_forget()  # Initially hide the label

        self.contact_image_label = tk.Label(self.canvas)
        self.contact_image_label.place_forget()  # Initially hide the label

        # Load and resize the contact image
        self.contact_image = Image.open("/Users/kierreog/Desktop/FinalProject/selfie.jpg")
        self.contact_image = self.contact_image.resize((200, 200), Image.LANCZOS)  # Resize image to be larger
        self.contact_photo = ImageTk.PhotoImage(self.contact_image)

    def create_button(self, text, command, color):
        button = tk.Button(self.button_frame, text=text, command=command, bg=color, fg="black",
                           font=('Helvetica', 14, 'bold'), padx=20, pady=10)
        button.pack(pady=5, padx=10, side="left")

    def update_image(self, width, height):
        if width <= 0 or height <= 0:
            return
        
        # Resize the image to fill the canvas dimensions
        resized_image = self.original_bg_image.resize((width, height), Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(resized_image)

        # Clear previous image and display the new one
        self.canvas.delete("background")

        # Display the image stretched to fill the canvas
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image, tags="background")

    def on_resize(self, event):
        # Update image when the canvas is resized
        self.update_image(event.width, event.height)

    def open_chatty(self):
        subprocess.Popen(["python3", "/Users/kierreog/Desktop/FinalProject/Chatty/Chatty.py"])

    def open_image_generation(self):
        subprocess.Popen(["python3", "/Users/kierreog/Desktop/FinalProject/Image Generation/main.py"])

    def open_snake_game(self):
        subprocess.Popen(["python3", "/Users/kierreog/Desktop/FinalProject/snake_game/main.py"])

    def open_weather_app(self):
        subprocess.Popen(["python3", "/Users/kierreog/Desktop/FinalProject/WeatherApp_GUI/weatherApp_GUI.py"])

    def open_vision_app(self):
         subprocess.Popen(["python3", "/Users/kierreog/Desktop/FinalProject/Facial Recognition/Vision.py"])

    

    def exit_application(self):
        self.master.destroy()  # Close the Tkinter window

    def show_contact_info(self):
        contact_info = (
            "Email: kierre.ogbebor@hgs.hiddengeniusproject.org\n"
            "Instagram: @k3air\n"
            "Phone: xxx-xxx-xxxx"
        )
        # Update contact info label text and show it
        self.contact_info_label.config(text=contact_info)
        self.contact_info_label.place(x=20, y=20)  # Position on canvas; adjust as needed

        # Display contact image
        self.contact_image_label.config(image=self.contact_photo)
        self.contact_image_label.place(x=20, y=120)  # Position below contact info; adjust as needed

# Main program to create and run the Tkinter GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = MenuApp(root)
    root.mainloop()