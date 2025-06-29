@echo off
echo Installing PyInstaller...
.venv\Scripts\python.exe -m pip install pyinstaller

echo.
echo Building executable...
.venv\Scripts\python.exe -m PyInstaller --onefile --noconsole --hidden-import=sklearn.neighbors.typedefs --hidden-import=sklearn.neighbors.quad_tree --hidden-import=sklearn.tree._utils --exclude-module=seaborn --name=CryptoValueAnalyzer crypto_analyzer.py

echo.
echo Build complete! Check the dist folder for CryptoValueAnalyzer.exe
pause 