import tkinter as tk
from tkinter import ttk, messagebox
import cv2
import os
import numpy as np
from datetime import datetime
from PIL import Image, ImageTk
from core.main_application import MainApplication
from core.recognition_manager import RecognitionManager
import logging

class FaceRecognitionUI:
    def __init__(self):
        """Initialize the main UI window"""
        self.root = tk.Tk()
        self.root.title("Face Recognition System")
        self.root.geometry("500x300")
        self.root.configure(bg="#2C2F33")
        self.setup_main_screen()
        
    def setup_main_screen(self):
        """Set up the main menu screen"""
        # Title Label
        title_label = tk.Label(
            self.root, 
            text="Face Recognition System",
            font=("Helvetica", 18, "bold"),
            fg="white",
            bg="#2C2F33"
        )
        title_label.pack(pady=20)

        # Start Recognition Button
        start_button = tk.Button(
            self.root,
            text="Start Recognition System",
            font=("Helvetica", 14),
            bg="#7289DA",
            fg="white",
            command=self.start_recognition,
            height=2,
            width=20
        )
        start_button.pack(pady=10)

        # Add Person Button
        add_person_button = tk.Button(
            self.root,
            text="Add Person",
            font=("Helvetica", 14),
            bg="#99AAB5",
            fg="black",
            command=self.open_add_person,
            height=2,
            width=20
        )
        add_person_button.pack(pady=10)

        # Quit Button
        quit_button = tk.Button(
            self.root,
            text="Quit",
            font=("Helvetica", 14),
            bg="#F04747",
            fg="white",
            command=self.quit_application,
            height=2,
            width=20
        )
        quit_button.pack(pady=10)

    def start_recognition(self):
        """Start the recognition system"""
        self.root.withdraw()  # Hide main window
        app = MainApplication()
        app.run()
        self.root.deiconify()  # Show main window again when recognition is closed

    def open_add_person(self):
        """Open the Add Person window"""
        self.root.withdraw()  # Hide main window
        add_person_window = AddPersonWindow(self)
        add_person_window.run()

    def quit_application(self):
        """Clean up and quit the application"""
        self.root.quit()

    def run(self):
        """Start the UI main loop"""
        self.root.mainloop()

