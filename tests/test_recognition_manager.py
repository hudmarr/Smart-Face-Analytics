# test_recognition_manager.py
from core.recognition_manager import RecognitionManager
import urllib.request
import os


def test_recognition_manager():
    """
    Tests the RecognitionManager by adding and recognizing a face.
    """
    manager = RecognitionManager()

    # Add a test face
    test_image_path = "sample_images/test_image.jpg"
    test_name = "Test User"
    manager.add_face(img_path=test_image_path, name=test_name)

    # Recognize the same face
    name, distance = manager.recognize_face(img_path=test_image_path)
    print(f"Recognized: {name} (Distance: {distance})")


def download_and_add_faces():
    """
    Downloads sample images and adds them to the database.
    """
    manager = RecognitionManager()

    # Define sample images and names
    images = {
        "Brad Pitt": "https://thumbs.dreamstime.com/b/brad-pitt-cannes-france-may-brad-pitt-gala-premiere-once-time-hollywood-festival-de-cannes-picture-166133619.jpg",
        "Angelina Jolie": "https://www.hollywoodreporter.com/wp-content/uploads/2023/09/GettyImages-1349503739-H-2023.jpg?w=1296&h=730&crop=1",
        "Will Smith": "https://hips.hearstapps.com/hmg-prod/images/actor-will-smith-arrives-at-the-los-angeles-world-premiere-news-photo-465783654-1565089503.jpg",
        "Shaquille O'Neal": "https://img.buzzfeed.com/buzzfeed-static/static/2021-12/5/3/asset/c2c13933c826/sub-buzz-10634-1638674991-21.jpg",
    }

    # Ensure sample_images directory exists
    os.makedirs("sample_images", exist_ok=True)

    for name, url in images.items():
        try:
            image_path = f"sample_images/{name.replace(' ', '_')}.jpg"
            print(f"Downloading {name}'s image...")
            urllib.request.urlretrieve(url, image_path)
            print(f"Adding {name} to the database...")
            manager.add_face(img_path=image_path, name=name)
        except Exception as e:
            print(f"Error adding {name}: {e}")

if __name__ == "__main__":
    #download_and_add_faces()
    test_recognition_manager()