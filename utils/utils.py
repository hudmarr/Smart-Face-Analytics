import json
import numpy as np
import base64
import logging

def serialize_embedding(embedding):
    """
    Serializes a numpy array embedding into a string for database storage.
    Uses base64 encoding to ensure safe storage of binary data.
    
    Args:
        embedding (numpy.ndarray): The facial embedding to serialize
        
    Returns:
        str: Base64 encoded string representation of the embedding
    """
    try:
        # Convert numpy array to bytes
        embedding_bytes = embedding.tobytes()
        
        # Encode as base64 string
        embedding_b64 = base64.b64encode(embedding_bytes).decode('utf-8')
        
        # Create a JSON object with the shape and data
        embedding_dict = {
            'shape': embedding.shape,
            'dtype': str(embedding.dtype),
            'data': embedding_b64
        }
        
        return json.dumps(embedding_dict)
    except Exception as e:
        logging.error(f"Error serializing embedding: {e}")
        return None

def deserialize_embedding(embedding_str):
    """
    Deserializes a string back into a numpy array embedding.
    
    Args:
        embedding_str (str): The serialized embedding string
        
    Returns:
        numpy.ndarray: The deserialized embedding array
    """
    try:
        # Parse the JSON string
        embedding_dict = json.loads(embedding_str)
        
        # Decode the base64 data
        embedding_bytes = base64.b64decode(embedding_dict['data'])
        
        # Reconstruct the numpy array
        embedding = np.frombuffer(
            embedding_bytes, 
            dtype=np.dtype(embedding_dict['dtype'])
        ).reshape(embedding_dict['shape'])
        
        return embedding
    except Exception as e:
        logging.error(f"Error deserializing embedding: {e}")
        return None

def calculate_embedding_distance(embedding1, embedding2):
    """
    Calculates the Euclidean distance between two facial embeddings.
    
    Args:
        embedding1 (numpy.ndarray): First embedding
        embedding2 (numpy.ndarray): Second embedding
        
    Returns:
        float: Euclidean distance between the embeddings
    """
    try:
        return np.linalg.norm(embedding1 - embedding2)
    except Exception as e:
        logging.error(f"Error calculating distance: {e}")
        return float('inf')