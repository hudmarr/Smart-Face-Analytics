# test_face_detector.py
import cv2
from core.face_detector import detect_faces
import urllib.request
import os

# Define URL of a test image
image_url = "https://img.freepik.com/free-photo/woman-home_144627-28149.jpg"
image_path = "sample_images/test_image.jpg"

# Create the sample_images directory if it doesn't exist
os.makedirs(os.path.dirname(image_path), exist_ok=True)

# Download the image
if not os.path.exists(image_path):
    print(f"Downloading test image from {image_url}...")
    urllib.request.urlretrieve(image_url, image_path)
    print(f"Test image saved to {image_path}.")


def test_detect_faces():
    """
    Tests the detect_faces function with a sample image.
    """
    test_image_path = "sample_images/test_image.jpg"
    frame = cv2.imread(test_image_path)

    if frame is None:
        print("Test image not found.")
        return

    frame_with_faces, face_objs = detect_faces(frame)

    print(f"Number of faces detected: {len(face_objs)}")
    for idx, face_obj in enumerate(face_objs):
        print(f"Face {idx + 1}: {face_obj}")

if __name__ == "__main__":
    test_detect_faces()