@echo off
setlocal
REM run_allure.cmd - Run pytest with Allure results, generate report and open it (Windows cmd.exe)
REM Usage: activate your virtualenv, then run: run_allure.cmd

REM 1) Run tests and output Allure results
echo Running pytest and writing Allure results to .\allure-results
pytest -q --alluredir=allure-results
set pytest_ret=%ERRORLEVEL%

REM 2) Resolve Allure CLI command
if defined ALLURE_CMD (
    echo Using ALLURE_CMD from environment: %ALLURE_CMD%
    goto GENERATE
)

REM Try to find allure via where.exe and capture the first result
for /f "usebackq delims=" %%A in (`where.exe allure 2^>nul`) do (
    if not defined ALLURE_CMD set "ALLURE_CMD=%%A"
)
if defined ALLURE_CMD goto GENERATE

REM If where failed, try common locations
if exist "%ProgramData%\chocolatey\bin\allure.bat" set "ALLURE_CMD=%ProgramData%\chocolatey\bin\allure.bat"
if defined ALLURE_CMD goto GENERATE

if exist "%USERPROFILE%\scoop\shims\allure.cmd" set "ALLURE_CMD=%USERPROFILE%\scoop\shims\allure.cmd"
if defined ALLURE_CMD goto GENERATE

if exist "%USERPROFILE%\scoop\apps\allure\current\bin\allure.exe" set "ALLURE_CMD=%USERPROFILE%\scoop\apps\allure\current\bin\allure.exe"
if defined ALLURE_CMD goto GENERATE

if exist "C:\tools\allure\bin\allure.bat" set "ALLURE_CMD=C:\tools\allure\bin\allure.bat"
if defined ALLURE_CMD goto GENERATE

REM User-provided location: Documents\allure
if exist "%USERPROFILE%\Documents\allure\bin\allure.bat" set "ALLURE_CMD=%USERPROFILE%\Documents\allure\bin\allure.bat"
if not defined ALLURE_CMD if exist "C:\Users\Asus\Documents\allure\bin\allure.bat" set "ALLURE_CMD=C:\Users\Asus\Documents\allure\bin\allure.bat"
if defined ALLURE_CMD goto GENERATE

REM Fallback: use PowerShell to resolve the command (handles shims/aliases visible to PowerShell)
for /f "usebackq delims=" %%P in (`powershell -NoProfile -Command "try{ $c = Get-Command allure -ErrorAction Stop; if ($c -and $c.Source) { Write-Output $c.Source } elseif ($c -and $c.Path) { Write-Output $c.Path } else { exit 1 } } catch { exit 1 }" 2^>nul`) do (
    if not defined ALLURE_CMD set "ALLURE_CMD=%%P"
)
if defined ALLURE_CMD goto GENERATE

echo.
echo Allure CLI not found in PATH or common locations.
echo Install it via Chocolatey (Admin):  choco install allure -y
echo OR via Scoop (PowerShell):  scoop install allure
echo OR download from: https://github.com/allure-framework/allure2/releases and add its "bin" to PATH
echo After installation make sure the `allure` command is available in cmd.exe.
echo.
echo Exiting without generating report.
exit /b 1

:GENERATE
echo Using Allure command: %ALLURE_CMD%

REM 3) Generate the report
echo Generating Allure report in .\allure-report
"%ALLURE_CMD%" generate allure-results -o allure-report --clean
if %ERRORLEVEL% NEQ 0 (
    echo Failed to generate Allure report. Check contents of allure-results.
    exit /b 2
)

REM 4) Open the report
echo Opening Allure report
"%ALLURE_CMD%" open allure-report

endlocal & exit /b %pytest_ret%
