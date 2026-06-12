# Чистый запуск бэкенда: сначала убивает зависшие uvicorn-воркеры на порту 8000,
# затем стартует сервер. Запуск:  .\run.ps1   (из папки server)

Write-Host "Останавливаю старые процессы сервера..." -ForegroundColor Yellow
Get-CimInstance Win32_Process -Filter "Name='python.exe' OR Name='pythonw.exe'" |
  Where-Object { $_.CommandLine -match 'uvicorn|app\.main|multiprocessing' } |
  ForEach-Object {
    Write-Host "  kill PID $($_.ProcessId)"
    taskkill /F /T /PID $_.ProcessId 2>&1 | Out-Null
  }
Start-Sleep -Seconds 1

Write-Host "Запускаю сервер на http://localhost:8000 ..." -ForegroundColor Green
Write-Host "Останавливать ТОЛЬКО через Ctrl+C в этом окне!" -ForegroundColor Cyan
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
