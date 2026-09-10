# Job Hunter Agent - Autonomous Mode Launcher
# Windows PowerShell Script

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "           JOB HUNTER AGENT - AUTONOMOUS MODE" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Starting fully autonomous job hunter..." -ForegroundColor Green
Write-Host ""
Write-Host "This agent will:" -ForegroundColor Yellow
Write-Host "  - Search jobs at 8:00 AM and 6:00 PM daily"
Write-Host "  - Check company legitimacy automatically"
Write-Host "  - Generate tailored resumes for matching jobs"
Write-Host "  - Generate cover letters"
Write-Host "  - Save everything in 'job_hunter/resumes/' folder"
Write-Host ""
Write-Host "You just need to:" -ForegroundColor Yellow
Write-Host "  1. Check the 'job_hunter/resumes/' folder"
Write-Host "  2. Review the generated resumes"
Write-Host "  3. Apply to the ones you like when you have time"
Write-Host ""
Write-Host "Press Ctrl+C to stop." -ForegroundColor Red
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

python -m job_hunter run --immediate

Read-Host "Press Enter to exit"
