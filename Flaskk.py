from flask import Flask, render_template
import cv2
import mediapipe as mp
import pyautogui
import pyaudio
import speech_recognition as sr
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import numpy as np
import cvzone
from pynput.keyboard import Controller

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/index.html")
def index1():
    return render_template("index.html")

@app.route("/mouse_home.html")
def mohome():
    return render_template("mouse_home.html")

@app.route("/mouse_hand.html")
def mohand():
    return render_template("mouse_hand.html")

@app.route("/mouse_eye.html")
def moeye():
    return render_template("mouse_eye.html")

@app.route("/mouse_voice.html")
def movoice():
    return render_template("mouse_voice.html")

@app.route("/keyboard_home.html")
def keyhome():
    return render_template("keyboard_home.html")

@app.route("/keyboard_hand.html")
def keyhand():
    return render_template("keyboard_hand.html")

@app.route("/empty.html")
def empty():
    cap = cv2.VideoCapture(0)
    hand_detector = mp.solutions.hands.Hands()
    drawing_utils = mp.solutions.drawing_utils
    screen_width, screen_height = pyautogui.size()
    index_y = 0
    pyautogui.FAILSAFE = False
    while True:
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        frame_height, frame_width, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = hand_detector.process(rgb_frame)
        hands = output.multi_hand_landmarks
        if hands:
            for hand in hands:
                drawing_utils.draw_landmarks(frame, hand)
                landmarks = hand.landmark
                for id, landmark in enumerate(landmarks):
                    x = int(landmark.x*frame_width)
                    y = int(landmark.y*frame_height)
                    if id == 8:
                        cv2.circle(img=frame, center=(x, y),
                        radius=10, color=(0, 255, 255))
                        index_x = screen_width/frame_width*x
                        index_y = screen_height/frame_height*y
                        pyautogui.moveTo(index_x, index_y)

                    if id == 12:
                        cv2.circle(img=frame, center=(x, y),
                        radius=10, color=(255, 0, 255))
                        m_x = screen_width/frame_width*x
                        m_y = screen_height/frame_height*y
                        print(abs(index_y - m_y))
                        if abs(index_y - m_y) < 40:
                            pyautogui.click()
                            print("Clicked")
                            print(abs(index_y - m_y))

                    if id == 4:
                        cv2.circle(img=frame, center=(x, y),
                        radius=10, color=(255, 255, 255))
                        thumb_x = screen_width/frame_width*x
                        thumb_y = screen_height/frame_height*y
                        print(abs(index_y - thumb_y))
                        if abs(index_y - thumb_y) < 70:
                            pyautogui.click(button='right')
                            print("right Click")
                            print(abs(index_y - thumb_y))

                    if id == 20:
                        cv2.circle(img=frame, center=(x, y),
                        radius=10, color=(255, 255, 0))
                        thumb_x = screen_width/frame_width*x
                        thumb_y = screen_height/frame_height*y
                        print("Double",abs(index_y - thumb_y))
                        if abs(index_y - thumb_y) > 150:
                            pyautogui.doubleClick()
                            print("double Click")
                            print(abs(index_y - thumb_y))

        cv2.imshow('Virtual Mouse', frame)
        cv2.waitKey(1)
    return render_template("empty.html")

@app.route("/empty1.html")
def empty1():
    cam = cv2.VideoCapture(0)
    face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
    screen_w, screen_h = pyautogui.size()
    pyautogui.FAILSAFE = False
    while True:
        _, frame = cam.read()
        frame = cv2.flip(frame,1)
        rgb_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        output = face_mesh.process(rgb_frame)
        landmark_points = output.multi_face_landmarks
        frame_h, frame_w, _ = frame.shape 
        cnt = 0
        if landmark_points:
            landmarks = landmark_points[0].landmark
            for id,landmark in enumerate(landmarks[474:478]):
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                print(x,y)
                cv2.circle(frame,(x,y),3,(0,255,0))
                if id == 1:
                    screen_x = int(landmark.x * screen_w)
                    screen_y = int(landmark.y * screen_h)
                    pyautogui.moveTo(screen_x,screen_y) 
            left =[landmarks[145],landmarks[159]]
            for landmark in left:
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame,(x,y),3,(0,255,255))
            l = left[0].y - left[1].y 
            print("difference = ",l)
            if l < 0.020:
                print('click')
                pyautogui.click()
                
        cv2.imshow("HEAD controlled mouse",frame)
        cv2.waitKey(1)
    return render_template("empty1.html")

