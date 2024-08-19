import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import matplotlib
import psutil  # For system monitoring
import pyttsx3  # For voice responses
import requests  # For Weather API
import cv2  # For facial recognition
import os  # For folder opening
from NetHyTechSTT.listen import listen  # Import your custom STT module

matplotlib.use('TkAgg')

class JarvisDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("JARVIS Dashboard")
        self.root.geometry("1200x900")
        self.root.attributes("-alpha", 0.9)  # Make the window transparent
        self.engine = pyttsx3.init()

        # Initialize the canvas
        self.canvas = tk.Canvas(root, width=1200, height=900)
        self.canvas.pack()

        # Initialize the theme and apply it
        self.current_theme = "blue"
        self.themes = {"blue": {"bg": "#001f3f", "fg": "white"}, "dark": {"bg": "#111111", "fg": "green"}}
        self.update_theme(self.current_theme)

        # Initialize the Canvas for the futuristic GUI
        self.bg_img = Image.open("logo.png")
        self.bg_img = self.bg_img.resize((1200, 900), Image.LANCZOS)
        self.tk_bg_img = ImageTk.PhotoImage(self.bg_img)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_bg_img)

        # Weather Display
        self.weather_label = Label(root, text="Fetching Weather...", fg=self.themes[self.current_theme]["fg"],
                                   bg=self.themes[self.current_theme]["bg"], font=("Helvetica", 16))
        self.weather_label.place(x=900, y=200)

        # Fetch weather on start
        self.get_weather()

        # System Status Labels
        self.cpu_label = Label(root, text="CPU: ", fg=self.themes[self.current_theme]["fg"],
                               bg=self.themes[self.current_theme]["bg"], font=("Helvetica", 16))
        self.cpu_label.place(x=900, y=50)
        self.mem_label = Label(root, text="Memory: ", fg=self.themes[self.current_theme]["fg"],
                               bg=self.themes[self.current_theme]["bg"], font=("Helvetica", 16))
        self.mem_label.place(x=900, y=100)
        self.network_label = Label(root, text="Network: ", fg=self.themes[self.current_theme]["fg"],
                                   bg=self.themes[self.current_theme]["bg"], font=("Helvetica", 16))
        self.network_label.place(x=900, y=150)

        # Face Recognition Button
        self.face_rec_button = Button(root, text="Face Recognition", command=self.face_recognition, bg="red",
                                      fg="white")
        self.face_rec_button.place(x=900, y=300)

        # Folder Opening Buttons
        self.folder_button = Button(root, text="Open Folder", command=self.open_folder, bg="blue", fg="white")
        self.folder_button.place(x=900, y=350)

        # Theme Change Button
        self.theme_button = Button(root, text="Change Theme", command=self.change_theme, bg="blue", fg="white")
        self.theme_button.place(x=900, y=400)

        # Voice command button
        self.voice_button = Button(root, text="Voice Command", command=self.voice_command, bg="red", fg="white")
        self.voice_button.place(x=1050, y=800)

        # Initial voice greeting
        self.speak("Hello, I am JARVIS. How can I assist you today?")

    def update_theme(self, theme):
        # Ensure canvas exists before updating
        if hasattr(self, 'canvas'):
            self.canvas.config(bg=self.themes[theme]["bg"])
        self.root.config(bg=self.themes[theme]["bg"])

    def get_weather(self):
        api_key = "your_openweathermap_api_key"
        city = "Delhi"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        try:
            response = requests.get(url)
            weather_data = response.json()
            temp = weather_data['main']['temp']
            weather_desc = weather_data['weather'][0]['description']
            self.weather_label.config(text=f"{city}: {temp}°C, {weather_desc.capitalize()}")
        except Exception as e:
            self.weather_label.config(text="Failed to fetch weather data")

    def face_recognition(self):
        # Open the webcam and recognize faces
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.imshow('Face Recognition', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

    def open_folder(self):
        folder_path = "C:/Users/YourUsername/Documents"
        os.startfile(folder_path)

    def change_theme(self):
        self.current_theme = "dark" if self.current_theme == "blue" else "blue"
        self.update_theme(self.current_theme)

    def voice_command(self):
        # Use the custom STT module to listen for commands
        listen()
        # After listening, you can process the content of the input file
        with open('input.txt', 'r') as file:
            command = file.read().strip().lower()
            print(f"Command: {command}")
            if "change theme" in command:
                self.change_theme()
                self.speak("Theme changed.")
            elif "status" in command:
                self.speak("The system is running smoothly.")
            elif "shutdown" in command:
                self.speak("Shutting down the system.")
                self.root.quit()
            elif "cpu" in command:
                cpu_usage = psutil.cpu_percent()
                self.speak(f"Current CPU usage is {cpu_usage} percent.")
            else:
                self.speak("Sorry, I did not understand the command.")

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()


def main():
    root = tk.Tk()
    app = JarvisDashboard(root)
    root.mainloop()


if __name__ == "__main__":
    main()
