# 🤖 JARVIS AI Assistant

A complete AI assistant inspired by Iron Man's JARVIS, powered by **Mistral AI** with voice recognition, system control, and web automation capabilities.

## ✨ Features

- 🎤 **Continuous Voice Recognition** - Always listening for your commands
- 🗣️ **Natural Speech Synthesis** - JARVIS speaks back to you
- 🌐 **Web Control** - Open websites, perform searches, navigate the internet  
- 💻 **System Integration** - Launch applications, manage files, control desktop
- 📧 **Communication** - Send emails, WhatsApp messages, manage contacts
- 🧠 **AI Intelligence** - Powered by Mistral AI for smart responses
- ⏰ **Task Management** - Set reminders, manage tasks, schedule events
- 🎵 **Media Control** - Control Spotify, manage music playback
- 💡 **Code Generation** - Create code for any project on demand
- 📊 **System Monitoring** - Check system stats, take screenshots

## 🚀 Quick Start

### Option 1: Automated Installation (Windows)
1. Download all files to a folder
2. Run `install.bat` as Administrator
3. Edit `.env` file with your API keys
4. Run `start_jarvis.bat` to start backend
5. Open `index.html` in your browser

### Option 2: Manual Installation

#### Prerequisites
- Python 3.8 or higher
- Modern web browser (Chrome, Edge, Firefox)
- Microphone for voice input
- Internet connection

#### Step 1: Install Python Dependencies
```bash
# Create virtual environment
python -m venv jarvis_env

# Activate virtual environment
# Windows:
jarvis_env\Scripts\activate
# Linux/Mac:
source jarvis_env/bin/activate

# Install packages
pip install -r requirements.txt
```

#### Step 2: Get API Keys
1. **Mistral AI API Key** (Required):
   - Go to [Mistral Console](https://console.mistral.ai/)
   - Create account and get API key
   - Copy the key

2. **Email Setup** (Optional):
   - Use Gmail App Password, not regular password
   - Enable 2FA and create App Password in Google Account settings

#### Step 3: Configure Environment
Create `.env` file:
```env
MISTRAL_API_KEY=your-actual-mistral-api-key-here
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-gmail-app-password
WEATHER_API_KEY=your-weather-api-key
```

#### Step 4: Start the System
```bash
# Start backend server
python jarvis_server.py

# Open frontend in browser
# Open index.html in your web browser
```

## 🎯 Voice Commands

### Website Control
- "Open YouTube" - Opens YouTube
- "Open Google" - Opens Google  
- "Open Instagram" - Opens Instagram
- "Open ChatGPT" - Opens ChatGPT
- "Search YouTube for Python tutorials"
- "Search Google for weather today"

### Application Control
- "Open Notepad" - Opens text editor
- "Open Calculator" - Opens calculator
- "Open Spotify" - Opens Spotify
- "Open Task Manager" - Opens system monitor
- "Open VS Code" - Opens code editor

### AI & Code Generation  
- "Create code for a web scraper"
- "Write code for a Python game"
- "Generate a React component"
- "Help me build a mobile app"

### Communication
- "Send email to John" - Compose email
- "Send WhatsApp