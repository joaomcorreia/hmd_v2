@echo off
REM deploy_production.bat - Deploy to main production domain (Windows)

echo 🚀 Deploying HMD to Production Environment...

REM Configuration
set PRODUCTION_HOST=hmdklusbedrijf.nl

REM Safety check
echo ⚠️  WARNING: This will deploy to PRODUCTION!
echo 🌐 Domain: %PRODUCTION_HOST%
echo.
set /p confirm="Are you sure you want to continue? (yes/no): "
if /i not "%confirm%"=="yes" (
    echo ❌ Deployment cancelled.
    exit /b 1
)

echo 📦 Installing dependencies...
python -m pip install -r requirements.txt
if %errorlevel% neq 0 goto :error

echo 🗃️  Running database migrations...
python manage.py migrate
if %errorlevel% neq 0 goto :error

echo 📁 Collecting static files...
python manage.py collectstatic --noinput
if %errorlevel% neq 0 goto :error

echo 🔍 Running deployment checks...
python manage.py check --deploy
if %errorlevel% neq 0 goto :error

echo ✅ Production deployment complete!
echo 🌐 Site should be available at: https://%PRODUCTION_HOST%
echo.
echo 🎉 Your HMD website is now live in production!
echo 📊 Monitor the following:
echo   - Server logs for any errors
echo   - Site performance and loading times
echo   - All functionality works as expected
goto :end

:error
echo ❌ Deployment failed! Check the error messages above.
exit /b 1

:end
pause