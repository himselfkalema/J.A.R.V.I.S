from core.voice import speak, listen
from core.ai import ask_ai
from core.personality import respond
from skills.system import get_time
from ui.hud import JarvisHUD, start_hud

WAKE_WORD = "jarvis"

hud = JarvisHUD()
start_hud(hud)

speak("JARVIS online. Awaiting wake word.")
hud.set_status("Awaiting wake word")

while True:
    heard = listen()

    if WAKE_WORD not in heard:
        continue

    hud.set_status("Listening for command")
    speak("Yes?")
    command = listen()

    if not command:
        hud.set_status("Idle")
        continue

    hud.set_status(f"Processing: {command}")
    ai = ask_ai(command)

    intent = ai["intent"]
    response = ai["response"]

    if intent == "greeting":
        hud.set_status("Greeting user")
        speak(respond("greeting"))

    elif intent == "time":
        hud.set_status("Fetching time")
        speak(f"The time is {get_time()}")

    elif intent == "exit":
        hud.set_status("Shutting down")
        speak(respond("exit"))
        break

    else:
        hud.set_status("Responding")
        speak(response)

    hud.set_status("Standing by")
