import os
import sys
import subprocess
import cv2
import numpy as np
from tqdm import tqdm
from time import sleep

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


# ==== SETTINGS ====
images_dir = "charuco_frames_1920x1080_live"               # Folder with saved frames
save_dir = "calibration_1920x1080_selected_frames"         # Folder for selected calibration images
os.makedirs(save_dir, exist_ok=True)

BOARD_ROWS = 8
BOARD_COLS = 11
SQUARE_LENGTH = 0.015  # in meters
MARKER_LENGTH = 0.011
ARUCO_DICT = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
board = aruco.CharucoBoard((BOARD_COLS, BOARD_ROWS), SQUARE_LENGTH, MARKER_LENGTH, ARUCO_DICT)


# ==== LOAD IMAGES ====
images = sorted([
    os.path.join(images_dir, f)
    for f in os.listdir(images_dir)
    if f.lower().endswith(('.png', '.jpg', '.jpeg'))
])

if not images:
    sys.exit(f"[ERROR] No images found in {images_dir}")

print(f"[INFO] Found {len(images)} frames for calibration\n")

# ==== DETECT CHARUCO CORNERS ====
all_corners = []
all_ids = []
img_size = None
valid_count = 0

for img_path in tqdm(images, desc="Detecting ChArUco corners", unit="image"):
    frame = cv2.imread(img_path)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, _ = aruco.detectMarkers(gray, ARUCO_DICT)

    if ids is not None and len(ids) > 0:
        retval, charuco_corners, charuco_ids = aruco.interpolateCornersCharuco(
            markerCorners=corners,
            markerIds=ids,
            image=gray,
            board=board
        )
        if retval is not None and retval > 22:
            all_corners.append(charuco_corners)
            all_ids.append(charuco_ids)
            if img_size is None:
                img_size = gray.shape[::-1]

            # === SAVE VALID IMAGE ===
            valid_count += 1
            filename = f"valid_{valid_count:03d}.jpg"
            cv2.imwrite(os.path.join(save_dir, filename), frame)

print(f"\n[INFO] Running calibration using {len(all_corners)} valid frames...")
print(f"[INFO] Saved {valid_count} valid images to '{save_dir}' folder.\n")


# # ==== SHOW PROGRESS BAR DURING CALIBRATION ====
# with tqdm(total=100, desc="Calibrating Camera", unit="%") as pbar:
#     for _ in range(20):  # simulate partial progress
#         sleep(0.05)
#         pbar.update(5)
#     ret, cameraMatrix, distCoeffs, rvecs, tvecs = aruco.calibrateCameraCharuco(
#         charucoCorners=all_corners,
#         charucoIds=all_ids,
#         board=board,
#         imageSize=img_size,
#         cameraMatrix=None,
#         distCoeffs=None
#     )
#     for _ in range(20, 100):
#         sleep(0.01)
#         pbar.update(1)

# # ==== RESULTS ====
# print("\n[RESULTS]")
# print("Calibration RMS error:", ret)
# print("\nCamera Matrix:\n", cameraMatrix)
# print("\nDistortion Coefficients:\n", distCoeffs.ravel())

# # ==== SAVE RESULTS ====
# np.savez("camera_calibration_charuco.npz",
#          cameraMatrix=cameraMatrix,
#          distCoeffs=distCoeffs,
#          rms_error=ret)

# print("\n[SAVED] Calibration data saved to 'camera_calibration_charuco.npz'")
