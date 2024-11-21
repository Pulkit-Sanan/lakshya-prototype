import os
import cv2
import numpy as np
import pickle

CHECKERBOARD = (7, 9)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Prepare object points
objp = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[0, :, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)

# Function to calibrate a camera and save parameters
def calibrate_camera(image_dir, output_file):
    objpoints = []  # 3D points in real world space
    imgpoints = []  # 2D points in image plane

    # List all files in the directory and filter for .jpg files
    images = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.endswith('.jpg')]

    if not images:
        print(f"No images found in the directory: {image_dir}")
        return

    last_valid_img = None
    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, 
                                                 cv2.CALIB_CB_ADAPTIVE_THRESH + 
                                                 cv2.CALIB_CB_FAST_CHECK + 
                                                 cv2.CALIB_CB_NORMALIZE_IMAGE)

        if ret:
            last_valid_img = img
            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)

    if last_valid_img is None:
        print(f"No valid chessboard images detected in directory: {image_dir}")
        return

    h, w = last_valid_img.shape[:2]
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, (w, h), None, None)

    print("Camera matrix : \n", mtx)
    print("dist : \n", dist)
    print("rvecs : \n", rvecs)
    print("tvecs : \n", tvecs)

    # Save calibration parameters to a pickle file
    with open(output_file, 'wb') as f:
        pickle.dump({'mtx': mtx, 'dist': dist, 'rvecs': rvecs, 'tvecs': tvecs}, f)

    print(f"Camera parameters saved to {output_file}")

# Calibrate both cameras and save parameters
calibrate_camera(r'C:\Users\pulki\Desktop\lakshya-prototype\sample_workflow\samb_logi', r'C:\Users\pulki\Desktop\lakshya-prototype\sample_workflow\dump\movable_camera_params.pkl')
calibrate_camera(r'C:\Users\pulki\Desktop\lakshya-prototype\sample_workflow\yash_logi',  r'C:\Users\pulki\Desktop\lakshya-prototype\sample_workflow\dump\static_camera_params.pkl')
