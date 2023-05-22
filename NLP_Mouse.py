import cv2
import mediapipe as mp
import pyautogui
import speech_recognition as sr


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
        for id,landmark in enumerate(landmarks[0:478]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame,(x,y),3,(0,255,0))
            if id == 1:
                screen_x = int(landmark.x * screen_w)
                screen_y = int(landmark.y * screen_h)
                pyautogui.moveTo(screen_x,screen_y)
                print(screen_x,screen_y)
    cv2.imshow("HEAD controlled mouse",frame)
    cv2.waitKey(1)
    
    listener = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("listing")       
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source,.25,1)
            command = str(listener.recognize_google(voice))
            print(command)
            c1 = command.lower()
            print(c1)
            if 'left' in c1 :
                print("left click")
                pyautogui.click()
            elif 'right' in c1:
                print("right clcik")
                pyautogui.click(button='right')
            elif 'double' in c1 or 'click' in c1:
                print("Double click")
                pyautogui.doubleClick()
            elif 'down' in c1:
                print("scrolling down")
                pyautogui.scroll(-1500)
            elif 'up' in c1 or 'scroll' in c1:
                print("scrolling up")
                pyautogui.scroll(1500)
            elif 'start' in c1:
                print("closing..")
                pyautogui.click(0,1079)
            elif 'close' in c1:
                print("closing..")
                pyautogui.click(1872,24)
            elif 'min' in c1:
                print("Minimize")
                pyautogui.click(1776,-29) 
            elif 'add' in c1:
                print("Address bar")
                pyautogui.click(258,55) 
            else:
                pass
                
    except:
        pass
