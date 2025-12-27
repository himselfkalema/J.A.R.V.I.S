def ask_ai(command):
    # Dummy AI for demonstration
    if any(word in command for word in ["hello", "hi", "hey"]):
        return {"intent": "greeting", "response": "Hello! How can I help you?"}
    elif "time" in command:
        return {"intent": "time", "response": "Let me check the time."}
    elif "exit" in command:
        return {"intent": "exit", "response": "Goodbye!"}
    else:
        return {"intent": "chat", "response": "I'm not sure how to help with that."}