class AddPersonWindow:
    def __init__(self, main_ui):
        self.main_ui = main_ui
        self.window = tk.Toplevel()
        self.window.title("Add New Person")
        self.window.geometry("400x500")  # Made taller for new fields
        self.window.configure(bg="#2C2F33")
        self.setup_ui()
        self.capture = None

    def setup_ui(self):
        """Set up the Add Person UI elements"""
        # Title
        title_label = tk.Label(
            self.window,
            text="Add New Person",
            font=("Helvetica", 16, "bold"),
            fg="white",
            bg="#2C2F33"
        )
        title_label.pack(pady=10)

        # Name Entry
        name_label = tk.Label(
            self.window,
            text="Name",
            font=("Helvetica", 12),
            fg="white",
            bg="#2C2F33"
        )
        name_label.pack(pady=5)
        self.name_entry = tk.Entry(
            self.window,
            font=("Helvetica", 12),
            width=30
        )
        self.name_entry.pack(pady=5)

        # Age Entry
        age_label = tk.Label(
            self.window,
            text="Age",
            font=("Helvetica", 12),
            fg="white",
            bg="#2C2F33"
        )
        age_label.pack(pady=5)
        self.age_entry = tk.Entry(
            self.window,
            font=("Helvetica", 12),
            width=30
        )
        self.age_entry.pack(pady=5)

        # Gender Dropdown
        gender_label = tk.Label(
            self.window,
            text="Gender",
            font=("Helvetica", 12),
            fg="white",
            bg="#2C2F33"
        )
        gender_label.pack(pady=5)
        self.gender_var = tk.StringVar()
        gender_dropdown = ttk.Combobox(
            self.window,
            textvariable=self.gender_var,
            font=("Helvetica", 12),
            state="readonly"
        )
        gender_dropdown["values"] = ["Male", "Female", "Non-binary", "Other"]
        gender_dropdown.pack(pady=5)

        # Ethnicity Dropdown (matching DeepFace options)
        ethnicity_label = tk.Label(
            self.window,
            text="Ethnicity",
            font=("Helvetica", 12),
            fg="white",
            bg="#2C2F33"
        )
        ethnicity_label.pack(pady=5)
        self.ethnicity_var = tk.StringVar()
        ethnicity_dropdown = ttk.Combobox(
            self.window,
            textvariable=self.ethnicity_var,
            font=("Helvetica", 12),
            state="readonly"
        )
        ethnicity_dropdown["values"] = [
            "Asian",
            "Indian", 
            "Black", 
            "White", 
            "Middle Eastern", 
            "Latino Hispanic"
        ]
        ethnicity_dropdown.pack(pady=5)

        # Submit Button
        submit_button = tk.Button(
            self.window,
            text="Start Camera",
            font=("Helvetica", 12),
            bg="#7289DA",
            fg="white",
            command=self.start_camera
        )
        submit_button.pack(pady=10)

        # Back Button
        back_button = tk.Button(
            self.window,
            text="Back",
            font=("Helvetica", 12),
            bg="#F04747",
            fg="white",
            command=self.go_back
        )
        back_button.pack(pady=10)

    def start_camera(self):
        """Validate inputs and start the camera"""
        # Validate required fields
        if not self.name_entry.get():
            messagebox.showerror("Error", "Please enter a name")
            return
            
        if not self.age_entry.get().isdigit():
            messagebox.showerror("Error", "Please enter a valid age")
            return

        if not self.gender_var.get():
            messagebox.showerror("Error", "Please select a gender")
            return

        if not self.ethnicity_var.get():
            messagebox.showerror("Error", "Please select an ethnicity")
            return

        self.window.withdraw()
        self.capture = cv2.VideoCapture(0)
        
        # Set camera properties for better color
        self.capture.set(cv2.CAP_PROP_AUTO_WB, 0.5)  # Adjust white balance
        self.capture.set(cv2.CAP_PROP_BRIGHTNESS, 150)  # Adjust brightness
        self.capture.set(cv2.CAP_PROP_CONTRAST, 150)  # Adjust contrast
        
        self.show_camera_window()

    def show_camera_window(self):
        """Show the camera window with capture button"""
        camera_window = tk.Toplevel()
        camera_window.title("Capture Photo")
        camera_window.geometry("800x700")  # Made taller for the button

        # Create frame for video
        video_frame = tk.Frame(camera_window, bg="black")
        video_frame.pack(pady=20)

        # Create label for video
        self.video_label = tk.Label(video_frame, bg="black")
        self.video_label.pack()

        # Create a styled capture button
        capture_button = tk.Button(
            camera_window,
            text="Capture Photo",
            font=("Helvetica", 16, "bold"),
            bg="white",
            fg="black",
            relief=tk.RAISED,
            width=20,
            height=2,
            command=lambda: self.capture_photo(camera_window)
        )
        capture_button.pack(pady=20)

        def update_frame():
            ret, frame = self.capture.read()
            if ret:
                # Apply color corrections
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Add color balance correction
                frame = cv2.addWeighted(
                    frame, 1.1,  # Increase contrast slightly
                    np.zeros(frame.shape, frame.dtype), 0,
                    -10  # Reduce brightness slightly
                )
                
                # Resize for display
                frame = cv2.resize(frame, (640, 480))
                
                # Convert to PhotoImage
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                
                # Update label
                self.video_label.configure(image=imgtk)
                self.video_label.image = imgtk
                
            camera_window.after(10, update_frame)

        update_frame()

    def capture_photo(self, camera_window):
        """Capture and save the photo"""
        ret, frame = self.capture.read()
        if ret:
            # Create directory if it doesn't exist
            if not os.path.exists("captured_faces"):
                os.makedirs("captured_faces")

            # Save image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_path = f"captured_faces/{self.name_entry.get()}_{timestamp}.jpg"
            cv2.imwrite(image_path, frame)

            # Save to database using RecognitionManager
            manager = RecognitionManager()
            manager.add_face(
                img_path=image_path,
                name=self.name_entry.get(),
                gender=self.gender_var.get(),
                age=self.age_entry.get(),
                ethnicity=self.ethnicity_var.get()
            )

            # Show success message
            messagebox.showinfo(
                "Success",
                "Photo captured and saved successfully!"
            )

            # Cleanup and return to main menu
            self.cleanup_camera()
            camera_window.destroy()
            self.window.destroy()
            self.main_ui.root.deiconify()

    def cleanup_camera(self):
        """Clean up camera resources"""
        if self.capture is not None:
            self.capture.release()
            cv2.destroyAllWindows()

    def go_back(self):
        """Return to main menu"""
        self.cleanup_camera()
        self.window.destroy()
        self.main_ui.root.deiconify()

    def run(self):
        """Start the Add Person window"""
        self.window.mainloop()

if __name__ == "__main__":
    ui = FaceRecognitionUI()
    ui.run()