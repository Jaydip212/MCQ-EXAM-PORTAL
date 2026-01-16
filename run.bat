@echo off
echo Starting MCQ Exam Portal (Django)...
echo.

echo Installing Python dependencies...
pip install -r requirements.txt
echo.

echo Installing Frontend dependencies...
cd frontend
call npm install
cd ..
echo.

echo Running Django migrations...
cd backend
python manage.py makemigrations
python manage.py migrate
cd ..
echo.

echo Starting Django Backend Server...
start cmd /k "cd backend && python manage.py runserver"

timeout /t 3

echo Starting Frontend Server...
start cmd /k "cd frontend && npm run dev"

echo.
echo Both servers are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo Admin Panel: http://localhost:8000/admin
echo.
pause
