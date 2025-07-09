from re import X
import cv2
import numpy as np
import time
import math
from djitellopy import Tello
from pyimagesearch.pid import PID
from keyboard_djitellopy import keyboard


# Import object detection related code
from models.experimental import attempt_load
from utils.datasets import letterbox
from utils.general import non_max_suppression_kpt, scale_coords
from utils.plots import plot_one_box
from torchvision import transforms
from numpy import random
import torch

WEIGHT = './best.pt'
device = "cuda" if torch.cuda.is_available() else "cpu"

model = attempt_load(WEIGHT, map_location=device)
if device == "cuda":
    model = model.half().to(device)
else:
    model = model.float().to(device)
names = model.module.names if hasattr(model, 'module') else model.names
colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]

states = {
    'melody': False,
    'cana': False
}


def detect_objects(image):
    image_orig = image.copy()
    image = letterbox(image, (640, 640), stride=64, auto=True)[0]
    if device == "cuda":
        image = transforms.ToTensor()(image).to(device).half().unsqueeze(0)
    else:
        image = transforms.ToTensor()(image).to(device).float().unsqueeze(0)

    with torch.no_grad():
        output = model(image)[0]
    output = non_max_suppression_kpt(output, conf_thres=0.25, iou_thres=0.65)[0]
    label = ""
    conf = 0
    # Draw label and confidence on the image
    output[:, :4] = scale_coords(image.shape[2:], output[:, :4], image_orig.shape).round()
    for *xyxy, conf, cls in output:
        label = f'{names[int(cls)]} {conf:.2f}'
        plot_one_box(xyxy, image_orig, label=label, color=colors[int(cls)], line_thickness=1)

    return image_orig, label, conf


