# © 2025 Sumedh Sohan - JARVIS AI Assistant
# All rights reserved. Unauthorized use is strictly prohibited.

#!/usr/bin/env python3
"""
JARVIS Configuration File
Contains all configuration settings and environment variables
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for JARVIS AI Assistant"""
    
    # API Configuration
    MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY', 'your-mistral-api-key-here')
    MISTRAL_MODEL = "mistral-large-latest"
    
    # Server Configuration
    HOST = '0.0.0.0'
    PORT = 5000
    DEBUG = True
    
    # Email Configuration
    EMAIL_CONFIG = {
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'email': os.getenv('EMAIL_ADDRESS', ''),
        'password': os.getenv('EMAIL_PASSWORD', ''),
        'sender_name': 'JARVIS AI Assistant'
    }
    
    # Weather API (Optional)
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', '')
    WEATHER_API_URL = 'http://api.openweathermap.org/data/2.5/weather'
    
    # WhatsApp Configuration (Optional)
    WHATSAPP_API_TOKEN = os.getenv('WHATSAPP_API_TOKEN', '')
    
    # System Paths for Applications
    WINDOWS_APP_PATHS = {
        'notepad': 'notepad.exe',
        'calculator': 'calc.exe',
        'task manager': 'taskmgr.exe',
        'spotify': 'spotify.exe',
        'chrome': r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        'firefox': r'C:\Program Files\Mozilla Firefox\firefox.exe',
        'vscode': r'C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe',
        'cmd': 'cmd.exe',
        'powershell': 'powershell.exe',
        'explorer': 'explorer.exe',
        'paint': 'mspaint.exe',
        'wordpad': 'wordpad.exe'
    }
    
    LINUX_APP_PATHS = {
        'notepad': 'gedit',
        'calculator': 'gnome-calculator',
        'task manager': 'gnome-system-monitor',
        'spotify': 'spotify',
        'chrome': 'google-chrome',
        'firefox': 'firefox',
        'vscode': 'code',
        'terminal': 'gnome-terminal',
        'files': 'nautilus'
    }
    
    MAC_APP_PATHS = {
        'notepad': 'TextEdit',
        'calculator': 'Calculator',
        'task manager': 'Activity Monitor',
        'spotify': 'Spotify',
        'chrome': 'Google Chrome',
        'firefox': 'Firefox',
        'vscode': 'Visual Studio Code',
        'terminal': 'Terminal',
        'finder': 'Finder'
    }
    
    # Website URLs
    WEBSITES = {
        'youtube': 'https://youtube.com',
        'google': 'https://google.com',
        'instagram': 'https://instagram.com',
        'facebook': 'https://facebook.com',
        'twitter': 'https://twitter.com',
        'x': 'https://x.com',
        'linkedin': 'https://linkedin.com',
        'github': 'https://github.com',
        'reddit': 'https://reddit.com',
        'chatgpt': 'https://chat.openai.com',
        'claude': 'https://claude.ai',
        'stackoverflow': 'https://stackoverflow.com',
        'gmail': 'https://gmail.com',
        'whatsapp': 'https://web.whatsapp.com',
        'netflix': 'https://netflix.com',
        'amazon': 'https://amazon.com',
        'spotify': 'https://open.spotify.com',
        'discord': 'https://discord.com',
        'zoom': 'https://zoom.us',
        'teams': 'https://teams.microsoft.com'
    }
    
    # Search Engine URLs
    SEARCH_ENGINES = {
        'youtube': 'https://youtube.com/results?search_query=',
        'google': 'https://google.com/search?q=',
        'github': 'https://github.com/search?q=',
        'stackoverflow': 'https://stackoverflow.com/search?q=',
        'reddit': 'https://reddit.com/search/?q=',
        'bing': 'https://bing.com/search?q=',
        'duckduckgo': 'https://duckduckgo.com/?q='
    }
    
    # Voice Settings
    VOICE_CONFIG = {
        'rate': 180,
        'volume': 0.8,
        'voice_id': 0  # 0 for male, 1 for female (if available)
    }
    
    # File Paths
    DOWNLOADS_PATH = os.path.join(os.path.expanduser('~'), 'Downloads')
    DOCUMENTS_PATH = os.path.join(os.path.expanduser('~'), 'Documents')
    DESKTOP_PATH = os.path.join(os.path.expanduser('~'), 'Desktop')
    
    # Task and Reminder Storage
    TASKS_FILE = 'jarvis_tasks.json'
    REMINDERS_FILE = 'jarvis_reminders.json'
    LOGS_FILE = 'jarvis_logs.txt'
    
    # Security Settings
    ALLOWED_COMMANDS = [
        'open', 'search', 'create', 'send', 'get', 'set', 'remind',
        'play', 'stop', 'pause', 'screenshot', 'system', 'weather',
        'email', 'whatsapp', 'code', 'file', 'folder', 'help'
    ]
    
    # Logging Configuration
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    @classmethod
    def get_app_paths(cls):
        """Get application paths based on operating system"""
        if os.name == 'nt':  # Windows
            return cls.WINDOWS_APP_PATHS
        elif os.name == 'posix':
            if os.uname().sysname == 'Darwin':  # macOS
                return cls.MAC_APP_PATHS
            else:  # Linux
                return cls.LINUX_APP_PATHS
        return {}
    
    @classmethod
    def validate_config(cls):
        """Validate configuration settings"""
        errors = []
        
        if not cls.MISTRAL_API_KEY or cls.MISTRAL_API_KEY == 'your-mistral-api-key-here':
            errors.append("❌ MISTRAL_API_KEY not set. Please set your Mistral API key.")
        
        if not cls.EMAIL_CONFIG['email']:
            errors.append("⚠️  EMAIL_ADDRESS not set. Email functionality will be limited.")
        
        if not cls.EMAIL_CONFIG['password']:
            errors.append("⚠️  EMAIL_PASSWORD not set. Email functionality will be limited.")
        
        return errors

# Create default .env file content
ENV_TEMPLATE = """# JARVIS AI Assistant Environment Variables
# Copy this to .env and fill in your actual values

# Mistral AI API Key (Required)
MISTRAL_API_KEY=your-mistral-api-key-here

# Email Configuration (Optional)
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password

# Weather API Key (Optional)
WEATHER_API_KEY=your-weather-api-key

# WhatsApp API Token (Optional)
WHATSAPP_API_TOKEN=your-whatsapp-token
"""

def create_env_file():
    """Create a template .env file if it doesn't exist"""
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write(ENV_TEMPLATE)
        print("📄 Created .env template file. Please fill in your API keys.")
    else:
        print("📄 .env file already exists.")

if __name__ == '__main__':
    # Validate configuration when run directly
    create_env_file()
    errors = Config.validate_config()
    
    if errors:
        print("⚠️  Configuration Issues Found:")
        for error in errors:
            print(f"   {error}")
    else:
        print("✅ Configuration validated successfully!")
    
    print(f"\n🔧 Current Configuration:")
    print(f"   Mistral Model: {Config.MISTRAL_MODEL}")
    print(f"   Server: {Config.HOST}:{Config.PORT}")
    print(f"   Debug Mode: {Config.DEBUG}")
    print(f"   App Paths: {len(Config.get_app_paths())} applications configured")
    print(f"   Websites: {len(Config.WEBSITES)} websites configured")