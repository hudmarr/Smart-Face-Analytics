# test_main_application.py
from core.main_application import MainApplication

def test_main_application():
    """
    Tests the MainApplication by running the real-time face recognition system.
    """
    app = MainApplication()
    print("Running the main application for testing. Press 'q' to quit.")
    app.run()

if __name__ == "__main__":
    test_main_application()
