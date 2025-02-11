import os
import logging
from datetime import datetime

def setup_logging():
    """
    Sets up logging configuration for the application.
    Creates necessary directories and configures log formatting and handling.
    """
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    os.makedirs(logs_dir, exist_ok=True)

    # Configure log file path with timestamp
    timestamp = datetime.now().strftime('%Y%m%d')
    log_file = os.path.join(logs_dir, f'app_{timestamp}.log')

    # Set up logging configuration
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            # File handler with daily rotation
            logging.FileHandler(log_file),
            # Console handler for immediate feedback
            logging.StreamHandler()
        ]
    )

    logging.info('Logging system initialized')