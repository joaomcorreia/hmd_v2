@echo off
REM deployment_staging.bat - Deploy to staging subdomain (Windows)

echo 🚀 Deploying HMD to Staging Environment...

REM Configuration
set STAGING_HOST=test3.hmdklusbedrijf.nl

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

echo ✅ Staging deployment complete!
echo 🌐 Site should be available at: https://%STAGING_HOST%
echo.
echo 🧪 Test the following before moving to production:
echo   - Admin interface: https://%STAGING_HOST%/admin/
echo   - Homepage and all pages load correctly
echo   - Static files (CSS/JS/images) load properly
echo   - Contact forms work
echo   - All admin tools function correctly
goto :end

:error
echo ❌ Deployment failed! Check the error messages above.
exit /b 1

:end
pause