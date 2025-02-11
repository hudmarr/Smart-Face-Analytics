import cv2

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Webcam could not be initialized.")
else:
    print("Webcam initialized successfully. Press 'q' to quit.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame.")
        break

    cv2.imshow("Webcam Test", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
