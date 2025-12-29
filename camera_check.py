import cv2
from pupil_apriltags import Detector
import numpy as np

# --- CONFIG ---
TAG_SIZE = 0.14  # meters (length of one side of tag)
CAMERA_CALIB_FILE = "camera_params_1920x1080.npz"  # your .npz file

# Load camera intrinsics from npz
data = np.load(CAMERA_CALIB_FILE)
camera_matrix = data['cameraMatrix']     # 3x3
dist_coeffs = data['distCoeffs']         # optional
fx, fy = camera_matrix[0,0], camera_matrix[1,1]
cx, cy = camera_matrix[0,2], camera_matrix[1,2]
CAMERA_PARAMS = [fx, fy, cx, cy]

# Initialize AprilTag detector
detector = Detector(
    families='tag36h11',
    nthreads=4,
    quad_decimate=1.0,
    quad_sigma=0.0,
    refine_edges=True
)

# Open camera (replace 0 with your camera index)
cap = cv2.VideoCapture(2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect tags and estimate pose
    tags = detector.detect(
        gray,
        estimate_tag_pose=True,
        camera_params=CAMERA_PARAMS,
        tag_size=TAG_SIZE
    )

    for tag in tags:
        t = tag.pose_t
        distance = np.linalg.norm(t)  # Euclidean distance in meters
        print(f"Tag ID {tag.tag_id} distance: {distance:.3f} m")
        print('a')

        # # Draw rectangle
        corners = tag.corners.astype(int)
        for i in range(4):
            cv2.line(frame, tuple(corners[i]), tuple(corners[(i + 1) % 4]), (0,255,0), 2)
        cv2.putText(frame, f"{distance:.2f} m", tuple(corners[0]), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)

    cv2.imshow("AprilTag Distance", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
