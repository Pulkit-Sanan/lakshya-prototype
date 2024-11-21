import numpy as np
import cv2 as cv
import serial
import time
import serial.serialutil
from ultralytics import YOLO

# Constants for cameras
STATIC_CAMERA_INDEX = 0
MOVABLE_CAMERA_INDEX = 1
SF = 0  # Serial flag

# Rotation and translation between cameras (assuming the cameras are in same plane)
theta = np.deg2rad(10)  # Example angle in radians
R = np.array([[np.cos(theta), -np.sin(theta), 0],
              [np.sin(theta), np.cos(theta), 0],
              [0, 0, 1]])
d = 10  # Distance between cameras in meters (only x axis, can be changed to both axis)
T = np.array([d, 0, 0])

#intrinsics for both cameras (focal length and principal point, process of calculating these values is in instrinsics.md)

# Intrinsics for both cameras
fx_static, fy_static, cx_static, cy_static = 800, 800, 640, 480  # Example values for static camera
INTRINSICS_STATIC = np.array([[fx_static, 0, cx_static],
                              [0, fy_static, cy_static],
                              [0, 0, 1]])

fx_movable, fy_movable, cx_movable, cy_movable = 800, 800, 640, 480  # Example values for movable camera
INTRINSICS_MOVABLE = np.array([[fx_movable, 0, cx_movable],
                               [0, fy_movable, cy_movable],
                               [0, 0, 1]])

def initialize_camera(camera_index):
    cap = cv.VideoCapture(camera_index)
    width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    C_x, C_y = width // 2, height // 2
    return cap, width, height, C_x, C_y

def initialize_serial_connection(port='COM5', baudrate=9600):
    while True:
        try:
            s_obj = serial.Serial(port, baudrate=baudrate, bytesize=8, parity='N', stopbits=1)
            return s_obj
        except serial.serialutil.SerialException as err:
            print(f"Arduino COM Not found: {err}")
            print("Retrying in 5 seconds...")
            time.sleep(5)

def process_frame_object_detection(model, frame):
    results = model.predict(frame, save=True, conf=0.8)
    if results:
        for bbox in results[0].boxes:
            if bbox.cls == 0:  # 'person' class in YOLO models typically has class index 0
                x_center, y_center, width, height = bbox.xywh[0]
                x1 = int(x_center - width / 2)
                y1 = int(y_center - height / 2)
                x2 = int(x_center + width / 2)
                y2 = int(y_center + height / 2)
                
                # Draw the bounding box
                cv.rectangle(frame, (x1, y1), (x2, y2), color=(0, 255, 0), thickness=2)
                
                # Draw the center point of the bounding box
                cv.circle(frame, (int(x_center), int(y_center)), radius=5, color=(0, 255, 0), thickness=-1)
                
                return int(x_center), int(y_center)
    raise IndexError("No person detected.")

def process_frame_pose_detection(model, frame):
    results = model.predict(frame, save=True, conf=0.8)
    if results:
        # Keypoints are stored in results[0].keypoints.xy[0], each keypoint corresponds to a body part
        keypoints = results[0].keypoints.xy[0]
        
        # Assuming keypoints[0] is the first keypoint (e.g., nose or center of the body)
        x, y = int(keypoints[0][0]), int(keypoints[0][1])
        
        # Optionally, you can draw keypoints for visualization
        for kp in keypoints:
            cv.circle(frame, (int(kp[0]), int(kp[1])), radius=5, color=(0, 0, 255), thickness=-1)
        
        return x, y
    raise IndexError("No keypoints detected.")



def project_to_3d(bbox_center, intrinsics, depth):
    x_normalized = (bbox_center[0] - intrinsics[0, 2]) / intrinsics[0, 0]
    y_normalized = (bbox_center[1] - intrinsics[1, 2]) / intrinsics[1, 1]
    point_3d = np.array([x_normalized * depth, y_normalized * depth, depth])
    return point_3d

def transform_to_movable_camera(point_3d, rotation_matrix, translation_vector):
    transformed_point = rotation_matrix @ point_3d + translation_vector
    return transformed_point

def reproject_to_image_plane(point_3d, intrinsics):
    point_2d = intrinsics @ point_3d
    point_2d /= point_2d[2]
    return int(point_2d[0]), int(point_2d[1])

