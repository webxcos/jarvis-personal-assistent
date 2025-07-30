# © 2025 Sumedh Sohan - JARVIS AI Assistant
# All rights reserved. Unauthorized use is strictly prohibited.

#!/usr/bin/env python3
"""
JARVIS AI Assistant Backend
Powered by Mistral AI API with system control capabilities
"""

import os
import json
import subprocess
import webbrowser
import smtplib
import threading
import time
import re
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify
from flask_cors import CORS
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import psutil
import requests

app = Flask(__name__)
CORS(app)

class JarvisBackend:
    def __init__(self):
        # Initialize Mistral client
        self.mistral_api_key = os.getenv('MISTRAL_API_KEY', 'your-mistral-api-key-here')
        self.mistral_client = MistralClient(api_key=self.mistral_api_key)
        self.model = "mistral-large-latest"
        
        # Task and reminder storage
        self.tasks = []
        self.reminders = []
        
        # Email configuration
        self.email_config = {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'email': os.getenv('EMAIL_ADDRESS', ''),
            'password': os.getenv('EMAIL_PASSWORD', '')
        }
        
        # System paths
        self.app_paths = {
            'notepad': 'notepad.exe',
            'calculator': 'calc.exe',
            'task manager': 'taskmgr.exe',
            'spotify': 'spotify.exe',
            'chrome': r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            'firefox': r'C:\Program Files\Mozilla Firefox\firefox.exe',
            'vscode': r'C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe'
        }
        
        print("🤖 JARVIS Backend initialized successfully!")
    
    def get_mistral_response(self, user_input):
        """Get response from Mistral AI"""
        try:
            system_prompt = """You are JARVIS, an advanced AI assistant inspired by Iron Man's AI. You are helpful, intelligent, and speak in a sophisticated but friendly manner. Address the user as 'Sir' occasionally.

You can help with:
- Opening websites and applications
- Searching the internet
- Creating code and files
- Managing tasks and reminders
- Sending emails and messages
- Controlling system functions
- Answering questions and providing information

Always provide helpful, accurate responses. If asked to perform actions, acknowledge them and provide clear instructions."""

            messages = [
                ChatMessage(role="system", content=system_prompt),
                ChatMessage(role="user", content=user_input)
            ]
            
            response = self.mistral_client.chat(
                model=self.model,
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"❌ Mistral API error: {e}")
            return f"I apologize, Sir. I'm experiencing some technical difficulties with my AI processing. Error: {str(e)}"
    
    def analyze_command(self, command):
        """Analyze command and determine actions"""
        command_lower = command.lower().strip()
        actions = []
        
        # Website opening patterns
        website_patterns = {
            'youtube': 'https://youtube.com',
            'google': 'https://google.com',
            'instagram': 'https://instagram.com',
            'facebook': 'https://facebook.com',
            'twitter': 'https://twitter.com',
            'linkedin': 'https://linkedin.com',
            'github': 'https://github.com',
            'reddit': 'https://reddit.com',
            'chatgpt': 'https://chat.openai.com',
            'claude': 'https://claude.ai',
            'stackoverflow': 'https://stackoverflow.com',
            'gmail': 'https://gmail.com',
            'whatsapp': 'https://web.whatsapp.com'
        }
        
        # Check for website opening commands
        for site_name, url in website_patterns.items():
            if f'open {site_name}' in command_lower:
                actions.append({
                    'type': 'open_website',
                    'url': url,
                    'site': site_name
                })
                break
        
        # Search patterns
        search_patterns = {
            'youtube': 'https://youtube.com/results?search_query=',
            'google': 'https://google.com/search?q=',
            'github': 'https://github.com/search?q=',
            'stackoverflow': 'https://stackoverflow.com/search?q='
        }
        
        # Check for search commands
        for platform, base_url in search_patterns.items():
            search_match = re.search(f'search {platform}.*?for (.+)', command_lower)
            if not search_match:
                search_match = re.search(f'search on {platform}.*?for (.+)', command_lower)
            if not search_match:
                search_match = re.search(f'{platform} search (.+)', command_lower)
            
            if search_match:
                query = search_match.group(1).strip()
                actions.append({
                    'type': 'search',
                    'platform': platform,
                    'query': query,
                    'base_url': base_url
                })
                break
        
        # Application opening patterns
        app_patterns = {
            'notepad': ['notepad', 'text editor'],
            'calculator': ['calculator', 'calc'],
            'task manager': ['task manager', 'taskmgr'],
            'spotify': ['spotify', 'music'],
            'chrome': ['chrome', 'browser'],
            'vscode': ['vscode', 'vs code', 'code editor']
        }
        
        for app_name, keywords in app_patterns.items():
            for keyword in keywords:
                if f'open {keyword}' in command_lower or f'launch {keyword}' in command_lower:
                    actions.append({
                        'type': 'open_application',
                        'app': app_name
                    })
                    break
        
        # Code creation patterns
        if 'create code' in command_lower or 'write code' in command_lower or 'generate code' in command_lower:
            project_match = re.search(r'(?:create|write|generate) code (?:for |to )?(.+)', command_lower)
            project_type = project_match.group(1).strip() if project_match else 'general project'
            actions.append({
                'type': 'create_code',
                'project_type': project_type
            })
        
        # Email patterns
        if 'send email' in command_lower or 'email' in command_lower:
            email_match = re.search(r'send email to (.+)', command_lower)
            recipient = email_match.group(1).strip() if email_match else 'unknown'
            actions.append({
                'type': 'send_email',
                'recipient': recipient
            })
        
        # Reminder patterns
        if 'remind me' in command_lower or 'set reminder' in command_lower:
            reminder_match = re.search(r'(?:remind me|set reminder) (?:to |about )?(.+)', command_lower)
            task = reminder_match.group(1).strip() if reminder_match else 'General reminder'
            actions.append({
                'type': 'reminder',
                'message': task,
                'time': 300  # 5 minutes default
            })
        
        # Weather patterns
        if 'weather' in command_lower:
            actions.append({
                'type': 'get_weather'
            })
        
        # System control patterns
        if 'screenshot' in command_lower or 'screen capture' in command_lower:
            actions.append({
                'type': 'screenshot'
            })
        
        if 'system info' in command_lower or 'computer info' in command_lower:
            actions.append({
                'type': 'system_info'
            })
        
        return actions
    
    def execute_action(self, action):
        """Execute specific actions"""
        try:
            if action['type'] == 'open_application':
                return self.open_application(action['app'])
            elif action['type'] == 'create_code':
                return self.create_code(action['project_type'])
            elif action['type'] == 'send_email':
                return self.send_email(action['recipient'])
            elif action['type'] == 'get_weather':
                return self.get_weather()
            elif action['type'] == 'screenshot':
                return self.take_screenshot()
            elif action['type'] == 'system_info':
                return self.get_system_info()
            else:
                return "Action executed successfully."
        except Exception as e:
            return f"Error executing action: {str(e)}"
    
    def open_application(self, app_name):
        """Open system applications"""
        try:
            if app_name in self.app_paths:
                if os.name == 'nt':  # Windows
                    subprocess.Popen(self.app_paths[app_name], shell=True)
                    return f"Opening {app_name}..."
                else:  # Linux/Mac
                    subprocess.Popen(['open', self.app_paths[app_name]])
                    return f"Opening {app_name}..."
            else:
                return f"Application {app_name} not found in system."
        except Exception as e:
            return f"Failed to open {app_name}: {str(e)}"
    
    def create_code(self, project_type):
        """Generate code using Mistral AI"""
        try:
            code_prompt = f"Create a complete, functional code example for: {project_type}. Include comments and make it production-ready."
            code_response = self.get_mistral_response(code_prompt)
            
            # Save code to file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{project_type.replace(' ', '_')}_{timestamp}.py"
            
            return {
                'type': 'create_file',
                'filename': filename,
                'content': code_response
            }
        except Exception as e:
            return f"Failed to create code: {str(e)}"
    
    def send_email(self, recipient):
        """Send email (placeholder - requires email setup)"""
        try:
            if not self.email_config['email'] or not self.email_config['password']:
                return "Email not configured. Please set EMAIL_ADDRESS and EMAIL_PASSWORD in environment variables."
            
            # This is a placeholder - in real implementation, you'd compose and send the email
            return f"Email functionality ready for {recipient}. Please provide email content to send."
        except Exception as e:
            return f"Email error: {str(e)}"
    
    def get_weather(self):
        """Get weather information"""
        try:
            # You can integrate with weather APIs like OpenWeatherMap
            return "Weather functionality requires API integration. Please add your weather API key."
        except Exception as e:
            return f"Weather error: {str(e)}"
    
    def take_screenshot(self):
        """Take a screenshot"""
        try:
            if os.name == 'nt':  # Windows
                import pyautogui
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}.png"
                pyautogui.screenshot(filename)
                return f"Screenshot saved as {filename}"
            else:
                return "Screenshot functionality needs platform-specific implementation."
        except Exception as e:
            return f"Screenshot error: {str(e)}"
    
    def get_system_info(self):
        """Get system information"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            info = f"""System Information:
