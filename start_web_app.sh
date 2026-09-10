#!/bin/bash

# Job Hunter Agent - Web Interface Launcher
# Linux/Mac Bash Script

echo "============================================================"
echo "           JOB HUNTER AGENT - WEB INTERFACE"
echo "============================================================"
echo ""
echo "Starting web application..."
echo ""
echo "Once started, open your browser and go to:"
echo "  http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop."
echo "============================================================"
echo ""

pip3 install -r requirements_web.txt
streamlit run app.py
