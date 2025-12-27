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
        },
        "shutdown": {
            "calm": ["Shutting down the system. Goodbye.", "Initiating shutdown sequence."],
            "sassy": ["As you wish, turning off.", "Finally, some rest for the system!"]
        },
        "restart": {
            "calm": ["Restarting the system.", "Initiating system restart."],
            "sassy": ["Rebooting now!", "Time for a fresh start!"]
        },
        "sleep": {
            "calm": ["Putting the system to sleep.", "Entering sleep mode."],
            "sassy": ["Nap time for the computer!", "Going to sleep mode now."]
        },
        "system_info": {
            "calm": ["Here's the system information.", "Gathering system data."],
            "sassy": ["Let me check my vitals for you.", "System status incoming!"]
        },
        "health_check": {
            "calm": ["Running system health check.", "Analyzing system status."],
            "sassy": ["Time for my checkup!", "Let's see how I'm doing."]
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
import os
# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    # Try to load .env file explicitly
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        load_dotenv(dotenv_path=env_path, encoding='utf-8')
    else:
        load_dotenv()  # Try default location
except Exception as e:
    print(f"Warning: Could not load .env file: {e}")
    # Try manual reading as fallback
    try:
        env_path = os.path.join(os.path.dirname(__file__), '.env')
        if os.path.exists(env_path):
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
    except Exception as e2:
        print(f"Warning: Could not manually read .env file: {e2}")

# Get API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables. Please set it in .env file or as an environment variable.")

client = OpenAI(api_key=api_key)

def ask_ai(user_input):
    # system prompt defines Jarvis behavior
    system_prompt = """
    You are Jarvis, a comprehensive laptop management assistant.
    Classify user input into intents:
    time, date, greeting, calculator, exit, open_app, shutdown, restart, sleep, 
    system_info, cpu_usage, memory_usage, disk_usage, battery_status, 
    internet_check, wifi_info, volume_control, search_files, create_folder, 
    open_folder, screenshot, health_check, chat
    
    Examples:
    - "what's my CPU usage" -> intent: "cpu_usage"
    - "check memory" -> intent: "memory_usage"
    - "how much disk space" -> intent: "disk_usage"
    - "battery status" -> intent: "battery_status"
    - "check internet" -> intent: "internet_check"
    - "wifi information" -> intent: "wifi_info"
    - "system information" -> intent: "system_info"
    - "health check" -> intent: "health_check"
    - "take screenshot" -> intent: "screenshot"
    - "search for file" -> intent: "search_files"
    - "create folder" -> intent: "create_folder"
    - "open folder" -> intent: "open_folder"
    - "increase volume" -> intent: "volume_control"
    - "what's the date" -> intent: "date"
    
    For open_app intent, extract the application name from the user's request.
    For shutdown: detect "shutdown", "turn off", "power off", "shut down laptop"
    For restart: detect "restart", "reboot", "restart laptop"
    For sleep: detect "sleep", "hibernate", "put to sleep"
    
    Return ONLY in JSON format:
    {"intent": "...", "response": "..."}
    If intent is open_app, include the app name in the response.
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
import subprocess
import psutil
import platform
import socket
import shutil
import glob
from pathlib import Path

engine = pyttsx3.init()
engine.setProperty('rate', 175)



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

# Application mapping for Windows
APP_COMMANDS = {
    "notepad": "notepad",
    "calculator": "calc",
    "calc": "calc",
    "paint": "mspaint",
    "browser": "start chrome",
    "chrome": "start chrome",
    "edge": "start msedge",
    "firefox": "start firefox",
    "explorer": "explorer",
    "file explorer": "explorer",
    "cmd": "cmd",
    "command prompt": "cmd",
    "powershell": "powershell",
    "task manager": "taskmgr",
    "settings": "start ms-settings:",
    "word": "winword",
    "excel": "excel",
    "powerpoint": "powerpnt",
    "spotify": "spotify",
    "discord": "discord",
    "steam": "steam",
    "control panel": "control",
}

def open_application(app_name):
    """Open an application based on app name"""

    app_name_lower = app_name.lower().strip()
    
    # Try to find the app in our mapping
    if app_name_lower in APP_COMMANDS:
        command = APP_COMMANDS[app_name_lower]
        try:
            # Use os.system for simple commands
            os.system(command)
            return True, f"Opening {app_name}"
        except Exception as e:
            return False, f"Failed to open {app_name}: {str(e)}"
    
    # Try common Windows start commands
    try:
        # Try using start command
        os.system(f'start {app_name_lower}')
        return True, f"Opening {app_name}"
    except:
        pass
    
    # Try using os.startfile (for file associations)
    try:
        os.startfile(app_name_lower)
        return True, f"Opening {app_name}"
    except:
        pass
    
    return False, f"Could not find application: {app_name}"

def shutdown_system():
    """Shutdown the system"""
    os.system("shutdown /s /t 5")  # Shutdown in 5 seconds

def restart_system():
    """Restart the system"""
    os.system("shutdown /r /t 5")  # Restart in 5 seconds

def sleep_system():
    """Put the system to sleep"""
    os.system("shutdown /h")  # Hibernate (sleep)
    

# ========== SYSTEM MONITORING FUNCTIONS ==========

def get_system_info():
    """Get comprehensive system information"""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        battery = psutil.sensors_battery() if hasattr(psutil, 'sensors_battery') else None
        
        info = {
            "cpu_usage": f"{cpu_percent}%",
            "memory_usage": f"{memory.percent}%",
            "memory_available": f"{memory.available / (1024**3):.2f} GB",
            "disk_usage": f"{disk.percent}%",
            "disk_free": f"{disk.free / (1024**3):.2f} GB",
            "os": platform.system(),
            "os_version": platform.version(),
            "processor": platform.processor(),
            "hostname": socket.gethostname()
        }
        
        if battery:
            info["battery_percent"] = f"{battery.percent}%"
            info["battery_plugged"] = "plugged in" if battery.power_plugged else "on battery"
        else:
            info["battery_percent"] = "N/A"
            info["battery_plugged"] = "N/A"
            
        return info
    except Exception as e:
        return {"error": str(e)}

def get_cpu_usage():
    """Get current CPU usage"""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        return f"CPU usage is {cpu_percent}%"
    except:
        return "Unable to get CPU usage"

def get_memory_usage():
    """Get current memory usage"""
    try:
        memory = psutil.virtual_memory()
        return f"Memory usage is {memory.percent}%. {memory.available / (1024**3):.2f} GB available out of {memory.total / (1024**3):.2f} GB total"
    except:
        return "Unable to get memory usage"

def get_disk_usage():
    """Get disk usage"""
    try:
        disk = psutil.disk_usage('/')
        return f"Disk usage is {disk.percent}%. {disk.free / (1024**3):.2f} GB free out of {disk.total / (1024**3):.2f} GB total"
    except:
        return "Unable to get disk usage"

def get_battery_status():
    """Get battery status"""
    try:
        battery = psutil.sensors_battery()
        if battery:
            status = "plugged in" if battery.power_plugged else "on battery"
            return f"Battery is at {battery.percent}% and {status}"
        else:
            return "Battery information not available"
    except:
        return "Unable to get battery status"

# ========== NETWORK FUNCTIONS ==========

def check_internet_connection():
    """Check if internet connection is available"""
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True, "Internet connection is active"
    except OSError:
        return False, "No internet connection detected"

def get_wifi_info():
    """Get WiFi information"""
    try:
        result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], 
                              capture_output=True, text=True, timeout=5)
        if 'SSID' in result.stdout:
            for line in result.stdout.split('\n'):
                if 'SSID' in line and 'BSSID' not in line:
                    return f"Connected to {line.split(':')[1].strip()}"
        return "WiFi information retrieved"
    except:
        return "Unable to get WiFi information"

# ========== VOLUME CONTROL ==========

def set_volume(level):
    """Set system volume (0-100)"""
    try:
        # Using nircmd or PowerShell for volume control
        subprocess.run(['powershell', '-command', 
                       f'(New-Object -ComObject Shell.Application).NameSpace(17).Items().Item("Audio Settings").InvokeVerb()'])
        return f"Volume controls opened. Please adjust manually."
    except:
        # Alternative: use nircmd if available, or just inform user
        return f"Please adjust volume manually. Requested level: {level}%"

def volume_up():
    """Increase volume"""
    try:
        os.system("powershell -command (New-Object -comObject Shell.Application).NameSpace(17).Items().Item('Audio Settings').InvokeVerb()")
        return "Opening volume controls"
    except:
        return "Please adjust volume manually"

def volume_down():
    """Decrease volume"""
    return volume_up()  # Same as volume up for now

def mute_volume():
    """Mute/unmute volume"""
    try:
        os.system("powershell -command (New-Object -comObject Shell.Application).NameSpace(17).Items().Item('Audio Settings').InvokeVerb()")
        return "Opening volume controls for mute"
    except:
        return "Please adjust volume manually"

# ========== FILE MANAGEMENT ==========

def search_files(query, path="C:\\"):
    """Search for files by name"""
    try:
        # Limit search to common directories for performance
        search_paths = [
            os.path.join(os.path.expanduser("~"), "Desktop"),
            os.path.join(os.path.expanduser("~"), "Documents"),
            os.path.join(os.path.expanduser("~"), "Downloads"),
        ]
        
        results = []
        for search_path in search_paths:
            if os.path.exists(search_path):
                for root, dirs, files in os.walk(search_path):
                    for file in files:
                        if query.lower() in file.lower():
                            results.append(os.path.join(root, file))
                    if len(results) >= 10:  # Limit results
                        break
                if len(results) >= 10:
                    break
        
        if results:
            return f"Found {len(results)} files matching '{query}'. Opening first result."
        else:
            return f"No files found matching '{query}'"
    except Exception as e:
        return f"Error searching for files: {str(e)}"

def open_folder(path):
    """Open a folder in File Explorer"""
    try:
        if os.path.exists(path):
            os.startfile(path)
            return f"Opening folder: {path}"
        else:
            return f"Folder not found: {path}"
    except Exception as e:
        return f"Error opening folder: {str(e)}"

def create_folder(folder_name, location=None):
    """Create a new folder"""
    try:
        if location is None:
            location = os.path.join(os.path.expanduser("~"), "Desktop")
        
        folder_path = os.path.join(location, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        return f"Created folder: {folder_path}"
    except Exception as e:
        return f"Error creating folder: {str(e)}"

# ========== SCREENSHOT ==========

def take_screenshot():
    """Take a screenshot"""
    try:
        screenshot_dir = os.path.join(os.path.expanduser("~"), "Pictures", "Screenshots")
        os.makedirs(screenshot_dir, exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = os.path.join(screenshot_dir, f"screenshot_{timestamp}.png")
        
        # Use Windows Snipping Tool or PowerShell
        os.system(f'powershell -command "Add-Type -AssemblyName System.Windows.Forms,System.Drawing; $bounds = [System.Windows.Forms.SystemInformation]::VirtualScreen; $bmp = New-Object System.Drawing.Bitmap $bounds.Width, $bounds.Height; $graphics = [System.Drawing.Graphics]::FromImage($bmp); $graphics.CopyFromScreen($bounds.Location, [System.Drawing.Point]::Empty, $bounds.Size); $bmp.Save(\'{screenshot_path}\'); $graphics.Dispose(); $bmp.Dispose()"')
        
        return f"Screenshot saved to {screenshot_path}"
    except Exception as e:
        return f"Error taking screenshot: {str(e)}"

# ========== DATE FUNCTIONS ==========

def get_date():
    """Get current date"""
    today = datetime.datetime.now()
    return today.strftime("%A, %B %d, %Y")

def get_date_time():
    """Get current date and time"""
    now = datetime.datetime.now()
    date_str = now.strftime("%A, %B %d, %Y")
    time_str = now.strftime("%H:%M")
    return f"{date_str} at {time_str}"

# ========== SYSTEM HEALTH CHECK ==========

def system_health_check():
    """Perform a comprehensive system health check"""
    try:
        info = get_system_info()
        internet_status, internet_msg = check_internet_connection()
        
        health_report = []
        
        # CPU check
        cpu = float(info.get("cpu_usage", "0").replace("%", ""))
        if cpu > 90:
            health_report.append("Warning: CPU usage is very high")
        else:
            health_report.append(f"CPU usage: {info.get('cpu_usage')} - Normal")
        
        # Memory check
        memory = float(info.get("memory_usage", "0").replace("%", ""))
        if memory > 90:
            health_report.append("Warning: Memory usage is very high")
        else:
            health_report.append(f"Memory: {info.get('memory_usage')} used - Normal")
        
        # Disk check
        disk = float(info.get("disk_usage", "0").replace("%", ""))
        if disk > 90:
            health_report.append("Warning: Disk space is running low")
        else:
            health_report.append(f"Disk: {info.get('disk_usage')} used - Normal")
        
        # Internet check
        health_report.append(internet_msg)
        
        # Battery check
        if info.get("battery_percent") != "N/A":
            battery = float(info.get("battery_percent", "0").replace("%", ""))
            if battery < 20 and info.get("battery_plugged") == "on battery":
                health_report.append(f"Warning: Battery is low at {info.get('battery_percent')}")
            else:
                health_report.append(f"Battery: {info.get('battery_percent')} - {info.get('battery_plugged')}")
        
        return ". ".join(health_report)
    except Exception as e:
        return f"Error performing health check: {str(e)}"


name = memory.get("name")
if name:
    speak(f"Welcome back, {name}. JARVIS system online and ready. I can help you manage your laptop, check system status, open applications, and much more. How may I assist you?")
else:
    speak("JARVIS system online and ready. I am your personal assistant and can help you manage your laptop. I can check system information, open applications, control power settings, manage files, take screenshots, and more. How may I assist you today?")

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
    elif intent == "open_app":
        # Extract app name from command
        app_name = None
        # Look for common patterns like "open notepad", "launch chrome", "start calculator"
        open_keywords = ["open", "launch", "start", "run"]
        for keyword in open_keywords:
            if keyword in command:
                # Get the app name after the keyword
                parts = command.split(keyword, 1)
                if len(parts) > 1:
                    app_name = parts[1].strip()
                    break
        
        # If not found, try to extract from response
        if not app_name:
            # Try common apps
            for app in APP_COMMANDS.keys():
                if app in command:
                    app_name = app
                    break
        
        if app_name:
            success, message = open_application(app_name)
            if success:
                speak(message)
            else:
                speak(message)
        else:
            speak("I didn't catch which application you want to open. Please specify the app name.")
    elif intent == "shutdown":
        speak(get_personalized_response("shutdown"))
        shutdown_system()
        break
    elif intent == "restart":
        speak(get_personalized_response("restart"))
        restart_system()
        break
    elif intent == "sleep":
        speak(get_personalized_response("sleep"))
        sleep_system()
        break
    elif intent == "exit":
        speak(get_personalized_response("exit"))
        break
    elif intent == "time":
        time_now = datetime.datetime.now().strftime("%H:%M")
        speak(get_personalized_response("time", time=time_now))
    elif intent == "date":
        date_info = get_date()
        speak(f"Today is {date_info}")
    elif intent == "system_info":
        speak(get_personalized_response("system_info"))
        info = get_system_info()
        if "error" not in info:
            info_text = f"OS: {info.get('os')} {info.get('os_version', '')}. "
            info_text += f"CPU usage: {info.get('cpu_usage')}. "
            info_text += f"Memory usage: {info.get('memory_usage')}. "
            info_text += f"Disk usage: {info.get('disk_usage')}. "
            if info.get('battery_percent') != "N/A":
                info_text += f"Battery: {info.get('battery_percent')}, {info.get('battery_plugged')}."
            speak(info_text)
        else:
            speak("Unable to retrieve system information.")
    elif intent == "cpu_usage":
        cpu_info = get_cpu_usage()
        speak(cpu_info)
    elif intent == "memory_usage":
        memory_info = get_memory_usage()
        speak(memory_info)
    elif intent == "disk_usage":
        disk_info = get_disk_usage()
        speak(disk_info)
    elif intent == "battery_status":
        battery_info = get_battery_status()
        speak(battery_info)
    elif intent == "internet_check":
        success, internet_msg = check_internet_connection()
        speak(internet_msg)
    elif intent == "wifi_info":
        wifi_info = get_wifi_info()
        speak(wifi_info)
    elif intent == "health_check":
        speak(get_personalized_response("health_check"))
        health_report = system_health_check()
        speak(health_report)
    elif intent == "screenshot":
        screenshot_result = take_screenshot()
        speak(screenshot_result)
    elif intent == "search_files":
        # Extract search query from command
        search_keywords = ["search", "find", "look for"]
        query = None
        for keyword in search_keywords:
            if keyword in command:
                parts = command.split(keyword, 1)
                if len(parts) > 1:
                    query = parts[1].strip()
                    # Remove common words
                    query = query.replace("for", "").replace("file", "").strip()
                    break
        if query:
            search_result = search_files(query)
            speak(search_result)
        else:
            speak("Please specify what file you want to search for.")
    elif intent == "create_folder":
        # Extract folder name from command
        folder_keywords = ["create", "make", "new folder"]
        folder_name = None
        for keyword in folder_keywords:
            if keyword in command:
                parts = command.split(keyword, 1)
                if len(parts) > 1:
                    folder_name = parts[1].strip()
                    folder_name = folder_name.replace("folder", "").replace("named", "").strip()
                    break
        if folder_name:
            folder_result = create_folder(folder_name)
            speak(folder_result)
        else:
            speak("Please specify the folder name.")
    elif intent == "open_folder":
        # Extract folder path from command
        folder_keywords = ["open", "show", "go to"]
        folder_path = None
        for keyword in folder_keywords:
            if keyword in command:
                parts = command.split(keyword, 1)
                if len(parts) > 1:
                    folder_path = parts[1].strip()
                    folder_path = folder_path.replace("folder", "").strip()
                    # Try common paths
                    if not os.path.exists(folder_path):
                        # Try desktop, documents, downloads
                        common_paths = {
                            "desktop": os.path.join(os.path.expanduser("~"), "Desktop"),
                            "documents": os.path.join(os.path.expanduser("~"), "Documents"),
                            "downloads": os.path.join(os.path.expanduser("~"), "Downloads"),
                        }
                        folder_path = common_paths.get(folder_path.lower(), folder_path)
                    break
        if folder_path:
            folder_result = open_folder(folder_path)
            speak(folder_result)
        else:
            speak("Please specify which folder to open.")
    elif intent == "volume_control":
        if "up" in command or "increase" in command:
            volume_result = volume_up()
            speak(volume_result)
        elif "down" in command or "decrease" in command:
            volume_result = volume_down()
            speak(volume_result)
        elif "mute" in command:
            volume_result = mute_volume()
            speak(volume_result)
        else:
            speak("Please specify: volume up, volume down, or mute")
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
