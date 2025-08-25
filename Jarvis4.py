import pyowm
import wikipedia
import pywhatkit
import pyttsx3
import pyjokes
import pyautogui
import pyperclip
import subprocess
import os
import secrets
import string
import random
import psutil
import datetime
import speech_recognition as sr
import smtplib
from mail_data import senderemail, epwd, to
from email.message import EmailMessage
from newsapi import NewsApiClient

# Store the selected voice id globally
selected_voice_id = None

# Screenshot counter
screenshot_counter = 1

def speak(audio):
    engine = pyttsx3.init()
    global selected_voice_id
    if selected_voice_id is not None:
        engine.setProperty('voice', selected_voice_id)
    engine.say(audio)
    engine.runAndWait()

def getvoices(voice):
    global selected_voice_id
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    # On Windows, voices may have different indexes. Adjust as needed:
    # print([i for i, v in enumerate(voices)])
    if voice == 1:
        selected_voice_id = voices[0].id
        engine.setProperty('voice', selected_voice_id)
        speak("hello this is jarvis")
    elif voice == 2:
        # You may need to change the index below for your preferred voice
        selected_voice_id = voices[-1].id
        engine.setProperty('voice', selected_voice_id)
        speak("hello this is Friday")

def time_now():
    return datetime.datetime.now().strftime("%H:%M:%S")

def date():
    now = datetime.datetime.now()
    return f"{now.day} {now.month} {now.year}"

def greeting():
    hour = datetime.datetime.now().hour
    if hour >= 6 and hour < 12:
        return "Good morning sir"
    elif hour >= 12 and hour < 18:
        return "Good afternoon sir"
    elif hour >= 18 and hour < 24:
        return "Good evening sir"
    else:
        return "Good night sir"

def wishme():
    current_time = time_now()
    current_date = date()
    greetings = greeting()
  # Combine all the speech into ONE call
    full_message = (
        f"{greetings} "
        f"Welcome back sir. "
        f"The current time is {current_time}. "
        f"The current date is {current_date}. "
        "Jarvis at your service, how can I help you today?"
    )
    speak(full_message)

def takeCommandCmd():
    query = input("Please tell me what you want: ")
    return query

def takeCommandMic():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        # r.adjust_for_ambient_noise(source, duration=0.2)
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-IN')
        print(f"User said: {query}")
    except Exception as e:
        print(e)
        speak("Sorry, I did not understand that.")
        speak("Please say that again...")
        return "None"
    return query

