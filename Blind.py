import speech_recognition as sr
import pyttsx3
import pyaudio
import pyttsx3
from time import sleep

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
while True:
    command = input("enter the character :")
    print(command)
    engine.say(command)
    engine.runAndWait()
    sleep(1)
    if command == 'quit':
        break