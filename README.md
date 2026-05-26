# Python with Selenium and Robot — Test run & Allure report instructions

This document explains step-by-step how to set up the environment, run tests in this project, and generate and view an Allure report on Windows (cmd.exe and PowerShell).

> Note: the instructions are written for Windows (cmd.exe / PowerShell). If you use another OS, adapt the commands accordingly.

---

## Table of contents
- Requirements
- Quick start (commands)
- Creating and activating a virtualenv
- Installing dependencies
- Running tests (all / single)
- Generating an Allure report (several ways)
- Helper script `run_allure.cmd`
- Troubleshooting: Allure in venv / PowerShell
- Additional tips and CI
- Running Robot Framework tests (English)

---

## Requirements
- Python 3.10+ (3.11/3.12 recommended)
- pip
- Google Chrome + chromedriver (if you run tests on Chrome) or another browser + driver
- (optional) Chocolatey or Scoop to install Allure CLI

---

## Quick start (most important commands)
In the project root (where `pytest.ini` / `requirements.txt` is located):

1) Create and activate a virtual environment (cmd.exe):

```bat
python -m venv .venv
.\.venv\Scripts\activate
```

(Or PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2) Install dependencies:

```bash
pip install -r requirements.txt
```

3) Run all tests and save results to `allure-results` folder:

```bash
pytest -q --alluredir=allure-results
```

4) Generate and open the HTML report (if Allure CLI is available in PATH):

```bash
allure generate allure-results -o allure-report --clean
allure open allure-report
```

If Allure is not in PATH, see the "Generating Allure report — alternatives" section below.

---

## Creating and activating virtualenv (details)
1. Create the virtualenv in the project folder:

```bat
python -m venv .venv
```

2. Activate the environment:

- cmd.exe:

```bat
.\.venv\Scripts\activate
```

- PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

After activation the prompt should show `(.venv)`.

---

## Installing dependencies
Assuming the project contains `requirements.txt` in the root:

```bash
pip install -r requirements.txt
```

If `allure-pytest` is not included in your requirements, install it manually:

```bash
pip install allure-pytest
```

---

## Running tests
- Run all tests:

```bash
pytest -q
```

- Run a single test file:

```bash
pytest -q test\test_homePage.py
```

- Run a single test within a file:

```bash
pytest -q test\test_homePage.py::TestHomepage::test_checkbox_then_verify
```

To save results in Allure format (required to generate the Allure report):

```bash
pytest -q --alluredir=allure-results
```

---

## Generating an Allure report — alternatives
Three approaches are shown below: (A) when `allure` is in PATH, (B) use the full path to the binary, (C) use the helper script.

A) If Allure CLI is available in PATH (global):

```bash
allure generate allure-results -o allure-report --clean
allure open allure-report
```

B) If Allure CLI is not in PATH — use the full path to `allure.bat` (example for your local install):

```bat
"C:\Users\Asus\Documents\allure\bin\allure.bat" generate allure-results -o allure-report --clean
"C:\Users\Asus\Documents\allure\bin\allure.bat" open allure-report
```

C) Quick preview (serve):

```bat
"C:\Users\Asus\Documents\allure\bin\allure.bat" serve allure-results
```

D) Open static HTML report without Allure CLI (if already generated):

```bat
start "" "%cd%\allure-report\index.html"
```

---

## Helper script `run_allure.cmd`
The repository includes `run_allure.cmd` — a helper that runs pytest with `--alluredir`, tries to locate Allure in several common locations (including `C:\Users\Asus\Documents\allure\bin`), generates the `allure-report` and opens it.

Run it from cmd.exe:

```bat
cmd /c run_allure.cmd
```

The script will attempt to automatically detect Allure; if not found, it prints installation instructions.

---

## Troubleshooting: `allure` not recognized in venv / PowerShell
If `allure --version` works in a fresh cmd window but after activating virtualenv or when using PowerShell you get:

```
allure : The term 'allure' is not recognized ...
```

try one of the following solutions:

1. Wrappers in the venv (already added): the `.venv\Scripts` folder contains `allure.cmd` and `allure.ps1` wrappers that forward calls to `C:\Users\Asus\Documents\allure\bin\allure.bat`. After activating the venv, `allure` should work.

2. Run Allure by full path (no PATH changes required):

```powershell
& "C:\Users\Asus\Documents\allure\bin\allure.bat" --version
```

3. If PowerShell blocks `.ps1` execution, run temporarily bypassing policy:

```powershell
powershell -ExecutionPolicy Bypass -NoProfile -Command ".\.venv\Scripts\Activate.ps1; & '$env:USERPROFILE\Documents\allure\bin\allure.bat' generate allure-results -o allure-report --clean; & '$env:USERPROFILE\Documents\allure\bin\allure.bat' open allure-report"
```

4. Permanent fix: add `C:\Users\Asus\Documents\allure\bin` to system PATH (Control Panel → System → Advanced system settings → Environment Variables) or via command:

```bat
setx PATH "%PATH%;C:\Users\Asus\Documents\allure\bin"
```

(After `setx` open a new terminal window for changes to take effect.)

---

## Additional tips
- If `allure generate` does not create a report, verify that `allure-results` contains `.json` files. If not, rerun pytest with `--alluredir`.
- In CI: install Allure CLI in the runner (choco/scoop or Docker) and publish the generated report as a build artifact.

---

## Running Robot Framework tests (English)
A short, practical guide to run Robot Framework tests from the project's virtual environment on Windows.

Basic steps (cmd.exe):

1. Activate the virtual environment:

```bat
.\.venv\Scripts\activate
```

2. Run a single Robot test file and save Robot results to `results` folder:

```bat
.\.venv\Scripts\python.exe -m robot -d results robot_tests\test_api_robot.robot
```

3. Run all Robot tests in the `robot_tests` directory:

```bat
.\.venv\Scripts\python.exe -m robot -d results robot_tests
```

Alternate: if `robot.bat` is available in the venv scripts, you can run:

```bat
.\.venv\Scripts\robot.bat -d results robot_tests\test_api_robot.robot
```

PowerShell examples:

```powershell
# activate
.\.venv\Scripts\Activate.ps1

# run a single file
.\.venv\Scripts\python.exe -m robot -d results robot_tests\test_api_robot.robot
```

Generating Allure-compatible results from Robot (optional):

- If you want to collect results for Allure, install the adapter and run Robot with the listener:

```powershell
pip install allure-robotframework
.\.venv\Scripts\python.exe -m robot --listener allure_robotframework -d allure-results robot_tests
```

- After tests create `allure-results`, generate and view the report using the Allure CLI (see earlier "Generating an Allure report" section). If Allure CLI is not in PATH, use the full path to your local Allure installation (example):

```bat
"C:\Users\Asus\Documents\allure\bin\allure.bat" serve allure-results
```

Notes and troubleshooting
- If you get "No keyword..." errors, ensure `robotframework-requests` (or other libraries used by your Robot tests) are installed in `.venv`:

```powershell
.\.venv\Scripts\pip.exe install robotframework-requests
```

- If `.venv\Scripts\robot.bat` is missing, prefer `python -m robot` as shown above.

---
