import pyttsx3

engine = pyttsx3.init()

engine.setProperty('rate', 210)   # speed (lower = slower)
engine.setProperty('volume', 100.0) # max volume

engine.say("Hello. I am Jarvis. Ready when you are.")
engine.runAndWait()
