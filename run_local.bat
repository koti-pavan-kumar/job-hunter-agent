@echo off
echo ========================================
echo Job Hunter Agent - Local Mode
echo ========================================
echo.
echo This will start the web app on your PC.
echo You can then login to platforms and run the agent.
echo.
echo Press any key to start...
pause > nul

cd /d "%~dp0"

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting local web server...
echo Open http://localhost:8501 in your browser
echo.
streamlit run app.py --server.port 8501
