@echo off
echo Resetting Database and Migrations...
echo.

cd backend

echo Stopping any running Django processes...
taskkill /F /IM python.exe 2>nul

timeout /t 2

echo Deleting old database...
if exist db.sqlite3 del /F db.sqlite3

echo Deleting old migrations...
if exist api\migrations rmdir /S /Q api\migrations

echo Creating migrations folder...
mkdir api\migrations
echo. > api\migrations\__init__.py

echo.
echo Creating fresh migrations...
python manage.py makemigrations

echo.
echo Running migrations...
python manage.py migrate

echo.
echo Database reset complete!
echo.
echo You can now run: python manage.py runserver
pause
