set VENV_PATH=.venv

IF NOT EXIST %VENV_PATH% (
	echo create new venv at %VENV_PATH%...
    py -m venv %VENV_PATH%
)

%VENV_PATH%\Scripts\pip.exe install -r requirements.txt

cls

%VENV_PATH%\Scripts\python.exe main.py