def sendEmail(receiver, subject, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(senderemail, epwd)
    email = EmailMessage()
    email['From'] = senderemail
    email['To'] = receiver
    email['Subject'] = subject
    email.set_content(content)
    server.send_message(email)    
    server.close()

def sendWhatsapp(phone_no, message):
    try:
        pywhatkit.sendwhatmsg_instantly(phone_no, message, 20, True, 5)
        speak("WhatsApp message has been sent successfully.")
    except Exception as e:
        print(e)
        speak("Sorry, I could not send the WhatsApp message.")

def searchWikipedia(query):
    try:
        speak(f"Searching Wikipedia for {query}...")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia:")
        speak(results)
    except Exception as e:
        print(e)
        speak("Sorry, I could not find any results on Wikipedia.")

def searchGoogle(query):
    try:
        speak(f"Searching Google for {query}...")
        pywhatkit.search(query)
        speak("Here are the Google search results.")
    except Exception as e:
        print(e)
        speak("Sorry, I could not perform the Google search.")

def playYoutubeVideo(query):
    try:
        speak(f"Playing {query} on YouTube...")
        pywhatkit.playonyt(query)
        speak("Enjoy your video.")
    except Exception as e:
        print(e)
        speak("Sorry, I could not play the YouTube video.")

def getWeather(city_name):
    try:
        owm = pyowm.OWM('c0764f5fe44e5d873da2ae0e97e762da')  # Replace with your actual API key
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(city_name)
        weather = observation.weather
        temp = weather.temperature('celsius')['temp']
        status = weather.detailed_status
        speak(f"The current temperature in {city_name} is {temp} degrees Celsius with {status}.")
    except Exception as e:
        print(e)
        speak("Sorry, I could not retrieve the weather information.")

def getNews():
    try:
        newsapi = NewsApiClient(api_key='539bec574a884605823bf44b84587cbb')  # Replace with your NewsAPI key
        top_headlines = newsapi.get_top_headlines(language='en')
        articles = top_headlines['articles']
        if not articles:
            speak("Sorry, I could not find any news updates.")
            return
        speak("Here are the top news headlines:")
        for i, article in enumerate(articles[:5]):
            speak(f"Headline {i+1}: {article['title']}")
    except Exception as e:
        print(e)
        speak("Sorry, I could not retrieve the news updates.")

def tellJoke():
    joke = pyjokes.get_joke()
    speak(joke)

def takeScreenshot():
    global screenshot_counter
    try:
        screenshot = pyautogui.screenshot()
        # Find next available filename
        while True:
            filename = f"screenshot_{screenshot_counter}.png"
            if not os.path.exists(filename):
                break
            screenshot_counter += 1
        screenshot.save(filename)
        speak(f"Screenshot saved as {filename}.")
        screenshot_counter += 1
    except Exception as e:
        print(e)
        speak("Sorry, I could not take the screenshot.")

def openApplication(app_name):
    app_map = {
        'chrome': r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        'notepad': 'notepad.exe',
        'calculator': 'calc.exe',
        'terminal': 'cmd.exe',
        'vscode': r'C:\Users\<username>\AppData\Local\Programs\Microsoft VS Code\Code.exe',
        'spotify': r'C:\Users\<username>\AppData\Roaming\Spotify\Spotify.exe',
        'explorer': 'explorer.exe',
        # Add more mappings as needed
    }
    app_to_open = app_map.get(app_name.lower(), app_name)
    try:
        if os.path.isfile(app_to_open) or app_to_open.endswith('.exe'):
            os.startfile(app_to_open)
        else:
            # Try opening as folder or fallback
            os.startfile(app_to_open)
        speak(f"Opening {app_to_open}.")
    except Exception as e:
        print(e)
        speak(f"Sorry, I could not open {app_to_open}.")

def openDocumentsFolder():
    try:
        documents_path = os.path.join(os.path.expanduser('~'), 'Documents')
        os.startfile(documents_path)
        speak("Opening your Documents folder.")
    except Exception as e:
        print(e)
        speak("Sorry, I could not open your Documents folder.")

def generatePassword(length=10):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    print(f"Generated password: {password}")

def rememberNote(note):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('memory.txt', 'a') as f:
        f.write(f"[{timestamp}] {note}\n")
    print(f"Remembered: [{timestamp}] {note}")

def recallNotes():
    try:
        with open('memory.txt', 'r') as f:
            notes = f.read()
        if notes:
            print("Your notes:")
            print(notes)
        else:
            print("No notes found.")
    except FileNotFoundError:
        print("No notes found.")

def flipCoin():
    result = random.choice(['Heads', 'Tails'])
    print(f"Coin flip result: {result}")

def rollDie():
    result = random.randint(1, 6)
    print(f"Die roll result: {result}")

def cpuBatteryUpdate():
    cpu_percent = psutil.cpu_percent(interval=1)
    battery = psutil.sensors_battery()
    if battery:
        battery_percent = battery.percent
        plugged = battery.power_plugged
        print(f"CPU Usage: {cpu_percent}% | Battery: {battery_percent}% | Plugged in: {plugged}")
    else:
        print(f"CPU Usage: {cpu_percent}% | Battery info not available.")

if __name__ == "__main__":
    getvoices(1)  # Set voice to Friday
    # wishme()
    while True:
        query = takeCommandMic().lower()
        if 'time' in query:
            speak(time_now())
        elif 'date' in query:
            speak(date())
        elif 'email' in query:
            email_list = {
                'shubham': 'tiwarisubham400@gmail.com'
            }
            speak("To whom should I send the email?")
            name = takeCommandMic()
            receiver = email_list[name.lower()]
            speak("What should be the subject of the email?")
            subject = takeCommandMic()
            speak("What should I say?")
            content = takeCommandMic()
            if content != "None":
                try:
                    sendEmail(receiver,subject,content)
                    speak("Email has been sent successfully.")
                except Exception as e:
                    print(e)
                    speak("Sorry, I could not send the email.")
        elif 'whatsapp' in query:
            whatsapp_list = {
                'shubham': '+918820238775',
                'sancho': '+917980447160',
                'pp': '+916290836210'
            }
            speak("To whom should I send the WhatsApp message?")
            name = takeCommandMic()
            phone_no = whatsapp_list.get(name.lower())
            if not phone_no:
                speak("Sorry, I don't have the WhatsApp number for that contact.")
                continue
            speak("What should I say?")
            message = takeCommandMic()
            if message != "None":
                sendWhatsapp(phone_no, message)
        elif 'wikipedia' in query:
            speak("What should I search on Wikipedia?")
            search_term = takeCommandMic()
            if search_term != "None":
                searchWikipedia(search_term)
        elif 'google' in query:
            speak("What should I search on Google?")
            search_term = takeCommandMic()
            if search_term != "None":
                searchGoogle(search_term)
        elif 'play youtube' in query:
            speak("What should I play on YouTube?")
            video_term = takeCommandMic()
            if video_term != "None":
                playYoutubeVideo(video_term)
        elif 'weather' in query:
            speak("For which city do you want the weather update?")
            city_name = takeCommandMic()
            if city_name != "None":
                getWeather(city_name)
        elif 'news' in query:
            getNews()
        elif 'read text' in query:
            clipboard_text = pyperclip.paste()
            if clipboard_text:
                speak(clipboard_text)
            else:
                speak("Clipboard is empty or does not contain text.")
        elif 'joke' in query or 'tell me a joke' in query:
            tellJoke()
        elif 'screenshot' in query or 'take screenshot' in query:
            takeScreenshot()
        elif query == 'open my documents':
            openDocumentsFolder()
        elif query.startswith('open '):
            app_name = query.replace('open ', '').strip()
            if app_name:
                openApplication(app_name)
            else:
                speak("Please specify the application to open.")
        elif 'generate password' in query:
            generatePassword()
        elif query.startswith('remember '):
            note = query.replace('remember ', '').strip()
            if note:
                rememberNote(note)
            else:
                print("Please specify what to remember.")
        elif 'recall' in query or 'what did i ask you to remember' in query:
            recallNotes()
        elif 'flip a coin' in query or 'coin toss' in query:
            flipCoin()
        elif 'roll a die' in query or 'roll dice' in query:
            rollDie()
        elif 'cpu' in query or 'battery' in query:
            cpuBatteryUpdate()
        elif 'offline' in query:
            speak("Going offline, sir. Have a nice day!")
            quit()