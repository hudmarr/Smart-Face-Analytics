import cv2
import time
import logging
import os
import numpy as np
from deepface import DeepFace
from core.recognition_manager import RecognitionManager

class MainApplication:
    def __init__(self):
        """
        Initialize the main application components.
        Sets up the video capture, recognition manager, and display settings.
        """
        # Initialize core components
        self.recognition_manager = RecognitionManager()
        self.video_capture = cv2.VideoCapture(0)
        self.last_analysis_time = time.time()
        
        # Set up display settings
        self.font = cv2.FONT_HERSHEY_DUPLEX  # More modern looking font
        
        # Verify camera is working
        if not self.video_capture.isOpened():
            raise RuntimeError("Could not start camera capture")

    def analyze_face(self, frame):
        """
        Analyzes facial features in a given frame using DeepFace.
        
        Args:
            frame: The video frame to analyze
            
        Returns:
            dict: Analysis results including age, gender, race, and emotion
                 or None if analysis fails
        """
        try:
            analysis = DeepFace.analyze(
                img_path=frame,
                actions=['age', 'gender', 'race', 'emotion'],
                enforce_detection=False,
                silent=True
            )
            return analysis[0] if analysis else None
        except Exception as e:
            logging.error(f"Error in face analysis: {e}")
            return None

    def format_gender_probability(self, analysis):
        """
        Formats the gender prediction to show only the dominant gender.
        
        Args:
            analysis (dict): The face analysis results
            
        Returns:
            str: Formatted gender string with probability
        """
        if 'gender' in analysis and isinstance(analysis['gender'], dict):
            woman_prob = analysis['gender'].get('Woman', 0)
            man_prob = analysis['gender'].get('Man', 0)
            
            if woman_prob > man_prob:
                return f"Gender: Female ({woman_prob:.2f}%)"
            else:
                return f"Gender: Male ({man_prob:.2f}%)"
        return "Gender: Unknown"

    def draw_text_with_background(self, frame, text, position, scale=0.6, color=(255, 255, 0)):
        """
        Draws text with a semi-transparent background for better visibility.
        
        Args:
            frame: The frame to draw on
            text: Text to display
            position: (x, y) coordinates
            scale: Font scale factor
            color: Text color in BGR format
        """
        # Calculate text dimensions
        (text_width, text_height), baseline = cv2.getTextSize(
            text, self.font, scale, 1  # Reduced thickness for measurement
        )
        
        # Calculate background rectangle dimensions
        padding = 5
        bg_rect_pt1 = (position[0], position[1] - text_height - padding)
        bg_rect_pt2 = (position[0] + text_width + padding, position[1] + padding)
        
        # Draw semi-transparent background
        overlay = frame.copy()
        cv2.rectangle(overlay, bg_rect_pt1, bg_rect_pt2, (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
        
        # Draw text with reduced thickness
        cv2.putText(
            frame,
            text,
            position,
            self.font,
            scale,
            color,
            1,  # Reduced thickness for cleaner text
            cv2.LINE_AA  # Anti-aliasing for smoother text
        )

    def run(self):
        try:
            while True:
                ret, frame = self.video_capture.read()
                if not ret:
                    continue

                current_time = time.time()
                if current_time - self.last_analysis_time >= 0.5:
                    try:
                        faces = DeepFace.extract_faces(
                            img_path=frame,
                            enforce_detection=False
                        )
                        
                        for face in faces:
                            facial_area = face['facial_area']
                            x = facial_area['x']
                            y = facial_area['y']
                            w = facial_area['w']
                            h = facial_area['h']

                            # Draw rectangle around face
                            cv2.rectangle(
                                frame,
                                (x, y),
                                (x + w, y + h),
                                (0, 255, 0),
                                2
                            )

                            face_region = frame[y:y+h, x:x+w]
                            temp_path = "temp_face.jpg"
                            cv2.imwrite(temp_path, face_region)
                            
                            name, confidence = self.recognition_manager.recognize_face(temp_path)
                            analysis = self.analyze_face(frame)
                            
                            if analysis:
                                line_height = 25
                                
                                if name != "Unknown":
                                    # Person is recognized - show both stored and predicted data
                                    person_details = self.recognition_manager.get_person_details(name)
                                    if person_details:
                                        # Calculate positions for side-by-side display above head
                                        left_section_x = x - w//2  # Left section starts half face width to the left
                                        right_section_x = x + w//2  # Right section starts half face width to the right
                                        text_y_start = y - 120  # Start height above head
                                        
                                        # Left side - Stored Information (Green)
                                        stored_info = [
                                            f"Stored Data:",
                                            f"Name: {person_details['name']}",
                                            f"Age: {person_details['age']}",
                                            f"Gender: {person_details['gender']}",
                                            f"Ethnicity: {person_details['ethnicity'].title()}"
                                        ]
                                        
                                        for i, text in enumerate(stored_info):
                                            self.draw_text_with_background(
                                                frame, 
                                                text,
                                                (left_section_x, text_y_start + (i * line_height)),
                                                color=(0, 255, 0)
                                            )

                                        # Right side - Predictions (Yellow)
                                        predictions = [
                                            "Predictions:",
                                            f"Age: {analysis['age']:.0f}",
                                            f"Gender: {self.format_gender_probability(analysis)}",
                                            f"Race: {analysis['dominant_race'].title()}",
                                            f"Emotion: {analysis['dominant_emotion'].title()}"
                                        ]
                                        
                                        for i, text in enumerate(predictions):
                                            self.draw_text_with_background(
                                                frame,
                                                text,
                                                (right_section_x, text_y_start + (i * line_height)),
                                                color=(255, 255, 0)
                                            )
                                else:
                                    # Unknown person - show only predictions centered above head
                                    text_y_start = y - 120
                                    center_x = x + w//4  # Center the text above the face
                                    
                                    predictions = [
                                        f"Age: {analysis['age']:.0f}",
                                        f"Gender: {self.format_gender_probability(analysis)}",
                                        f"Race: {analysis['dominant_race'].title()}",
                                        f"Emotion: {analysis['dominant_emotion'].title()}"
                                    ]
                                    
                                    for i, text in enumerate(predictions):
                                        self.draw_text_with_background(
                                            frame,
                                            text,
                                            (center_x, text_y_start + (i * line_height)),
                                            color=(255, 255, 0)
                                        )

                    except Exception as e:
                        logging.error(f"Error in face detection: {e}")

                    self.last_analysis_time = current_time

                cv2.imshow('Face Recognition System', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        finally:
            if os.path.exists("temp_face.jpg"):
                os.remove("temp_face.jpg")
            self.video_capture.release()
            cv2.destroyAllWindows()

def test_main_application():
    """
    Test function to run the main application.
    """
    app = MainApplication()
    app.run()

if __name__ == "__main__":
    test_main_application()