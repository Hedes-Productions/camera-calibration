import cv2
import numpy as np

cap = cv2.VideoCapture(2)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)


if not cap.isOpened():
    print("Cannot open camera")
    exit()

frame_count = 0  # to save multiple frames if needed

while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame. Exiting ...")
        break

    # Optional: save the frame for inspection
    if frame_count < 1:  # save only the first frame
        cv2.imwrite("test_frame_4k.png", frame)
        print(f"Saved frame shape: {frame.shape}")
        frame_count += 1

    cv2.imshow('OBS Live Feed', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
