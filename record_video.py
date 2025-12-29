import cv2
import os

# ==== USER SETTINGS ====
output_dir = "recorded_video"
os.makedirs(output_dir, exist_ok=True)

video_filename = os.path.join(output_dir, "droidcam_recording.mp4")
frame_width = 1280         # Adjust depending on your DroidCam resolution
frame_height = 720
fps = 20                  # Frames per second
record_seconds = 60       # Optional: duration of recording, or press 'q' to stop

# ==== SETUP VIDEO CAPTURE ====
# 0 = default webcam; if DroidCam app is running, it usually registers as a webcam
cap = cv2.VideoCapture(0)  

if not cap.isOpened():
    print("[ERROR] Cannot open webcam. Make sure DroidCam is running.")
    exit()

# Optional: set resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

# ==== SETUP VIDEO WRITER ====
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # For MP4
out = cv2.VideoWriter(video_filename, fourcc, fps, (frame_width, frame_height))

print("[INFO] Press 'q' to stop recording...")

frame_count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        print("[ERROR] Failed to grab frame")
        break

    out.write(frame)  # Save frame to video
    cv2.imshow("DroidCam Recording", frame)
    frame_count += 1

    # Stop if user presses 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # # Optional: stop after fixed duration
    # if fps * record_seconds > 0 and frame_count >= fps * record_seconds:
    #     break

cap.release()
out.release()
cv2.destroyAllWindows()
print(f"[DONE] Video saved as {video_filename}")
