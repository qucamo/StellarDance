Stellar Dance is an interactive app that visualizes gravitational interactions in binary and triple star systems.
It combines a Streamlit web UI with a Pygame desktop simulation window. Star parameters can be set manually, picked from presets, or loaded from NASA Exoplanet Archive (PS/PSComppars) and SIMBAD. An Education Mode (FAQ/quiz/glossary) is included.

Table of Contents

Project Architecture

Features

Requirements

Installation & Run

A. Prebuilt EXE

B. From Source

Build EXE (PyInstaller)

Usage

Configuration (user_stars.json)

Troubleshooting

Repository Structure

License & Credits

Project Architecture

start.py — launcher.

Finds a free port, programmatically starts the Streamlit server, and opens a browser after the server is healthy.

Works both from source and as a bundled EXE.

app.py — Streamlit UI.

Choose system type (2/3 stars), presets, manual inputs, and see the “Current Star Parameters” panel.

Load parameters from NASA PS/PSComppars and SIMBAD (auto-syncs to input widgets).

Button to start the external simulation (writes user_stars.json and launches gravity.py).

Education Mode: FAQ, mini-quiz, glossary, quick Q&A.

Starry background (CSS) for a clean dark UI.

gravity.py — Pygame simulator.

Reads user_stars.json (mass, radius, color, number of stars, time speed).

Simulates 2–3 bodies with orbit visualization and guards against numerical blow-ups.

Exits cleanly (no sys.exit()), so it plays nicely with Streamlit.

Features

Binary/Triple modes (2 or 3 stars).

Presets: Sun, Sirius A/B, Betelgeuse, Proxima Centauri, Rigel.

NASA PS/PSComppars: load st_mass and st_rad by hostname.

SIMBAD: estimate mass/radius by spectral type (O–M).

Manual editing:

Mass (kg), Radius (m), Color for each star.

+/- step for numeric fields = 10,000,000 (fast adjustments).

Live “📊 Current Star Parameters” panel (always reflects up-to-date values).

⏱ Time Speed slider: 1000…70000.

Launches external Pygame simulation window.

Education Mode: FAQ, Quiz, Glossary, quick Q&A.

Dark theme with starfield background.

Requirements

Windows 10/11 x64 (primary target).

From source: Python 3.11+.

Internet required for NASA/SIMBAD lookups.

(Sometimes) Microsoft Visual C++ Redistributable 2015–2022 (x64) if the EXE complains about vcruntime*.dll.

Installation & Run
A. Prebuilt EXE

Download the ZIP of the build: dist/start/.

Extract (e.g., to C:\Apps\StellarDance\start\).

Run start.exe.

If SmartScreen warns: More info → Run anyway.

Allow local firewall access if prompted.

Your browser opens automatically at http://127.0.0.1:<port>.

No other installation is required for the EXE.

B. From Source
# go to project folder
cd C:\Users\nuras\Downloads\NASAspaceapps

# (if scripts are restricted)
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# create & activate venv
python -m venv .venv
.\.venv\Scripts\activate

# install dependencies
pip install --upgrade pip
pip install -r requirements.txt
# if you don't have the file:
# pip install streamlit pygame pandas numpy astroquery astropy matplotlib certifi requests

# launch the app (the launcher will open the browser when ready)
python start.py


Alternative (run Streamlit directly):

python -m streamlit run app.py --server.port 8501 --server.headless true

Build EXE (PyInstaller)
pyinstaller --noconfirm --clean --onedir --windowed ^
  --add-data "app.py;." ^
  --add-data "gravity.py;." ^
  --add-data "user_stars.json;." ^
  start.py


Output: dist\start\start.exe.

If pyinstaller is missing:

pip install pyinstaller

Usage

Select system: Binary (2) or Triple (3).

Set star parameters:

Presets — apply to Star 1/2/3.

NASA — enter hostname (e.g., Kepler-10, HD 209458) and apply.

SIMBAD — enter object name (e.g., Vega, Rigel) and apply.

Custom — edit Mass (kg) and Radius (m) manually.
The +/- step is 10,000,000 for fast changes.

Check 📊 Current Star Parameters — it reflects the latest values.

Set ⏱ Time Speed (1000…70000).

Press “🚀 Launch Pygame Window” to run the simulation.

On cloud platforms (e.g., Streamlit Community Cloud) an external Pygame window is not available — use local run or EXE.

Configuration (user_stars.json)

Created automatically by app.py before launching gravity.py.

Binary example

{
  "system_type": "binary",
  "time_speed": 5000,
  "stars": [
    {"mass": 1.989e30, "radius": 6.957e8, "color": "#FFD700"},
    {"mass": 2.06e30,  "radius": 1.71e9,  "color": "#BFD9FF"}
  ]
}


Triple example

{
  "system_type": "triple",
  "time_speed": 12000,
  "stars": [
    {"mass": 1.989e30, "radius": 6.957e8, "color": "#FFD700"},
    {"mass": 4.0e30,   "radius": 2.2e9,   "color": "#87CEFA"},
    {"mass": 1.2e30,   "radius": 8.0e8,   "color": "#FF6F91"}
  ]
}

Troubleshooting

Browser shows “127.0.0.1 refused to connect”
Use start.py or start.exe. The launcher opens the browser only after the server is healthy. If running Streamlit directly, give it a moment to start.

NASA query failed
Uses the Planetary Systems tables (PS/PSComppars). Try exact hostname (e.g., HD 209458, Kepler-10). Internet required.

SIMBAD: Not found
Check spelling. For rare objects without a spectral type, defaults are used (G-type).

EXE fails / missing DLL
Install Microsoft Visual C++ Redistributable 2015–2022 (x64).

Antivirus blocks EXE
Add to exceptions or confirm run (SmartScreen → “Run anyway”).

Port is in use
start.py picks a free port automatically (8501–8600). Close other instances or apps holding the port.

Repository Structure
.
├── app.py            # Streamlit UI
├── gravity.py        # Pygame simulation engine
├── start.py          # Launcher (starts Streamlit and opens the browser)
├── requirements.txt  # Dependencies
├── user_stars.json   # Simulation config (auto-generated)
└── README.md


Example requirements.txt:

streamlit
pygame
pandas
numpy
astroquery
astropy
matplotlib
certifi
requests

License & Credits

License: MIT (or update to your preferred license).

Credits: NASA Exoplanet Archive and SIMBAD for open data; the Stellar Dance team
