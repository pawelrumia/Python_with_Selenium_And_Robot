@echo off
REM Wrapper to forward Allure CLI calls to user's installation
SET "USER_ALLURE=%USERPROFILE%\Documents\allure\bin\allure.bat"
if exist "%USER_ALLURE%" (
    "%USER_ALLURE%" %*
) else (
    echo Allure not found at %USER_ALLURE%
    exit /b 1
)

