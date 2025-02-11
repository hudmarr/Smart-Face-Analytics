# config.py
class Config:
    """
    Configuration class for the face recognition project.
    """
    # Database configuration
    DATABASE_PATH = "facial_db/facial_data.db"

    # DeepFace settings
    MODEL_NAME = "Facenet"
    DETECTOR_BACKEND = "opencv"

    # Video settings
    CAMERA_INDEX = 0  # Default camera index
    FRAME_ANALYSIS_INTERVAL = 0.5  # Interval for detailed face analysis (in seconds)

    # Logging settings
    LOG_LEVEL = "INFO"

    @staticmethod
    def print_config():
        """
        Prints the current configuration.
        """
        print("Configuration:")
        print(f"DATABASE_PATH: {Config.DATABASE_PATH}")
        print(f"MODEL_NAME: {Config.MODEL_NAME}")
        print(f"DETECTOR_BACKEND: {Config.DETECTOR_BACKEND}")
        print(f"CAMERA_INDEX: {Config.CAMERA_INDEX}")
        print(f"FRAME_ANALYSIS_INTERVAL: {Config.FRAME_ANALYSIS_INTERVAL}")
        print(f"LOG_LEVEL: {Config.LOG_LEVEL}")