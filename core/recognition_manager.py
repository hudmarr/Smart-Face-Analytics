import sqlite3
import numpy as np
import logging
from deepface import DeepFace
from utils.utils import serialize_embedding, deserialize_embedding, calculate_embedding_distance

class RecognitionManager:
    def __init__(self, db_path="facial_db/facial_data.db"):
        self.db_path = db_path
        self.setup_database()
        
    def setup_database(self):
        """Creates the database schema with additional fields for age and ethnicity"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                # Updated table schema to include age and ethnicity
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS faces (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        gender TEXT,
                        age INTEGER,
                        ethnicity TEXT,
                        embedding TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                conn.commit()
                logging.info("Database setup completed successfully")
        except Exception as e:
            logging.error(f"Database setup failed: {e}")
            raise

    def add_face(self, img_path, name, gender=None, age=None, ethnicity=None):
        """
        Adds a new face to the database with all attributes.
        
        Args:
            img_path (str): Path to the image file
            name (str): Name of the person
            gender (str, optional): Gender of the person
            age (int, optional): Age of the person
            ethnicity (str, optional): Ethnicity of the person
        """
        try:
            # Convert age to integer if it's provided
            age_val = int(age) if age is not None else None
            
            # Generate embedding using DeepFace
            embedding_result = DeepFace.represent(
                img_path=img_path, 
                model_name="Facenet", 
                enforce_detection=False
            )
            embedding = embedding_result[0]["embedding"]
            
            # Serialize the embedding for storage
            embedding_str = serialize_embedding(np.array(embedding))
            
            # Store in database with new fields
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO faces (name, gender, age, ethnicity, embedding)
                    VALUES (?, ?, ?, ?, ?)
                """, (name, gender, age_val, ethnicity, embedding_str))
                conn.commit()
                logging.info(f"Successfully added face for {name}")
                
        except Exception as e:
            logging.error(f"Error adding face: {e}")
            raise

    def recognize_face(self, img_path):
        """
        Recognizes a face by comparing with stored embeddings.
        We've adjusted the confidence threshold and improved the comparison logic
        for more reliable face matching.
        
        Args:
            img_path (str): Path to image file to recognize
            
        Returns:
            tuple: (name, confidence_score) of the best match
        """
        try:
            # Generate embedding for input image
            input_embedding = DeepFace.represent(
                img_path=img_path, 
                model_name="Facenet",
                enforce_detection=False
            )[0]["embedding"]
            
            # Convert input embedding to numpy array
            input_embedding = np.array(input_embedding)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name, embedding FROM faces")
                rows = cursor.fetchall()

            min_distance = float('inf')
            best_match = "Unknown"
            
            for name, embedding_str in rows:
                stored_embedding = deserialize_embedding(embedding_str)
                if stored_embedding is not None:
                    # Calculate cosine similarity instead of Euclidean distance
                    distance = 1 - np.dot(input_embedding, stored_embedding) / (
                        np.linalg.norm(input_embedding) * np.linalg.norm(stored_embedding)
                    )
                    
                    if distance < min_distance:
                        min_distance = distance
                        best_match = name

            # Adjusted confidence threshold (lower value = stricter matching)
            confidence_threshold = 0.4
            if min_distance > confidence_threshold:
                return "Unknown", None
                
            return best_match, min_distance
            
        except Exception as e:
            logging.error(f"Error during face recognition: {e}")
            return "Unknown", None

    def get_person_details(self, name):
        """
        Retrieves all stored details for a person.
        
        Args:
            name (str): Name of the person
            
        Returns:
            dict: Person's details including age, gender, and ethnicity
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT name, gender, age, ethnicity FROM faces WHERE name = ?",
                    (name,)
                )
                row = cursor.fetchone()
                
                if row:
                    return {
                        'name': row[0],
                        'gender': row[1],
                        'age': row[2],
                        'ethnicity': row[3]
                    }
                return None
                
        except Exception as e:
            logging.error(f"Error retrieving person details: {e}")
            return None