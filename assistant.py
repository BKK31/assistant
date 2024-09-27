import subprocess
import wolframalpha
import pyttsx3
import tkinter
import json
import random
import operator
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os

# import winshell # For windows
import shutil  # For Linux machines
import pyjokes
import feedparser
import smtplib
import ctypes
import time
import requests
from twilio.rest import Client
from clint.textui import progress
from ecapture import ecapture as ec
from bs4 import BeautifulSoup
import sys
import google.generativeai as Genai

# import win32com.client as wincl
from urllib.request import urlopen

api_key = ""
Genai.configure(api_key=api_key)

model = Genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=Genai.GenerationConfig(
        max_output_tokens=2048,
        temperature=0.7,
    ),
)

assistant = "Veda 1 point o"

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe(assistant):
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        print("Good Morning Sir !")
        speak("Good Morning Sir !")
    elif hour >= 12 and hour < 18:
        print("Good Afternoon Sir !")
        speak("Good Afternoon Sir !")
    else:
        print("Good Evening Sir !")
        speak("Good Evening Sir !")

    assname = assistant
    print("I am your Assistant")
    speak("I am your Assistant")
    print(assname)
    speak(assname)


def load_username():
    try:
        with open("username.txt", "r") as file:
            uname = file.read().strip()
            return uname
    except FileNotFoundError:
        return None


def save_username(uname):
    with open("username.txt", "w") as file:
        file.write(uname)


def ask_username():
    print("What should I call you, sir?")
    speak("What should I call you, sir?")
    uname = takeCommand()
    print(f"Welcome Mister {uname}\nHow can I help you?")
    speak(f"Welcome Mister {uname}")
    speak("How can I help you?")
    save_username(uname)
    return uname


def takeCommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}\n")

        except Exception as e:
            print(e)
            print("Unable to Recognize your voice.")
            return "None"

    return query


def sendEmail(to, content):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()

    # Enable low security in gmail
    server.login("your email id", "your email password")
    server.sendmail("your email id", to, content)
    server.close()


if __name__ == "__main__":
    clear = lambda: os.system("cls")

    clear()
    wishMe(assistant)
    uname = load_username()
    if uname is None:
        uname = ask_username()
    else:
        print(f"Welcome back, Mister {uname}\nHow can I help you?")
        speak(f"Welcome back, Mister {uname}")
        speak("How can I help you?")

    while True:
        query = takeCommand().lower()
        """
        All the commands said by user will be stored here in 'query' and will be converted to lowercase for easy recognition of command
        """
        # if "wikipedia" in query:
        #     speak("Searching Wikipedia...")
        #     query = query.replace("wikipedia", "")
        #     results = wikipedia.summary(query, sentences=3)
        #     speak("According to Wikipedia...")
        #     print(results)
        #     speak(results)

        if "open youtube" in query:
            print("Here you go to Youtube\n")
            speak("Here you go to Youtube\n")
            webbrowser.open("youtube.com")

        elif "open google" in query:
            print("Here you go to Google\n")
            speak("Here you go to Google\n")
            webbrowser.open("google.com")

        elif "the time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"Sir, the time is {strTime}")
            speak(f"Sir, the time is {strTime}")

        elif "stop" in query:
            print(f"Thank you for using, {assistant}")
            speak(f"Thank you for using, {assistant}")
            sys.exit()

        else:
            response = model.generate_content(query)
            ans = response.text
            print(ans)
            speak(ans)