def main():
    drone = Tello()
    drone.connect()
    drone.streamon()
    frame_read = drone.get_frame_read()
    
    dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
    parameters = cv2.aruco.DetectorParameters_create()

    fs = cv2.FileStorage('calibration_parameters.xml', cv2.FILE_STORAGE_READ)
    intrinsic = fs.getNode("intrinsic").mat()
    distortion = fs.getNode("distortion").mat()
    fs.release()
    x_pid = PID(kP=0.7, kI=0.0001, kD=0.1)
    z_pid = PID(kP=0.7, kI=0.0001, kD=0.1)
    y_pid = PID(kP=0.7, kI=0.0001, kD=0.1)
    yaw_pid = PID(kP=0.7, kI=0.0001, kD=0.1)
    x_pid.initialize()
    yaw_pid.initialize()
    z_pid.initialize()
    y_pid.initialize()  # Fixed the typo here
    max_speed_threshold = 40
    state = -1
    state0 = 0
    movestate = 0
    dool = 0
    back=1
    matx = [0,0,2,2,4,2]
    maty = [0,2,0,4,2,2]
    while True:
        frame = frame_read.frame
        cv2.imshow("", frame)
        markerCorners, markerids, rejectedCandidates = cv2.aruco.detectMarkers(frame, dictionary, parameters=parameters)
        if (markerids is not None and state == 0) or (markerids is not None and state == 2):
            rvec, tvec, _objPoints = cv2.aruco.estimatePoseSingleMarkers(markerCorners, 15, intrinsic, distortion)
            
            for i in range(rvec.shape[0]):
                rot = np.zeros(shape=(3, 3))
                cv2.Rodrigues(rvec[i], rot, jacobian=0)
                ypr = cv2.RQDecomp3x3(rot)[0]
                yaw_update = ypr[1]*1.4
                if abs(tvec[0,0,0]) < 10 and abs(tvec[0,0,1]) < 10 and tvec[0,0,2] < 70 and state==0:
                    drone.send_rc_control(0, 0, 0, 0)
                    movestate = 0
                    state0 = 1
                    state = state + 1
                    drone.move_up(20)
                    time.sleep(1)
                if  tvec[0,0,2] > 60 and tvec[0,0,2] < 70 and state==2:#右轉
                    drone.rotate_clockwise(90)
                    state0 = 1
                    state = state + 1
                x_update = tvec[0, 0, 0]
                print("org_x: " + str(x_update))
                x_update = x_pid.update(x_update, sleep=0)  
                print("pid_x: " + str(x_update))

                y_update = -(tvec[0, 0, 1])
                print("org_y: " + str(y_update))
                y_update = y_pid.update(y_update, sleep=0)  
                print("pid_y: " + str(y_update))

                z_update = tvec[0, 0, 2] -50
                print("org_z: " + str(z_update))
                z_update = z_pid.update(z_update, sleep=0)
                print("pid_z: " + str(z_update))

                # x:left_right z: forward_back y: up_down yaw: y_rotare 
                if x_update > max_speed_threshold:
                    x_update = max_speed_threshold
                elif x_update < -max_speed_threshold:
                    x_update = -max_speed_threshold

                if y_update > max_speed_threshold:
                    y_update = max_speed_threshold
                elif y_update < -max_speed_threshold:
                    y_update = -max_speed_threshold

                if z_update > max_speed_threshold:
                    z_update = max_speed_threshold
                elif z_update < -max_speed_threshold:
                    z_update = -max_speed_threshold
                
                yaw_update = math.degrees(math.atan2(tvec[0,0,0],tvec[0,0,2]))
                # yaw_update = yaw_pid.update(yaw_update, sleep=0)
                if yaw_update > max_speed_threshold:
                    yaw_update = max_speed_threshold
                elif yaw_update < -max_speed_threshold:
                    yaw_update = -max_speed_threshold
                    
                print(tvec[0, 0, 0], tvec[0, 0, 1], tvec[0, 0, 2])
                print(x_update, y_update, z_update, yaw_update)
                if x_update>0:
                    x_update=x_update*2
                drone.send_rc_control(int(x_update), int(z_update*0.8), int(y_update*1.5), 0)
                state0 = 0
                frame = cv2.aruco.drawDetectedMarkers(frame, markerCorners, markerids)
                frame = cv2.aruco.drawAxis(frame, intrinsic, distortion, rvec[i, :, :], tvec[i, :, :], 10)

                middle = (markerCorners[0][0][0] + markerCorners[0][0][2]) // 2
                middle -= (100, 50)
                middle = tuple(middle)
                cv2.putText(frame, f"x: {tvec[0, 0, 0]: .3f}, y: {tvec[0, 0, 1]: .3f}, z: {tvec[0, 0, 2]: .3f}", middle,
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 1, cv2.LINE_AA)
        elif (state == 0 and state0==0) or (state == 2 and state0==0) or (state == 4 and state0==0):
            state0=1
            drone.send_rc_control(0, 0, 0, 0)
        elif state == 1:
            grayframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            ret, grayframe = cv2.threshold(grayframe, 40, 255, cv2.THRESH_BINARY)
            cv2.imshow("bw",grayframe)
            mat = np.zeros((5,5), dtype=int)
            times0=0
            times1=0
            for i in range(0,6):
                sumi=matx[i]*144
                for ii in range(0,12):
                    sumj=maty[i]*192
                    for jj in range(0,16):
                        mat[matx[i]][maty[i]]=mat[matx[i]][maty[i]]+grayframe[sumi][sumj]
                        sumj=sumj+12
                    sumi=sumi+12
            sum=mat[0][0]+mat[0][2]+mat[2][0]+mat[2][2]+mat[2][4]+mat[4][2]
            if sum<1020 and back>0:
                back=0
                print("toob")
                drone.move_back(30)
            elif sum>293505 and back>0:
                back=0
                print("toow")
                drone.move_back(30)
            elif movestate == 0:
                if mat[0][2]-10200>mat[2][0]:
                    print("movestate=0")
                    drone.send_rc_control(0, 0, 0, 0)
                    drone.move_left(20)
                    movestate = movestate + 1
                    state0=1
                else:
                    print("movestate=0")
                    drone.send_rc_control(0, 0, 18, 0)
                    state0=0
            elif movestate == 1:
                if dool == 1:
                    if mat[0][2]<mat[0][0]-10200:
                        print("movestate=1")
                        drone.send_rc_control(0, 0, 0, 0)
                        drone.move_up(20)
                        movestate = movestate + 1
                        dool = 3
                        state0=1
                    else:
                        print("movestate=1")
                        drone.send_rc_control(-8, 0, 0, 0)
                        state0=0
                else:
                    drone.move_left(100)
                    movestate = movestate + 1
            elif dool == 3:
                if mat[0][2]-10200>mat[2][0]:
                    print("dool=3")
                    drone.send_rc_control(0, 0, 0, 0)
                    drone.move_left(20)
                    dool = dool + 1
                    state0=1
                else:
                    print("dool=3")
                    drone.send_rc_control(0, 0, 18, 0)
                    state0=0
            elif dool == 4:
                if mat[4][2]<mat[2][0]-10200:
                    print("dool=4")
                    drone.send_rc_control(0, 0, 0, 0)
                    drone.move_down(20)
                    dool = dool + 1
                    state0=1
                else:
                    print("dool=4")
                    drone.send_rc_control(-8, 0, 0, 0)
                    state0=0
            elif dool == 5:
                if mat[4][2]-10200>mat[2][0]:
                    print("dool=5")
                    drone.send_rc_control(0, 0, 0, 0)
                    drone.move_left(20)
                    dool = dool + 1
                    state0=1
                else:
                    print("dool=5")
                    drone.send_rc_control(0, 0, -18, 0)
                    state0=0
            elif movestate == 2:
                if mat[4][2]<mat[2][0]-10200:
                    print("movestate=2")
                    drone.send_rc_control(0, 0, 0, 0)
                    drone.move_down(60)
                    movestate = movestate + 1
                    state0=1
                else:
                    print("movestate=2")
                    drone.send_rc_control(-8, 0, 0, 0)
                    state0=0
            elif movestate == 3:
                if mat[4][2]-10200>mat[2][0]:
                    print("movestate=3")
                    drone.send_rc_control(0, 0, 0, 0)
                    drone.move_back(30)
                    drone.move_left(100)
                    drone.move_forward(25)
                    movestate = movestate + 1
                    state0=1
                else:
                    print("movestate=3")
                    drone.send_rc_control(0, 0, -18, 0)
                    state0=0
            elif movestate == 4:
                if mat[0][2]<mat[2][0]-10200:
                    print("movestate=4")
                    drone.send_rc_control(0, 0, 0, 0)
                    drone.move_up(20)
                    movestate = movestate + 1
                    state0=1
                else:
                    print("movestate=4")
                    drone.send_rc_control(-8, 0, 0, 0)
                    state0=0
            elif movestate == 5:
                if mat[0][2]-10200>mat[2][0]:
                    print("movestate=5")
                    drone.send_rc_control(0, 0, 0, 0)
                    drone.move_left(20)
                    movestate = movestate + 1
                    state0=1
                else:
                    print("movestate=5")
                    drone.send_rc_control(0, 0, 18, 0)
                    state0=0
            elif movestate == 6:
                if dool == 2:
                    if mat[0][2]<mat[0][0]-10200:
                        print("movestate=6")
                        drone.send_rc_control(0, 0, 0, 0)
                        movestate = movestate + 1
                        dool = 3
                        state0=1
                    else:
                        print("movestate=6")
                        drone.send_rc_control(-8, 0, 0, 0)
                        state0=0
                else:
                    drone.move_left(100)
                    movestate = movestate + 1
            elif movestate == 7:
                if state0==1:
                    drone.send_rc_control(-8, 0, 0, 0)
                    state0=0
                markerCorners, markerids, rejectedCandidates = cv2.aruco.detectMarkers(frame, dictionary, parameters=parameters)
                if markerids is not None:
                    drone.move_back(70)
                    state = 2
        elif state == -1:#感測娃娃
            if states['melody'] == False and states['cana'] == False:
                detected_frame, label, conf = detect_objects(frame)
                if label:
                    print(label)
                if label.startswith('melody') and conf>0.3:
                    states['melody'] = True
                    states['cana'] = False
                    print("Entering Melody State")
                    dool = 1
                    state+=1
                    # Perform actions for Melody State

                elif label.startswith('cana') and conf>0.3:
                    states['melody'] = False
                    states['cana'] = True
                    print("Entering Cana State")
                    dool = 2
                    state+=1
                    # Perform actions for Cana State

            #     cv2.imshow("Detected Objects", detected_frame)
            # elif states['melody'] == True and states['cana'] == False:
            #     cv2.imshow("", frame)
            # elif states['melody'] == False and states['cana'] == True:
            #     cv2.imshow("", frame)
            # Display the frame with object detection results
        elif state == 3:#感測人臉
            drone.move_right(200)
            time.sleep(3)
            drone.move_forward(240)
            drone.rotate_counter_clockwise(180)
            drone.send_rc_control(0, 0, 0, 0)
            drone.move_right(60)
            time.sleep(3)
            state = state+1
            drone.land()
        key = cv2.waitKey(1)
        if key != -1:
            keyboard(drone, key)
            if key == ord('1'):
                state = -1
                state0 = 0
                movestate = 0
                dool = 1
                back=1
                drone.move_up(20)
                drone.move_forward(180)

if __name__ == "__main__":
    main()