def draw_crosshairs(frame, C_x, C_y):
    cv.line(img=frame, pt1=(0, C_y), pt2=(frame.shape[1], C_y), color=(0, 0, 255), thickness=2, lineType=5)
    cv.line(img=frame, pt1=(C_x, 0), pt2=(C_x, frame.shape[0]), color=(0, 0, 255), thickness=2, lineType=5)

def calculate_differences(center_x, center_y, C_x, C_y):
    return center_x - C_x, center_y - C_y

def send_serial_command(s_obj, diff_x, diff_y):
    if abs(diff_x) < 45 and abs(diff_y) < 35:
        s_obj.write(b'0')
        return
    # Determine directional command based on `diff_x` and `diff_y`
    if diff_x < 0:
        if diff_y == 0:
            s_obj.write(b'3')
        elif diff_y > 0:
            s_obj.write(b'8')
        else:
            s_obj.write(b'5')
    elif diff_x == 0:
        if diff_y > 0:
            s_obj.write(b'2')
        else:
            s_obj.write(b'1')
    else:
        if diff_y == 0:
            s_obj.write(b'4')
        elif diff_y > 0:
            s_obj.write(b'7')
        else:
            s_obj.write(b'6')

def main_loop():
    global SF
    static_cap, STATIC_WIDTH, STATIC_HEIGHT, STATIC_C_x, STATIC_C_y = initialize_camera(STATIC_CAMERA_INDEX)
    movable_cap, MOVABLE_WIDTH, MOVABLE_HEIGHT, MOVABLE_C_x, MOVABLE_C_y = initialize_camera(MOVABLE_CAMERA_INDEX)
    
    model = YOLO('yolo11s.pt')  # YOLO model for object detection
    pose_model = YOLO('yolo11s-pose.pt')  # YOLO model for pose detection
    s_obj = initialize_serial_connection()
    SF = 1

    while static_cap.isOpened() and movable_cap.isOpened():
        success, static_frame = static_cap.read()
        _, movable_frame = movable_cap.read()
        if not success:
            break

        draw_crosshairs(movable_frame, MOVABLE_C_x, MOVABLE_C_y)

        try:
            # Phase 1: Align Bounding Box Center

            # 1. Process the static camera frame to find the person (object detection)
            static_center_x, static_center_y = process_frame_object_detection(model, static_frame)
            depth = 1000  # Replace with actual depth value if available
            point_3d_static = project_to_3d((static_center_x, static_center_y), INTRINSICS_STATIC, depth)
            point_3d_movable = transform_to_movable_camera(point_3d_static, R, T)
            movable_target_x, movable_target_y = reproject_to_image_plane(point_3d_movable, INTRINSICS_MOVABLE)

            # 2. Draw the transformed target on the movable frame
            cv.circle(movable_frame, (movable_target_x, movable_target_y), radius=5, color=(0, 255, 0), thickness=-1)
            cv.line(movable_frame, (MOVABLE_C_x, MOVABLE_C_y), (movable_target_x, movable_target_y), (0, 255, 0), 2)

            # 3. Send serial command to align the movable camera to the transformed bounding box center
            diff_x, diff_y = movable_target_x - MOVABLE_C_x, movable_target_y - MOVABLE_C_y
            send_serial_command(s_obj, diff_x, diff_y)

            # Phase 2: Align with Keypoint
            # 4. Process the movable camera frame using the pose model to get keypoints (pose detection)
            x_p, y_p = process_frame_pose_detection(pose_model, movable_frame)

            # 5. Align the camera with the keypoint (typically keypoints[0] for the nose)
            diff_x_keypoint, diff_y_keypoint = x_p - MOVABLE_C_x, y_p - MOVABLE_C_y
            send_serial_command(s_obj, diff_x_keypoint, diff_y_keypoint)

            print(f"Transformed Bounding Box Center for Movable Camera: ({movable_target_x}, {movable_target_y})")
            print(f"Keypoint Position: ({x_p}, {y_p})")

        except IndexError as e:
            print(f"{e} - No detection found")
            if SF == 1:
                s_obj.write(b'0')

        except serial.serialutil.SerialException:
            pass

        cv.imshow('Static Camera Inference', static_frame)
        cv.imshow('Movable Camera Alignment', movable_frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    cleanup(static_cap, movable_cap, s_obj)


def cleanup(static_cap, movable_cap, s_obj):
    static_cap.release()
    movable_cap.release()
    if SF == 1:
        try:
            s_obj.close()
        except serial.serialutil.SerialException:
            pass
    cv.destroyAllWindows()

if __name__ == "__main__":
    main_loop()
