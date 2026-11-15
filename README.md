# homeloop

Home voice assistant – work in progress. For now it shows the microphone loudness in the terminal.

## Setup

Requires Python 3.10+ and a microphone.

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If PowerShell blocks `Activate.ps1`, run once: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

## Run

With the virtual environment activated:

```powershell
python main.py
```

Stop with `Ctrl+C`.

## Configuration

Optional `.env` file in the project root:

```
MIC_DEVICE=Realtek MME   # device index or name + audio API; empty = system default
```

List the available devices with `python -m sounddevice`.