CPU Usage: {cpu_percent}%
Memory: {memory.percent}% used ({memory.used//1024//1024} MB / {memory.total//1024//1024} MB)
Disk: {disk.percent}% used ({disk.used//1024//1024//1024} GB / {disk.total//1024//1024//1024} GB)
"""
            return info
        except Exception as e:
            return f"System info error: {str(e)}"
    
    def process_command(self, command):
        """Main command processing function"""
        try:
            # Get AI response
            ai_response = self.get_mistral_response(command)
            
            # Analyze for actions
            actions = self.analyze_command(command)
            
            # Execute actions
            action_results = []
            for action in actions:
                if action['type'] in ['open_website', 'search']:
                    # These are handled by frontend
                    action_results.append(action)
                else:
                    result = self.execute_action(action)
                    if isinstance(result, dict):
                        action_results.append(result)
                    else:
                        action_results.append({'type': 'message', 'content': result})
            
            return {
                'response': ai_response,
                'actions': action_results,
                'status': 'success'
            }
            
        except Exception as e:
            print(f"❌ Error processing command: {e}")
            return {
                'response': f"I apologize, Sir. I encountered an error processing your request: {str(e)}",
                'actions': [],
                'status': 'error'
            }

# Initialize JARVIS
jarvis = JarvisBackend()

# Flask routes
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'JARVIS backend is operational'})

@app.route('/process_command', methods=['POST'])
def process_command():
    """Process voice commands"""
    try:
        data = request.get_json()
        command = data.get('command', '')
        
        if not command:
            return jsonify({'error': 'No command provided'}), 400
        
        print(f"🗣️  Processing command: {command}")
        result = jarvis.process_command(command)
        
        return jsonify(result)
        
    except Exception as e:
        print(f"❌ API Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/get_tasks', methods=['GET'])
def get_tasks():
    """Get current tasks"""
    return jsonify({'tasks': jarvis.tasks})

@app.route('/add_task', methods=['POST'])
def add_task():
    """Add a new task"""
    try:
        data = request.get_json()
        task = data.get('task', '')
        
        if task:
            task_obj = {
                'id': len(jarvis.tasks) + 1,
                'text': task,
                'created': datetime.now().isoformat(),
                'completed': False
            }
            jarvis.tasks.append(task_obj)
            return jsonify({'message': 'Task added successfully', 'task': task_obj})
        
        return jsonify({'error': 'No task provided'}), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/system_status', methods=['GET'])
def system_status():
    """Get system status"""
    try:
        status = jarvis.get_system_info()
        return jsonify({'status': status})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting JARVIS AI Assistant Backend...")
    print("📡 Server running on http://localhost:5000")
    print("🔑 Make sure to set your MISTRAL_API_KEY environment variable")
    print("📧 Set EMAIL_ADDRESS and EMAIL_PASSWORD for email functionality")
    print("⚡ Ready to assist!")
    
    app.run(host='0.0.0.0', port=5000, debug=True)