# Job Hunter Agent - Web Interface Launcher
# Windows PowerShell Script

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "           JOB HUNTER AGENT - WEB INTERFACE" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Starting web application..." -ForegroundColor Green
Write-Host ""
Write-Host "Once started, open your browser and go to:" -ForegroundColor Yellow
Write-Host "  http://localhost:8501"
Write-Host ""
Write-Host "Press Ctrl+C to stop." -ForegroundColor Red
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

pip install -r requirements_web.txt
streamlit run app.py

Read-Host "Press Enter to exit"
