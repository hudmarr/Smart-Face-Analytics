import os
import sys
import logging
from utils.logging_utils import setup_logging
from ui.ui import FaceRecognitionUI

def main():
    """
    Main entry point for the face recognition application.
    Sets up logging and launches the main UI.
    """
    try:
        # Ensure all required directories exist
        os.makedirs('logs', exist_ok=True)
        os.makedirs('captured_faces', exist_ok=True)
        
        # Set up logging first
        setup_logging()
        
        # Log application start
        logging.info("Starting Face Recognition System")
        
        # Initialize and run the UI
        ui = FaceRecognitionUI()
        ui.run()
        
    except Exception as e:
        logging.error(f"Application error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()