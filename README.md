# Camera Calibration with DroidCam and MATLAB

This project provides a step-by-step guide to calibrate a camera using DroidCam, Python, and MATLAB for tag detection purposes.

---

## Prerequisites

- Python 3.x
- MATLAB with Image Processing and Computer Vision Toolbox
- DroidCam installed on your PC and mobile device
- Other python packages needed to run the project

---

## Project Files and Their Usages

- **cam_index_check.py** – Can be used to test if the camera setup is working properly.
- **camera_check_with_apriltags.py** – Can test AprilTag detection with the `.npz` file containing the required camera calibration parameters.
- **valid_frames_selector.py** – Can be used to select valid frames after getting the camera frames folder created by `main.py`.
- **main.py** – Used to record and save the appropriate camera frames via Charuco Board calibration.
- **npz_file_creator.py** – Generate a npz file by given camera parameters.

---

## Setup and Calibration Steps

### 1. Open DroidCam Client
- Launch the DroidCam client on your PC.
- Check the resolution under **Sources** and **File > Settings > Video > Base resolution**.

### 2. Download or Clone the Repository
```bash
git clone <repository-url>
```

### 3. Generate a Charuco Board
- Open the Charuco Board generator: [Charuco Board Generator](https://calib.io/pages/camera-calibration-pattern-generator?srsltid=AfmBOorgefTk7QRn33_Bgg6dpJQEoleuVLC4ZGda5_mW3_0RMg54qUKe)

### 4. Capture Camera Frames
- Run `main.py` in the downloaded project.
- Move your camera and save frames (they will be automatically saved).
- **Note:** Ensure parameters such as resolution, number of columns and rows, and time intervals in the code are correct.

### 5. Filter Camera Frames
- Run `valid_frames_selector.py`.
- This will filter out low-quality frames and save the selected frames in a new folder.
- **Note:** Check parameters in the script before running.

### 6. Calibrate Camera in MATLAB
1. Open MATLAB.
2. Go to the **Apps** section at the top.
3. Launch the **Camera Calibrator** app under Image Processing and Computer Vision.
4. Click **Add Images** and select the folder containing the filtered camera frames.
5. In **Options**, select **3 Coefficients** and **Tangential Distortion**.
6. Click **Calibrate**.
7. Review the graph of image frames vs. error.
8. Use the red slider to select poorly predicted frames.
9. Right-click on the left panel containing the frames and select **Remove** to discard low-quality frames.
10. Repeat recalibration until pixel error is around **0.4 – 0.7**.

### 7. Export Camera Parameters
- Export camera parameters to the workspace.
- Copy the intrinsic matrix `k`, radial distortion, and tangential distortion parameters.
- Paste them into the appropriate sections of `npz_file_creator.py` in the project.

### 8. Generate NPZ File
- Run `npz_file_creator.py`.
- The script will generate a `.npz` file containing the camera matrix and other parameters required for tag detection.

---

## Notes
- Ensure all parameters (resolution, board size, etc.) are correctly set in the scripts.
- Calibration might need several iterations to achieve an acceptable pixel error.



