@echo off
echo ============================================================
echo           JOB HUNTER AGENT - WEB INTERFACE
echo ============================================================
echo.
echo Starting web application...
echo.
echo Once started, open your browser and go to:
echo   http://localhost:8501
echo.
echo Press Ctrl+C to stop.
echo ============================================================
echo.

pip install -r requirements_web.txt
streamlit run app.py

pause
