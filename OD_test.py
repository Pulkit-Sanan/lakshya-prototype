import cv2 as cv
import serial, time
import serial.serialutil
from ultralytics import YOLO

# Constants for camera
CAMERA_INDEX = 2
WIDTH, HEIGHT = None, None
C_x, C_y = None, None
SF = 0  # Serial flag

def initialize_camera(camera_index=CAMERA_INDEX):
    cap = cv.VideoCapture(camera_index)
    global WIDTH, HEIGHT, C_x, C_y
    WIDTH = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    HEIGHT = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    C_x, C_y = WIDTH // 2, HEIGHT // 2
    return cap

def initialize_serial_connection(port='COM1', baudrate=9600):
    while True:
        try:
            s_obj = serial.Serial(port, baudrate=baudrate, bytesize=8, parity='N', stopbits=1)
            return s_obj
        except serial.serialutil.SerialException as err:
            print(f"Arduino COM Not found: {err}")
            print("Retrying in 5 seconds...")
            time.sleep(5)

def process_frame(model, frame):
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

def draw_crosshairs(frame):
    cv.line(img=frame, pt1=(0, C_y), pt2=(WIDTH, C_y), color=(0, 0, 255), thickness=2, lineType=5)
    cv.line(img=frame, pt1=(C_x, 0), pt2=(C_x, HEIGHT), color=(0, 0, 255), thickness=2, lineType=5)

def calculate_differences(center_x, center_y):
    return center_x - C_x, center_y - C_y

def send_serial_command(s_obj, diff_x, diff_y):
    if abs(diff_x) < 45 and abs(diff_y) < 35:
        s_obj.write(b'0')  # Target is within range
        return
    # Determine directional command based on `diff_x` and `diff_y`
    if diff_x < 0:
        if diff_y == 0:
            s_obj.write(b'3')  # Left
        elif diff_y > 0:
            s_obj.write(b'8')  # Down-Left
        else:
            s_obj.write(b'5')  # Up-Left
    elif diff_x == 0:
        if diff_y > 0:
            s_obj.write(b'2')  # Down
        else:
            s_obj.write(b'1')  # Up
    else:
        if diff_y == 0:
            s_obj.write(b'4')  # Right
        elif diff_y > 0:
            s_obj.write(b'7')  # Down-Right
        else:
            s_obj.write(b'6')  # Up-Right

def main_loop():
    global SF
    cap = initialize_camera()
    model = YOLO('yolo11s.pt')  # Using yolo11s model for object detection
    s_obj = initialize_serial_connection()
    SF = 1  # Serial flag is set once Arduino is connected

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        draw_crosshairs(frame)

        try:
            center_x, center_y = process_frame(model, frame)
            cv.line(img=frame, pt1=(C_x, C_y), pt2=(center_x, center_y), color=(0, 255, 0), thickness=3)

            diff_x, diff_y = calculate_differences(center_x, center_y)
            if SF == 1:
                send_serial_command(s_obj, diff_x, diff_y)

            print(f"Person Bounding Box Center: ({center_x}, {center_y})")

        except IndexError as e:
            print(f"{e} - No person detected")
            if SF == 1:
                s_obj.write(b'0')

        except serial.serialutil.SerialException:
            pass

        cv.imshow('Yolov8 Inference', frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cleanup(cap, s_obj)

def cleanup(cap, s_obj):
    cap.release()
    if SF == 1:
        try:
            s_obj.close()
        except serial.serialutil.SerialException:
            pass
    cv.destroyAllWindows()

if __name__ == "__main__":
    main_loop()
