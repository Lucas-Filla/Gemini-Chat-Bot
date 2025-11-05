# Gemini-Terminal-App
A small personal assistant app using Google Gemini created for Ohio University's CS3560

##Usage

1) Ensure Python (3.10+) and uv are installed
```
//for uv
curl -LsSf https://astral.sh/uv/install.sh | sh
```
2) Initialize current folder as uv workspace
3) Initialize virtual python environment
```
uv init .
uv venv
```
4) Install **both** google-genai and PIL (Preferably through a virtual environment)
```
uv pip install -q -U google-genai
uv pip install pillow
```
5) Export your Gemini Api Key (Image generation only works with paid key)
```
// Mac & Linux
export GEMINI_API_KEY="YOUR_KEY"
// Windows Powershell
$env:GEMINI_API_KEY = "YOUR_KEY"
```
6) Use it!
```
uv run main.py
```
