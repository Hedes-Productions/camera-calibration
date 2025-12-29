import numpy as np

# ==== USER INPUTS ====

# Example MATLAB-style camera matrix
# camera_matrix_str = "[9.989938924767152e+02,-0.315815371259140,6.447528588232972e+02;0,9.982690971513557e+02,3.497243247382249e+02;0,0,1]"

camera_matrix_str = "[1.493520768351498e+03,0,9.553083600574623e+02;0,1.492081218123735e+03,5.143161694635473e+02;0,0,1]"


# Example distortions
RadialDistortion = [0.185298868397711,-0.847346595414806,1.288810222217649]   # [k1, k2, k3]
TangentialDistortion = [0.001277286356453,-0.002126723965508]       # [p1, p2, (optional placeholder)]


# ==== PROCESSING ====

# Convert MATLAB-style string to NumPy array
camera_matrix = np.array(eval(camera_matrix_str.replace(';', '],[')))

# Combine into OpenCV-style 5-coefficient vector [k1, k2, p1, p2, k3]
distCoeffs = np.array([
    RadialDistortion[0],   # k1
    RadialDistortion[1],   # k2
    TangentialDistortion[0],  # p1
    TangentialDistortion[1],  # p2
    RadialDistortion[2]    # k3
])

# ==== SAVE TO FILE ====
np.savez("camera_params_1920x1080.npz", cameraMatrix=camera_matrix, distCoeffs=distCoeffs)

print("[INFO] Camera matrix:\n", camera_matrix)
print("[INFO] Distortion coefficients:", distCoeffs)
print("[INFO] Saved updated camera parameters to 'camera_params.npz'")
