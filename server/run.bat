@echo off
REM Запуск бэкенда из cmd. Сначала активируй venv, потом:  run.bat
REM Останавливать сервер ТОЛЬКО через Ctrl+C в этом окне.

echo Останавливаю старые процессы uvicorn...
powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'python.exe' -and $_.CommandLine -match 'uvicorn|app.main|multiprocessing' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }" 2>nul

echo Запускаю сервер на http://localhost:8000 (Ctrl+C для остановки)...
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
