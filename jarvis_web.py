"""
JARVIS Web Interface - Flask Backend
Provides a web-based frontend for JARVIS voice assistant
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import threading
import queue
import json
import os
from dotenv import load_dotenv

# Load environment variables
try:
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        load_dotenv(dotenv_path=env_path, encoding='utf-8')
    else:
        load_dotenv()
except:
    pass

# Import JARVIS functions
import sys
import importlib.util

# Import from main jarvis file (handle filename with ampersand)
jarvis_path = os.path.join(os.path.dirname(__file__), 'jarvis_&_reply.py')
spec = importlib.util.spec_from_file_location("jarvis_reply", jarvis_path)
jarvis_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(jarvis_module)

# Import functions from the module
speak = jarvis_module.speak
listen = jarvis_module.listen
ask_ai = jarvis_module.ask_ai
get_system_info = jarvis_module.get_system_info
get_cpu_usage = jarvis_module.get_cpu_usage
get_memory_usage = jarvis_module.get_memory_usage
get_disk_usage = jarvis_module.get_disk_usage
get_battery_status = jarvis_module.get_battery_status
check_internet_connection = jarvis_module.check_internet_connection
get_wifi_info = jarvis_module.get_wifi_info
system_health_check = jarvis_module.system_health_check
take_screenshot = jarvis_module.take_screenshot
search_files = jarvis_module.search_files
create_folder = jarvis_module.create_folder
open_folder = jarvis_module.open_folder
open_application = jarvis_module.open_application
get_date = jarvis_module.get_date
get_personalized_response = jarvis_module.get_personalized_response
personality = jarvis_module.personality
memory = jarvis_module.memory
APP_COMMANDS = jarvis_module.APP_COMMANDS

import datetime

app = Flask(__name__)
CORS(app)

# Global variables for communication
command_queue = queue.Queue()
response_queue = queue.Queue()
system_status = {}

@app.route('/')
def index():
    """Serve the main web interface"""
    return render_template('index.html')

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get current system status"""
    try:
        status = {
            "cpu": get_cpu_usage(),
            "memory": get_memory_usage(),
            "disk": get_disk_usage(),
            "battery": get_battery_status(),
            "internet": check_internet_connection()[1],
            "wifi": get_wifi_info(),
            "time": datetime.datetime.now().strftime("%H:%M:%S"),
            "date": get_date()
        }
        return jsonify(status)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/command', methods=['POST'])
