import numpy as np
import cv2 as cv
from ultralytics import YOLO
import pickle

# Load YOLO model
model = YOLO('yolo11s.pt')  # Replace with your YOLO model
STATIC_CAMERA_INDEX = 2 # yash webcam
MOVABLE_CAMERA_INDEX = 1 # samb webcam

# Load camera calibration parameters from pickle files
def load_camera_params(file):
    with open(file, 'rb') as f:
        params = pickle.load(f)
    return params['mtx'], params['dist']

# Load parameters for both cameras
camera_matrix_static, dist_static = load_camera_params(r'C:\Users\pulki\Desktop\lakshya-prototype\sample_workflow\dump\static_camera_params.pkl')
camera_matrix_movable, dist_movable = load_camera_params(r'C:\Users\pulki\Desktop\lakshya-prototype\sample_workflow\dump\movable_camera_params.pkl')

# Distance between cameras in centimeters
translation_vector = np.array([20, 0, 0]) / 100.0  # Convert to meters

# Undistortion function
def undistort_frame(frame, camera_matrix, dist_coeffs):
    h, w = frame.shape[:2]
    new_camera_matrix, roi = cv.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (w, h), 1, (w, h))
    undistorted_frame = cv.undistort(frame, camera_matrix, dist_coeffs, None, new_camera_matrix)
    return undistorted_frame

# Project to 3D (fixed depth)
def project_to_3d_fixed_depth(bbox_center, intrinsics, depth=1.0):
    x_normalized = (bbox_center[0] - intrinsics[0, 2]) / intrinsics[0, 0]
    y_normalized = (bbox_center[1] - intrinsics[1, 2]) / intrinsics[1, 1]
    point_3d = np.array([x_normalized * depth, y_normalized * depth, depth])
    return point_3d

# Transform 3D point to movable camera
def transform_to_movable_camera(point_3d, translation_vector):
    transformed_point = point_3d + translation_vector
    return transformed_point

# Reproject to 2D
def reproject_to_image_plane(point_3d, intrinsics):
    point_2d = intrinsics @ point_3d
    point_2d /= point_2d[2]
    return int(point_2d[0]), int(point_2d[1])

# Process frame with YOLO and get bounding box
def process_frame(model, frame):
    results = model.predict(frame, save=True, conf=0.8)
    if results:
        for bbox in results[0].boxes:
            if bbox.cls == 0:  # Person class
                x_min, y_min, x_max, y_max = map(int, bbox.xyxy[0])
                x_center, y_center = (x_min + x_max) // 2, (y_min + y_max) // 2
                return (x_center, y_center), (x_min, y_min, x_max, y_max)
    return None, None

# Initialize cameras
cap_static = cv.VideoCapture(STATIC_CAMERA_INDEX)  
cap_movable = cv.VideoCapture(MOVABLE_CAMERA_INDEX)  

while cap_static.isOpened() and cap_movable.isOpened():
    ret_static, static_frame = cap_static.read()
    ret_movable, movable_frame = cap_movable.read()
    if not ret_static or not ret_movable:
        break

    # Undistort frames
    static_frame = undistort_frame(static_frame, camera_matrix_static, dist_static)
    movable_frame = undistort_frame(movable_frame, camera_matrix_movable, dist_movable)

    # Detect object in internal camera feed
    bbox_center, bbox_coords = process_frame(model, static_frame)
    if bbox_center and bbox_coords:
        print(f"Bounding box center (static camera): {bbox_center}")
        
        # Draw bounding box in static camera frame
        cv.rectangle(static_frame, bbox_coords[:2], bbox_coords[2:], (0, 255, 0), 2)

        # Estimate 3D coordinates
        depth = 2  # Assume fixed depth
        point_3d_static = project_to_3d_fixed_depth(bbox_center, camera_matrix_static, depth)
        
        # Transform to movable camera
        point_3d_movable = transform_to_movable_camera(point_3d_static, translation_vector)
        
        # Reproject to 2D
        movable_bbox_center = reproject_to_image_plane(point_3d_movable, camera_matrix_movable)
        print(f"Bounding box center (movable camera): {movable_bbox_center}")
        
        # Draw the transformed bounding box
        cv.circle(movable_frame, movable_bbox_center, radius=15, color=(0, 255, 0), thickness=-1)

    # Display both camera feeds
    cv.imshow('Static Camera', static_frame)
    cv.imshow('Movable Camera', movable_frame)

    # Break on 'q' key
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap_static.release()
cap_movable.release()
cv.destroyAllWindows()
