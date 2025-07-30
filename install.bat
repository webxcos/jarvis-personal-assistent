# © 2025 Sumedh Sohan - JARVIS AI Assistant
# All rights reserved. Unauthorized use is strictly prohibited.

@echo off
echo ========================================
echo    JARVIS AI Assistant - Installation
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found
python --version

echo.
echo 📦 Creating virtual environment...
python -m venv jarvis_env

echo.
echo 🔧 Activating virtual environment...
call jarvis_env\Scripts\activate.bat

echo.
echo 📥 Installing Python packages...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo 📄 Creating configuration files...
python config.py

echo.
echo 🔑 Setting up environment variables...
if not exist .env (
    echo # JARVIS AI Assistant Environment Variables> .env
    echo # Fill in your actual API keys>> .env
    echo.>> .env
    echo # Mistral AI API Key ^(Required^)>> .env
    echo MISTRAL_API_KEY=your-mistral-api-key-here>> .env
    echo.>> .env
    echo # Email Configuration ^(Optional^)>> .env
    echo EMAIL_ADDRESS=your-email@gmail.com>> .env
    echo EMAIL_PASSWORD=your-app-password>> .env
    echo.>> .env
    echo # Weather API Key ^(Optional^)>> .env
    echo WEATHER_API_KEY=your-weather-api-key>> .env
    echo.>> .env
    echo ✅ Created .env file template
) else (
    echo ✅ .env file already exists
)

echo.
echo 🚀 Creating startup scripts...

REM Create start_jarvis.bat
echo @echo off> start_jarvis.bat
echo echo Starting JARVIS AI Assistant...>> start_jarvis.bat
echo call jarvis_env\Scripts\activate.bat>> start_jarvis.bat
echo python jarvis_server.py>> start_jarvis.bat
echo pause>> start_jarvis.bat

REM Create start_frontend.bat  
echo @echo off> start_frontend.bat
echo echo Opening JARVIS Frontend...>> start_frontend.bat
echo start index.html>> start_frontend.bat

echo ✅ Created startup scripts

echo.
echo ========================================
echo        Installation Complete! 🎉
echo ========================================
echo.
echo 📋 Next Steps:
echo 1. Edit .env file and add your Mistral API key
echo 2. Run 'start_jarvis.bat' to start the backend server
echo 3. Open 'index.html' in your browser or run 'start_frontend.bat'
echo.
echo 🔑 Important:
echo - Get your Mistral API key from: https://console.mistral.ai/
echo - For email features: Use Gmail App Password, not regular password
echo - For voice: Allow microphone access in your browser
echo.
echo 📁 Files created:
echo - jarvis_env\ (Python virtual environment)
echo - .env (Environment variables - EDIT THIS!)
echo - start_jarvis.bat (Start backend server)
echo - start_frontend.bat (Open frontend)
echo.
echo 🎯 Quick Start Commands:
echo   Backend:   start_jarvis.bat
echo   Frontend:  start_frontend.bat
echo   Config:    python config.py
echo.
pause