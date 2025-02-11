# database_utils.py
import sqlite3
import logging
from utils import serialize_embedding, deserialize_embedding

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def initialize_database(db_path):
    """
    Initializes the SQLite database for storing facial data.

    Args:
        db_path (str): Path to the SQLite database file.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS faces (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                embedding TEXT NOT NULL
            )
            """
        )
        conn.commit()
        conn.close()
        logging.info("Database initialized successfully.")
    except Exception as e:
        logging.error(f"Error initializing database: {e}")

def add_face_to_database(db_path, name, embedding):
    """
    Adds a new face to the database.

    Args:
        db_path (str): Path to the SQLite database file.
        name (str): Name of the person.
        embedding (numpy.ndarray): Facial embedding of the person.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        embedding_str = serialize_embedding(embedding)
        cursor.execute("INSERT INTO faces (name, embedding) VALUES (?, ?)", (name, embedding_str))
        conn.commit()
        conn.close()
        logging.info(f"Added {name} to the database.")
    except Exception as e:
        logging.error(f"Error adding face to database: {e}")

def fetch_all_faces(db_path):
    """
    Fetches all faces and embeddings from the database.

    Args:
        db_path (str): Path to the SQLite database file.

    Returns:
        list: A list of tuples containing names and embeddings.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name, embedding FROM faces")
        rows = cursor.fetchall()
        conn.close()

        # Deserialize embeddings
        faces = [(name, deserialize_embedding(embedding)) for name, embedding in rows]
        return faces
    except Exception as e:
        logging.error(f"Error fetching faces from database: {e}")
        return []

def find_closest_match(db_path, embedding):
    """
    Finds the closest match for a given embedding in the database.

    Args:
        db_path (str): Path to the SQLite database file.
        embedding (numpy.ndarray): The embedding to match.

    Returns:
        tuple: The name of the closest match and the distance, or ("Unknown", None) if no match is found.
    """
    try:
        faces = fetch_all_faces(db_path)
        min_distance = float("inf")
        closest_name = "Unknown"

        for name, db_embedding in faces:
            if db_embedding is not None:
                distance = calculate_distance(embedding, db_embedding)
                if distance < min_distance:
                    min_distance = distance
                    closest_name = name

        return closest_name, min_distance
    except Exception as e:
        logging.error(f"Error finding closest match: {e}")
        return "Unknown", None
