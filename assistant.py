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
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import CacheFileHandler
from urllib.request import urlopen
from dotenv import load_dotenv

# Load API Keys from .env file
load_dotenv()

# Store the API keys
gemini_api = os.getenv('GEMINI_API')
spotify_client_id = os.getenv('SPOTIFY_CLIENT_ID')
spotify_client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
weather_api = os.getenv('WEATHER_API')

default_location = 'Bangalore, India'


Genai.configure(api_key=gemini_api)

model = Genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=Genai.GenerationConfig(
        max_output_tokens=2048,
        temperature=0.7,
    ),
)

cache_handler = CacheFileHandler(cache_path=".spotipycache")

sp_oauth = SpotifyOAuth(client_id=spotify_client_id,
                  client_secret=spotify_client_secret,
                  redirect_uri="http://localhost:8888/callback",
                  scope="user-library-read user-modify-playback-state user-read-playback-state",
                  cache_handler=cache_handler)
token_info = sp_oauth.get_access_token()

sp = spotipy.Spotify(auth=token_info['access_token'])

# Refresh access token if expired
if sp_oauth.is_token_expired(token_info):
    token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    sp = spotipy.Spotify(auth=token_info['access_token'])

assistant = "Veda 1 point o"

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)


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
    
def open_web_player():
    webbrowser.open("https://open.spotify.com/")
    print("Opening Spotify Web Player...")
    speak("Opening Spotify Web Player...")
    
def playSpotify():
    try:
        devices = sp.devices()

        if not devices['devices']:
            open_web_player()
            time.sleep(5)
            devices = sp.devices()
        
        if not devices['devices']:
            print("Failed to detect the Web Player after opening it.")
            speak("Failed to detect the Web Player after opening it.")
            return

        # Retrieve user's liked songs
        results = sp.current_user_saved_tracks()
        liked_songs = results["items"]

        # Get the song URIs
        song_uris = [song["track"]["uri"] for song in liked_songs]
        
        # Play the songs on the first available device
        device_id = devices['devices'][0]['id']
        sp.start_playback(device_id=device_id, uris=song_uris)
        print("Playing your liked songs...")
        speak("Playing your liked songs...")

    except spotipy.exceptions.SpotifyException as e:
        print(f"Spotify API Error: {e}")
        speak(f"Spotify API Error: {e}")
        
def open_website(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url  # Default to https if no scheme is provided
    webbrowser.open(url)


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
        if "open youtube" in query:
            print("Here you go to YouTube\n")
            speak("Here you go to YouTube\n")
            open_website("youtube.com")
            exit()

        elif "open google" in query:
            print("Here you go to Google\n")
            speak("Here you go to Google\n")
            open_website("google.com")
            exit()
            
        elif "open github" in query or "open my github" in query:
            print(f"Here you go to your github")
            speak(f"Here you go to your github")
            open_website("github.com/bkk31")
            exit()

        elif "the time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"Sir, the time is {strTime}")
            speak(f"Sir, the time is {strTime}")

        elif "stop" in query:
            print(f"Thank you for using, {assistant}")
            speak(f"Thank you for using, {assistant}")
            sys.exit()
            
        elif "play liked songs" in query or "play songs" in query or "play like songs" in query:
            playSpotify()
            exit()   

        elif "restart" in query:
            subprocess.call(["shutdown", "/r"])
             
        elif "hibernate" in query or "sleep" in query:
            speak("Hibernating")
            subprocess.call("shutdown / h")
 
        elif "log off" in query or "sign out" in query:
            speak("Make sure all the application are closed before sign-out")
            time.sleep(5)
            subprocess.call(["shutdown", "/l"])
            
        elif 'joke' in query:
            joke = pyjokes.get_joke()
            print(joke)
            speak(joke)

        else:
            response = model.generate_content(query)
            ans = response.text
            print(ans)
            speak(ans)
