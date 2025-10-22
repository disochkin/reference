@echo off
REM Перемещение в корневую директорию проекта
cd /d %~dp0

REM Активируем виртуальное окружение (если используется)
call .\.venv\Scripts\activate.bat

REM Запускаем uvicorn с указанием модуля и имени переменной приложения
.\.venv\Scripts\uvicorn app:app --host 127.0.0.1 --port 8000

pause