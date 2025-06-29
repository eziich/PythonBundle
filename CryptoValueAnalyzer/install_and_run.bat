@echo off
echo Installing required packages...
.venv\Scripts\python.exe -m pip install requests matplotlib pandas numpy scikit-learn seaborn

echo.
echo Running Crypto Analyzer...
.venv\Scripts\python.exe crypto_analyzer.py

pause 