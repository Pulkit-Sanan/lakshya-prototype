import cv2 as cv
import serial, time
import serial.serialutil
first = time.time()
from ultralytics import YOLO

cap = cv.VideoCapture(1)
WIDTH = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
C_x = WIDTH//2
HEIGHT = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
C_y = HEIGHT//2
SF=0

while(True):
    try:
        s_obj = serial.Serial('COM1')
        s_obj.baudrate = 9600  # set Baud rate to 9600
        s_obj.bytesize = 8   # Number of data bits = 8
        s_obj.parity  ='N'   # No parity
        s_obj.stopbits = 1
        SF=1
        break
    except serial.serialutil.SerialException as err:
        print("Arduino COM Not found on ??", err)
        print("Trying again in 5 seconds")
        time.sleep(5);

model = YOLO('yolov8n-pose.pt')

while cap.isOpened():
    success, frame = cap.read()

    if success:
        results = model.predict(frame, save=True, conf=0.8)
        #annotated_frame = results[0].plot()
        cv.line(img=frame, pt1=(0, C_y), pt2=(WIDTH, C_y), color=(0, 0, 255), thickness=2, lineType=5, shift=0)
        cv.line(img=frame, pt1=(C_x, 0), pt2=(C_x, HEIGHT), color=(0, 0, 255), thickness=2, lineType=5, shift=0)
        print('------------------------------------')
        try:
            iter_r = [int(_) for _ in results[0].keypoints.xy[0][0]]
            if(iter_r==[0, 0]):
                if(SF==1):
                    s_obj.write(b'0')
                raise IndexError("Some problem")
            print(f'result={iter_r}\n')
            cv.line(img=frame, pt1=(C_x, C_y), pt2=iter_r, color=(0, 255, 0), thickness=3, lineType=8, shift=0)
        
            x_p = iter_r[0]
            y_p = iter_r[1]
            diff_x = x_p-C_x
            diff_y = y_p-C_y
            if(SF==1):
                if(abs(diff_x)<45 and abs(diff_y)<35):
                    s_obj.write(b'0')
                    raise serial.serialutil.SerialException
                if(diff_x<0):
                    if(diff_y==0):
                        s_obj.write(b'3')
                    elif(diff_y>0):
                        s_obj.write(b'8')
                    else:
                        s_obj.write(b'5')
                elif(diff_x==0):
                    if(diff_y==0):
                        s_obj.write(b'0')
                    elif(diff_y>0):
                        s_obj.write(b'2')
                    else:
                        s_obj.write(b'1')
                else:
                    if(diff_y==0):
                        s_obj.write(b'4')
                    elif(diff_y>0):
                        s_obj.write(b'7')
                    else:
                        s_obj.write(b'6')    

        except IndexError as e:
            print(str(e), "\nNothing Detected")
        except serial.serialutil.SerialException:
                pass
        print('------------------------------------')
        cv.imshow('Yolov8 Inference', frame)
        if cv.waitKey(1) & 0xFF==ord('q'):
            break
    else:
        break

if(SF==1):
    try:
        s_obj.close()
    except serial.serialutil.SerialException:
        pass
cap.release()
cv.destroyAllWindows()
