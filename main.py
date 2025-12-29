import os
import sys
import subprocess
import cv2
import numpy as np
from tqdm import tqdm

# ==== AUTO-INSTALL DEPENDENCIES ====
def ensure_package(pkg):
    try:
        __import__(pkg)
    except ImportError:
        print(f"[INFO] Installing missing package: {pkg} ...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

ensure_package("tqdm")

try:
    import cv2.aruco as aruco
except ImportError:
    print("[INFO] Installing required library: opencv-contrib-python...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "opencv-contrib-python"])
    import cv2.aruco as aruco


# ==== USER SETTINGS ====
output_dir = "charuco_frames_1920x1080_live"
save_interval = 1                   # Save every Nth valid frame (1 = all valid)
min_corners_detected = 20           # Minimum number of visible ChArUco corners
min_coverage_ratio = 0.05           # Rough board coverage threshold
show_preview = True                 # Show detection preview while recording
max_frames = 20000                  # Safety limit

# ==== CHARUCO BOARD DEFINITION ====
BOARD_ROWS = 8
BOARD_COLS = 11
SQUARE_LENGTH = 0.015
MARKER_LENGTH = 0.011
ARUCO_DICT = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

board = aruco.CharucoBoard(
    (BOARD_COLS, BOARD_ROWS),
    SQUARE_LENGTH,
    MARKER_LENGTH,
    ARUCO_DICT
)

# ==== SETUP CAMERA WITH FORCED RESOLUTION ====
# Try default webcam index 0; if that’s not DroidCam, try index 1 or 2.
cap = cv2.VideoCapture(2)  # Use DirectShow backend on Windows

# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# Verify resolution
ret, frame = cap.read()
if not ret:
    sys.exit("[ERROR] Cannot grab frame from DroidCam. Make sure it's running.")
print(f"[INFO] Captured frame resolution: {frame.shape[1]}x{frame.shape[0]}")

if not cap.isOpened():
    sys.exit("[ERROR] Cannot open DroidCam. Make sure it's running and selected as a webcam device.")

os.makedirs(output_dir, exist_ok=True)
print("[INFO] Press 'q' to quit.\n")

frame_idx = 0
saved_idx = 0

with tqdm(total=max_frames, desc="Capturing", unit="frame") as pbar:
    while frame_idx < max_frames:
        ret, frame = cap.read()
        if not ret:
            print("[WARN] Frame grab failed.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = aruco.detectMarkers(gray, ARUCO_DICT)

        if ids is not None and len(ids) > 0:
            aruco.refineDetectedMarkers(gray, board, corners, ids, rejectedCorners=None)

            retval, charuco_corners, charuco_ids = aruco.interpolateCornersCharuco(
                markerCorners=corners,
                markerIds=ids,
                image=gray,
                board=board
            )

            if retval is not None and retval >= min_corners_detected:
                all_pts = np.concatenate(corners, axis=1).reshape(-1, 2)
                x_min, y_min = np.min(all_pts, axis=0)
                x_max, y_max = np.max(all_pts, axis=0)
                bbox_area = (x_max - x_min) * (y_max - y_min)
                frame_area = frame.shape[0] * frame.shape[1]
                coverage_ratio = bbox_area / frame_area

                if coverage_ratio > min_coverage_ratio:
                    # Save this frame
                    if saved_idx % save_interval == 0:
                        filename = os.path.join(output_dir, f"frame_{frame_idx:05d}.png")
                        cv2.imwrite(filename, frame)
                        tqdm.write(f"[SAVED] {filename} ({int(retval)} corners, coverage={coverage_ratio:.2f})")
                    saved_idx += 1

                    # Draw detections
                    if show_preview:
                        aruco.drawDetectedMarkers(frame, corners, ids)
                        if charuco_corners is not None:
                            for p in charuco_corners:
                                cv2.circle(frame, tuple(np.int32(p[0])), 3, (0, 255, 0), -1)

        # Show frame and handle quit
        if show_preview:
            cv2.putText(frame, f"Frame {frame_idx} | Saved: {saved_idx}",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            cv2.imshow("ChArUco Live Capture (DroidCam)", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_idx += 1
        pbar.update(1)

cap.release()
cv2.destroyAllWindows()
print(f"\n[DONE] {saved_idx} good ChArUco frames saved in '{output_dir}'.")