def handle_command():
    """Handle voice or text commands"""
    try:
        data = request.json
        command = data.get('command', '').strip()
        
        if not command:
            return jsonify({"error": "No command provided"}), 400
        
        # Process command through JARVIS AI
        ai_result = ask_ai(command)
        intent = ai_result.get("intent", "chat")
        response = ai_result.get("response", "I didn't understand that.")
        
        # Handle different intents
        result = process_command(intent, command, response)
        
        return jsonify({
            "intent": intent,
            "response": result.get("message", response),
            "action": result.get("action"),
            "data": result.get("data")
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def process_command(intent, command, response):
    """Process commands and return results"""
    result = {"message": response, "action": None, "data": None}
    
    try:
        if intent == "time":
            time_now = datetime.datetime.now().strftime("%H:%M")
            result["message"] = get_personalized_response("time", time=time_now)
            result["data"] = {"time": time_now}
            
        elif intent == "date":
            date_info = get_date()
            result["message"] = f"Today is {date_info}"
            result["data"] = {"date": date_info}
            
        elif intent == "cpu_usage":
            result["message"] = get_cpu_usage()
            
        elif intent == "memory_usage":
            result["message"] = get_memory_usage()
            
        elif intent == "disk_usage":
            result["message"] = get_disk_usage()
            
        elif intent == "battery_status":
            result["message"] = get_battery_status()
            
        elif intent == "internet_check":
            success, msg = check_internet_connection()
            result["message"] = msg
            
        elif intent == "wifi_info":
            result["message"] = get_wifi_info()
            
        elif intent == "system_info":
            info = get_system_info()
            if "error" not in info:
                result["message"] = f"OS: {info.get('os')} {info.get('os_version', '')}. CPU: {info.get('cpu_usage')}. Memory: {info.get('memory_usage')}. Disk: {info.get('disk_usage')}."
                result["data"] = info
            else:
                result["message"] = "Unable to retrieve system information."
                
        elif intent == "health_check":
            result["message"] = system_health_check()
            
        elif intent == "screenshot":
            screenshot_result = take_screenshot()
            result["message"] = screenshot_result
            result["action"] = "screenshot"
            
        elif intent == "open_app":
            app_name = extract_app_name(command)
            if app_name:
                success, message = open_application(app_name)
                result["message"] = message
                result["action"] = "app_opened"
                result["data"] = {"app": app_name}
            else:
                result["message"] = "I didn't catch which application you want to open."
                
        elif intent == "search_files":
            query = extract_search_query(command)
            if query:
                search_result = search_files(query)
                result["message"] = search_result
            else:
                result["message"] = "Please specify what file you want to search for."
                
        elif intent == "create_folder":
            folder_name = extract_folder_name(command)
            if folder_name:
                folder_result = create_folder(folder_name)
                result["message"] = folder_result
            else:
                result["message"] = "Please specify the folder name."
                
        elif intent == "open_folder":
            folder_path = extract_folder_path(command)
            if folder_path:
                folder_result = open_folder(folder_path)
                result["message"] = folder_result
            else:
                result["message"] = "Please specify which folder to open."
                
        elif intent == "shutdown":
            result["message"] = get_personalized_response("shutdown")
            result["action"] = "warning"
            result["data"] = {"type": "shutdown"}
            
        elif intent == "restart":
            result["message"] = get_personalized_response("restart")
            result["action"] = "warning"
            result["data"] = {"type": "restart"}
            
        elif intent == "sleep":
            result["message"] = get_personalized_response("sleep")
            result["action"] = "warning"
            result["data"] = {"type": "sleep"}
            
    except Exception as e:
        result["message"] = f"Error processing command: {str(e)}"
    
    return result

def extract_app_name(command):
    """Extract application name from command"""
    open_keywords = ["open", "launch", "start", "run"]
    for keyword in open_keywords:
        if keyword in command:
            parts = command.split(keyword, 1)
            if len(parts) > 1:
                return parts[1].strip()
    for app in APP_COMMANDS.keys():
        if app in command:
            return app
    return None

def extract_search_query(command):
    """Extract search query from command"""
    search_keywords = ["search", "find", "look for"]
    for keyword in search_keywords:
        if keyword in command:
            parts = command.split(keyword, 1)
            if len(parts) > 1:
                query = parts[1].strip()
                query = query.replace("for", "").replace("file", "").strip()
                return query
    return None

def extract_folder_name(command):
    """Extract folder name from command"""
    folder_keywords = ["create", "make", "new folder"]
    for keyword in folder_keywords:
        if keyword in command:
            parts = command.split(keyword, 1)
            if len(parts) > 1:
                folder_name = parts[1].strip()
                folder_name = folder_name.replace("folder", "").replace("named", "").strip()
                return folder_name
    return None

def extract_folder_path(command):
    """Extract folder path from command"""
    folder_keywords = ["open", "show", "go to"]
    for keyword in folder_keywords:
        if keyword in command:
            parts = command.split(keyword, 1)
            if len(parts) > 1:
                folder_path = parts[1].strip()
                folder_path = folder_path.replace("folder", "").strip()
                if not os.path.exists(folder_path):
                    common_paths = {
                        "desktop": os.path.join(os.path.expanduser("~"), "Desktop"),
                        "documents": os.path.join(os.path.expanduser("~"), "Documents"),
                        "downloads": os.path.join(os.path.expanduser("~"), "Downloads"),
                    }
                    folder_path = common_paths.get(folder_path.lower(), folder_path)
                return folder_path
    return None

@app.route('/api/execute_action', methods=['POST'])
def execute_action():
    """Execute dangerous actions like shutdown/restart"""
    try:
        data = request.json
        action_type = data.get('type')
        confirmed = data.get('confirmed', False)
        
        if not confirmed:
            return jsonify({"error": "Action not confirmed"}), 400
        
        if action_type == "shutdown":
            shutdown_system = jarvis_module.shutdown_system
            shutdown_system()
            return jsonify({"message": "Shutting down..."})
        elif action_type == "restart":
            restart_system = jarvis_module.restart_system
            restart_system()
            return jsonify({"message": "Restarting..."})
        elif action_type == "sleep":
            sleep_system = jarvis_module.sleep_system
            sleep_system()
            return jsonify({"message": "Going to sleep..."})
        else:
            return jsonify({"error": "Unknown action"}), 400
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting JARVIS Web Interface...")
    print("Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

