# add_face_ui.py
import cv2
import logging
from core.recognition_manager import RecognitionManager
import tkinter as tk
from tkinter import ttk

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class AddFaceUI:
    """
    Provides a user interface for adding new faces to the database.
    """

    def __init__(self):
        """
        Initializes the AddFaceUI.
        """
        self.recognition_manager = RecognitionManager()
        self.video_capture = cv2.VideoCapture(0)  # Use webcam
        logging.info("AddFaceUI initialized.")

    def capture_face(self, name, gender, race):
        """
        Captures a face from the webcam and adds it to the database.

        Args:
            name (str): Name of the person to associate with the captured face.
            gender (str): Gender of the person.
            race (str): Race of the person.
        """
        try:
            logging.info(f"Capturing face for {name}...")
            while True:
                ret, frame = self.video_capture.read()
                if not ret:
                    logging.error("Error reading frame from webcam.")
                    break

                # Display the frame
                cv2.imshow("Capture Face", frame)

                # Capture face on 'c' key press
                if cv2.waitKey(1) & 0xFF == ord('c'):
                    # Save the captured frame as an image
                    image_path = f"captured_faces/{name}.jpg"
                    cv2.imwrite(image_path, frame)
                    logging.info(f"Face captured and saved as {image_path}.")

                    # Add the face to the database
                    self.recognition_manager.add_face(img_path=image_path, name=name, gender=gender, race=race)
                    break

                # Exit on 'q' key press
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        except Exception as e:
            logging.error(f"Error capturing face: {e}")
        finally:
            self.video_capture.release()
            cv2.destroyAllWindows()

    def open_ui(self):
        """
        Opens a UI to enter details and start the capture process.
        """
        root = tk.Tk()
        root.title("Add New Person")
        root.geometry("400x300")
        root.configure(bg="#2C2F33")

        # Title
        title_label = tk.Label(root, text="Add New Person", font=("Helvetica", 16, "bold"), fg="white", bg="#2C2F33")
        title_label.pack(pady=10)

        # Name Entry
        name_label = tk.Label(root, text="Name", font=("Helvetica", 12), fg="white", bg="#2C2F33")
        name_label.pack(pady=5)
        name_entry = tk.Entry(root, font=("Helvetica", 12), width=30)
        name_entry.pack(pady=5)

        # Gender Dropdown
        gender_label = tk.Label(root, text="Gender", font=("Helvetica", 12), fg="white", bg="#2C2F33")
        gender_label.pack(pady=5)
        gender_var = tk.StringVar()
        gender_dropdown = ttk.Combobox(root, textvariable=gender_var, font=("Helvetica", 12), state="readonly")
        gender_dropdown["values"] = ["Male", "Female", "Non-binary", "Other"]
        gender_dropdown.pack(pady=5)

        # Race Dropdown
        race_label = tk.Label(root, text="Race", font=("Helvetica", 12), fg="white", bg="#2C2F33")
        race_label.pack(pady=5)
        race_var = tk.StringVar()
        race_dropdown = ttk.Combobox(root, textvariable=race_var, font=("Helvetica", 12), state="readonly")
        race_dropdown["values"] = ["Asian", "Black", "White", "Hispanic", "Other"]
        race_dropdown.pack(pady=5)

        # Submit Button
        def submit():
            name = name_entry.get()
            gender = gender_var.get()
            race = race_var.get()
            if name:
                root.destroy()
                self.capture_face(name=name, gender=gender, race=race)
            else:
                logging.error("Name is required to add a person.")

        submit_button = tk.Button(root, text="Submit", font=("Helvetica", 12), bg="#7289DA", fg="white", command=submit)
        submit_button.pack(pady=10)

        root.mainloop()

if __name__ == "__main__":
    add_face_ui = AddFaceUI()
    add_face_ui.open_ui()
