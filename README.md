# Stellar Dance

Stellar Dance is an interactive app that visualizes gravitational interactions in binary and triple star systems.
It combines a Streamlit web UI with a Pygame desktop simulation window. Star parameters can be set manually,
picked from presets, or loaded from NASA Exoplanet Archive (PS/PSComppars) and SIMBAD. An Education Mode
(FAQ, quiz, glossary) is included.

---

## Table of Contents

- [Project Architecture](#project-architecture)
- [Features](#features)
- [Requirements](#requirements)
- [Installation and Run](#installation-and-run)
  - [A. Prebuilt EXE](#a-prebuilt-exe)
  - [B. From Source](#b-from-source)
- [Build EXE with PyInstaller](#build-exe-with-pyinstaller)
- [Usage](#usage)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Repository Structure](#repository-structure)
- [License and Credits](#license-and-credits)

---

## Project Architecture

- `start.py` – launcher.
  - Finds a free port, starts the Streamlit server programmatically, and opens the browser after the server is healthy.
  - Works both from source and as a bundled EXE.

- `app.py` – Streamlit UI.
  - Choose system type (2 or 3 stars), apply presets, edit parameters, and view the Current Star Parameters panel.
  - Load parameters from NASA PS/PSComppars and SIMBAD (auto-syncs with input widgets).
  - Button to launch the external simulation (writes `user_stars.json` and starts `gravity.py`).
  - Education Mode: FAQ, quiz, glossary, quick Q&A.
  - Starfield background via CSS.

- `gravity.py` – Pygame simulator.
  - Reads `user_stars.json` (mass, radius, color, number of stars, time speed).
  - Simulates 2–3 bodies with simple visualized orbits and numeric safety guards.
  - Exits cleanly without `sys.exit()` to avoid conflicts with Streamlit.

---

## Features

- Binary and triple modes (2 or 3 stars).
- Presets: Sun, Sirius A, Sirius B, Betelgeuse, Proxima Centauri, Rigel.
- NASA PS/PSComppars: load `st_mass` and `st_rad` by `hostname`.
- SIMBAD: estimate mass and radius by spectral type (O to M).
- Manual editing for each star:
  - Mass (kg), Radius (m), Color.
  - Plus/minus step for numeric fields is 10,000,000 (fast adjustments).
- Live "Current Star Parameters" panel.
- Time Speed slider: 1000 to 70000.
- Launches an external Pygame simulation window.
- Education Mode: FAQ, quiz, glossary, quick Q&A.

---

## Requirements

- Windows 10 or 11, 64-bit.
- From source: Python 3.11 or newer.
- Internet required for NASA and SIMBAD lookups.
- In some environments: Microsoft Visual C++ Redistributable 2015–2022 (x64).

---

## Installation and Run

### A. Prebuilt EXE

1. Download the ZIP of the build: `dist/start/`.
2. Extract to a folder, for example: `C:\Apps\StellarDance\start\`.
3. Run `start.exe`.
   - If SmartScreen warns, choose "More info" and then "Run anyway".
   - Allow local firewall access if prompted.
4. Your browser will open at `http://127.0.0.1:<port>`.

No other installation is required for the EXE.

### B. From Source

powershell
  go to project folder
```
cd C:\Users\nuras\Downloads\NASAspaceapps
```
  if scripts are restricted
```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```
  create and activate a virtual environment
```
python -m venv .venv
.\.venv\Scripts\activate
```
  install dependencies
```
pip install --upgrade pip
pip install -r requirements.txt
```
  if you do not have requirements.txt:
```
pip install streamlit pygame pandas numpy astroquery astropy matplotlib certifi requests
```
  run the launcher (it opens the browser when the server is ready)
```
python start.py
Alternative: run Streamlit directly
```
```powershell

python -m streamlit run app.py --server.port 8501 --server.headless true
```
# Build EXE with PyInstaller

```powershell

pyinstaller --noconfirm --clean --onedir --windowed ^
  --add-data "app.py;." ^
  --add-data "gravity.py;." ^
  --add-data "user_stars.json;." ^
  start.py
Output will be at: dist\start\start.exe.
```
If PyInstaller is missing:

```powershell
pip install pyinstaller
```
# Usage
### Select system type: Binary (2) or Triple (3).

### Presets: 
  Choose a preset and apply it to Star 1, 2, or 3.

### NASA: 
  Enter hostname (for example, Kepler-10, HD 209458) and apply.

### SIMBAD: 
  Enter object name (for example, Vega, Rigel) and apply.

### Custom: 
  Edit Mass (kg) and Radius (m) manually. Plus/minus step is 10,000,000.
Review the "Current Star Parameters" panel to confirm values.

### Set Time Speed (1000 to 70000).

### Click "Launch Pygame Window" to run the simulation.
  Note: On cloud platforms (for example, Streamlit Community Cloud), the external Pygame window is not available. Use local run or EXE.

# Configuration
  user_stars.json is created automatically by app.py before launching gravity.py.

### Binary example:

```json

{
  "system_type": "binary",
  "time_speed": 5000,
  "stars": [
    {"mass": 1.989e30, "radius": 6.957e8, "color": "#FFD700"},
    {"mass": 2.06e30,  "radius": 1.71e9,  "color": "#BFD9FF"}
  ]
}
```
### Triple example:

```json

{
  "system_type": "triple",
  "time_speed": 12000,
  "stars": [
    {"mass": 1.989e30, "radius": 6.957e8, "color": "#FFD700"},
    {"mass": 4.0e30,   "radius": 2.2e9,   "color": "#87CEFA"},
    {"mass": 1.2e30,   "radius": 8.0e8,   "color": "#FF6F91"}
  ]
}
```
# Troubleshooting
### Browser shows: 
```
"127.0.0.1 refused to connect"
```
  Use start.py or start.exe. The launcher opens the browser only after the server reports healthy.
If running Streamlit directly, wait a few seconds or try another port.

```
NASA query failed
```
  Planetary Systems tables (PS and PSComppars). Try exact hostnames, for example HD 209458, Kepler-10. Internet required.
```
SIMBAD not found
```
  Check the object name spelling. For rare objects without a spectral type, default values are used.
```
EXE fails or reports missing DLLs
```
  Install Microsoft Visual C++ Redistributable 2015–2022 (x64).
```
Port is in use
```
  start.py automatically picks a free port between 8501 and 8600. Close other instances or apps using the port.

# Repository Structure
```
.
├── app.py            # Streamlit UI
├── gravity.py        # Pygame simulation engine
├── start.py          # Launcher
├── requirements.txt  # Dependencies
├── user_stars.json   # Auto-generated config
├── README.md
```
~~~nginx

streamlit
pygame
pandas
numpy
astroquery
astropy
matplotlib
certifi
requests
~~~
# License and Credits

This project is intended for educational and research purposes.
Data sources: NASA Exoplanet Archive (PS/PSCompPars) and SIMBAD.
