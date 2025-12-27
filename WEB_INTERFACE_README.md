# JARVIS Web Interface

A beautiful, modern web-based frontend for your JARVIS voice assistant!

## Features

✨ **Modern UI Design**
- Beautiful gradient interface
- Real-time system status monitoring
- Chat-like interface for commands
- Responsive design

📊 **System Monitoring**
- Live CPU, Memory, Disk usage
- Battery status
- Internet connection status
- Real-time clock and date

💬 **Interactive Chat**
- Type commands directly
- Voice input support (coming soon)
- Command history
- Visual feedback

## How to Run

1. **Make sure your virtual environment is activated:**
   ```powershell
   .venv\Scripts\Activate.ps1
   ```

2. **Start the web server:**
   ```powershell
   python jarvis_web.py
   ```

3. **Open your browser:**
   - Go to: `http://localhost:5000`
   - The JARVIS interface will load automatically

## Usage

### Text Commands
Simply type your command in the input box and press Enter or click Send.

**Example commands:**
- "What's my CPU usage?"
- "Check memory"
- "Open notepad"
- "System information"
- "Take screenshot"
- "What's the date?"

### System Status
The sidebar shows real-time system information that updates every 5 seconds.

### Dangerous Actions
For commands like shutdown, restart, or sleep, a confirmation dialog will appear to prevent accidental actions.

## Architecture

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Communication**: REST API (JSON)

## API Endpoints

- `GET /` - Main web interface
- `GET /api/status` - Get system status
- `POST /api/command` - Send a command
- `POST /api/execute_action` - Execute dangerous actions (with confirmation)

## Troubleshooting

**Port already in use?**
- Change the port in `jarvis_web.py` (line 292): `app.run(debug=True, host='0.0.0.0', port=5000)`

**Can't import jarvis functions?**
- Make sure `jarvis_&_reply.py` is in the same directory
- Check that all dependencies are installed

**API key not loading?**
- Verify your `.env` file exists and contains `OPENAI_API_KEY=your_key`

Enjoy your JARVIS web interface! 🚀

