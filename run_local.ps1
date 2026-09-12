Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Job Hunter Agent - Local Mode" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "This will start the web app on your PC." -ForegroundColor Yellow
Write-Host "You can then login to platforms and run the agent." -ForegroundColor Yellow
Write-Host ""
Write-Host "Press any key to start..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Set-Location $PSScriptRoot

Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host ""
Write-Host "Starting local web server..." -ForegroundColor Green
Write-Host "Open http://localhost:8501 in your browser" -ForegroundColor Cyan
Write-Host ""
streamlit run app.py --server.port 8501
