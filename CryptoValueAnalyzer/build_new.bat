@echo off
echo Building new executable from crypto_analyzer_clean.py...
.venv\Scripts\python.exe -m PyInstaller --onefile --noconsole --name=CryptoValueAnalyzer crypto_analyzer_clean.py
echo Build complete! Check dist folder.
pause 