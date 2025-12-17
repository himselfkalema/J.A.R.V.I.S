personality = {
    "mood": "calm",  # calm, happy, sassy, serious
    "greeting_style": "polite",  # casual, funny, formal
    "responses": {
        "greeting": {
            "polite": ["Hello. How may I assist you?", "Standing by, sir."],
            "funny": ["Hey there, genius!", "Yo! What's up?"],
            "casual": ["Hey!", "Hi!"]
        },
        "time": {
            "calm": ["The current time is {time}.", "It is {time} right now."],
            "sassy": ["Tick-tock! It's {time}.", "Time flies! It's {time}."],
        },
        "exit": {
            "calm": ["Shutting down. Goodbye.", "System powering off."],
            "sassy": ["Later, human!", "Finally, some rest!"]
        }
    }
}

import random

def get_personalized_response(intent, **kwargs):
    # Get responses for the intent
    intent_responses = personality["responses"].get(intent, {})
    # Pick responses based on mood or greeting_style
    if intent == "greeting":
        style = personality.get("greeting_style", "polite")
        mood_responses = intent_responses.get(style, ["Hello."])
    else:
        mood = personality.get("mood", "calm")
        mood_responses = intent_responses.get(mood, ["I have nothing to say."])
    # Randomly pick one
    response = random.choice(mood_responses)
    # Format with kwargs like {time}, {name}
    return response.format(**kwargs)
from openai import OpenAI
import json

client = OpenAI(
    api_key="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"
)

def ask_ai(user_input):
    # system prompt defines Jarvis behavior
    system_prompt = """
    You are Jarvis, a polite and helpful assistant.
    Classify user input into intents:
    time, date, greeting, calculator, exit, chat
    Return ONLY in JSON format:
    {"intent": "...", "response": "..."}
    """

    response = client.responses.create(
        model="gpt-5-nano",
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        store=True,
    )

    output_text = response.output_text
    try:
        return json.loads(output_text)
    except:
        # fallback if AI does not return JSON
        return {"intent": "chat", "response": output_text}
import random

INTENTS = {
    "time": ["time", "clock", "current time"],
    "date": ["date", "day", "today"],
    "greeting": ["hello", "hi", "hey", "greetings"],
    "exit": ["exit", "shutdown", "quit", "goodbye"],
    "calculator": ["calculator", "calc"],
    "set_name": ["my name is", "call me"]
}

FOLLOW_UPS = ["and", "what about", "also", "tell me that too"]

RESPONSES = {
    "greeting": [
        "Hello. How may I assist?",
        "Good to hear from you.",
        "Standing by."
    ]
}

context = {
    "last_intent": None
}
from memory import load_memory, save_memory
memory = load_memory()

def get_intent(command):
    for intent, keywords in INTENTS.items():
        for word in keywords:
            if word in command:
                return intent
    return None
import speech_recognition as sr
import pyttsx3
import datetime
import os

engine = pyttsx3.init()
r = sr.Recognizer()

WAKE_WORD = "bread"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen(timeout=None):
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source, timeout=timeout)
    try:
        return r.recognize_google(audio).lower()
    except:
        return ""


name = memory.get("name")
if name:
    speak(f"Welcome back, {name}. Standing by.")
else:
    speak("System online. Standing by.")

while True:
    command = listen()
    if command == "":
        continue

    ai_result = ask_ai(command)
    intent = ai_result["intent"]
    response = ai_result["response"]

    # handle actions safely
    if intent == "calculator":
        speak(response)
        os.system("calc")
    elif intent == "exit":
        speak(get_personalized_response("exit"))
        break
    elif intent == "time":
        time_now = datetime.datetime.now().strftime("%H:%M")
        speak(get_personalized_response("time", time=time_now))
    elif intent == "greeting":
        name = memory.get("name")
        speak(get_personalized_response("greeting"))
    elif intent == "set_mood":
        # user says "be sassy" or "be happy"
        mood = command.split("be")[-1].strip()
        if mood in ["calm", "happy", "sassy", "serious"]:
            personality["mood"] = mood
            speak(f"Personality changed to {mood}.")
        else:
            speak("I don't understand that mood.")
    else:
        speak(response)