@app.route("/empty2.html")
def empty2():
    cam = cv2.VideoCapture(0)
    face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
    screen_w, screen_h = pyautogui.size()
    pyautogui.FAILSAFE = False
    while True:
        _, frame = cam.read()
        frame = cv2.flip(frame,1)
        rgb_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        output = face_mesh.process(rgb_frame)
        landmark_points = output.multi_face_landmarks
        frame_h, frame_w, _ = frame.shape 
        cnt = 0
        
        listener = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                print("LISTINING")       
                listener.adjust_for_ambient_noise(source)
                voice = listener.listen(source,.25,1)
                command = str(listener.recognize_google(voice))
                print(command)
                c1 = command.lower()
                print(c1)
                if 'left' in c1 :
                    print("LEFT ClICK")
                    pyautogui.click()
                elif 'right' in c1:
                    print("RIGHT ClICK")
                    pyautogui.click(button='right')
                elif 'double' in c1 or 'click' in c1:
                    print("DOUBLE ClICK")
                    pyautogui.doubleClick()
                elif 'down' in c1:
                    print("SCROLLING DOWN")
                    pyautogui.scroll(-1500)
                elif 'up' in c1 or 'scroll' in c1:
                    print("SCROLLING UP")
                    pyautogui.scroll(1500)
                elif 'start' in c1:
                    print("WINDOWS START")
                    pyautogui.click(0,1079)
                elif 'close' in c1:
                    print("CLOSING")
                    pyautogui.click(1872,24)
                elif 'min' in c1:
                    print("MINIMIZE")
                    pyautogui.click(1776,-29) 
                elif 'add' in c1:
                    print("ADDRESS BAR")
                    pyautogui.click(258,55) 
                else:
                    pass
                    
        except:
            pass
        if landmark_points:
            landmarks = landmark_points[0].landmark
            for id,landmark in enumerate(landmarks[0:478]):
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame,(x,y),3,(0,255,0))
                if id == 1:
                    screen_x = int(landmark.x * screen_w)
                    screen_y = int(landmark.y * screen_h)
                    pyautogui.moveTo(screen_x,screen_y)
                    print("X = ",screen_x," Y = ",screen_y)
        cv2.imshow("HEAD controlled mouse",frame)
        cv2.waitKey(1)
    return render_template("empty2.html")

@app.route("/empty3.html")
def empty3():
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)
     
    detector = HandDetector(detectionCon=1)
    keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
            ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]
    finalText = ""
     
    keyboard = Controller()
     
     
    def drawAll(img, buttonList):
        for button in buttonList:
            x, y = button.pos
            w, h = button.size
            cvzone.cornerRect(img, (button.pos[0], button.pos[1], button.size[0], button.size[1]),20, rt=0)
            cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
            cv2.putText(img, button.text, (x + 20, y + 65),
                        cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
        return img
     
     

     
    class Button():
        def __init__(self, pos, text, size=[85, 85]):
            self.pos = pos
            self.size = size
            self.text = text
     
     
    buttonList = []
    for i in range(len(keys)):
        for j, key in enumerate(keys[i]):
            buttonList.append(Button([100 * j + 50, 100 * i + 50], key))
     
    while True:
        success, img = cap.read()
        img = cv2.flip(img,1)
        img = detector.findHands(img)
        lmList, bboxInfo = detector.findPosition(img)
        img = drawAll(img, buttonList)
     
        if lmList:
            for button in buttonList:
                x, y = button.pos
                w, h = button.size
     
                if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                    cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (175, 0, 175), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65),
                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    l, _, _ = detector.findDistance(8, 12, img, draw=False)
                    print(l)
     
                    ## when clicked
                    if l < 45:
                        keyboard.press(button.text)
                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + 65),
                        cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                        finalText += button.text
                        sleep(0.15)
     
        cv2.rectangle(img, (50, 350), (700, 450), (175, 0, 175), cv2.FILLED)
        cv2.putText(img, finalText, (60, 430),
        cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
     
        cv2.imshow("Image", img)
        cv2.waitKey(1)
    return render_template("empty3.html")

    

if __name__ == "__main__":
    app.run(debug=True, port=5000)