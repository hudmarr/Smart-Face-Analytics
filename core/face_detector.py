import cv2
from deepface import DeepFace

def detect_faces(frame, detector_backend="opencv"):
    """
    Detects faces in a given frame and returns the frame with bounding boxes drawn around the faces.

    Args:
        frame (numpy.ndarray): The input frame (image) in which to detect faces.
        detector_backend (str): The backend to use for face detection. Default is "opencv".

    Returns:
        tuple: A tuple containing:
            - frame (numpy.ndarray): The frame with bounding boxes drawn around detected faces.
            - face_objs (list): A list of dictionaries containing information about each detected face.
    """
    try:
        # Detect and extract faces from the frame using DeepFace
        face_objs = DeepFace.extract_faces(img_path=frame, detector_backend=detector_backend, enforce_detection=False)

        # Draw bounding boxes around detected faces
        for face_obj in face_objs:
            facial_area = face_obj["facial_area"]
            x, y, w, h = facial_area["x"], facial_area["y"], facial_area["w"], facial_area["h"]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Draw green bounding box

        return frame, face_objs

    except Exception as e:
        print(f"Error detecting faces: {e}")
        return frame, []


def test_face_detector():
    """
    Tests the face detector with a live webcam feed.
    """
    # Initialize video capture
    video_capture = cv2.VideoCapture(0)  # Use default webcam

    if not video_capture.isOpened():
        print("Error: Could not open webcam.")
        return

    print("Press 'q' to quit...")

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        # Detect faces in the frame
        frame_with_faces, face_objs = detect_faces(frame)

        # Display the frame with bounding boxes
        cv2.imshow("Face Detector", frame_with_faces)

        # Print the number of faces detected
        print(f"Detected {len(face_objs)} face(s).")

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture and close windows
    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # Test the face detector
    test_face_detector()