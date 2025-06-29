@echo off
echo Installing PyInstaller...
.venv\Scripts\python.exe -m pip install pyinstaller

echo.
echo Building executable (simplified)...
.venv\Scripts\python.exe -m PyInstaller --onefile --noconsole --exclude-module=seaborn --exclude-module=scipy --name=CryptoValueAnalyzer crypto_analyzer_clean.py

echo.
echo Build complete! Check the dist folder for CryptoValueAnalyzer.exe
pause 