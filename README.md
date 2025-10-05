Description

Stellar Dance is an interactive application for visualizing the gravitational interaction of binary and triple star systems.
The project consists of a web interface on Streamlit and a separate simulation window on Pygame. The star parameters can be set manually, selected from presets, or downloaded from the NASA Exoplanet Archive (PS/PSComppars) and SIMBAD databases. There is a learning mode (FAQ/quiz/glossary).

Project architecture

The application is divided into three key files:

start.py — entry point (launcher).

Finds a free port, programmatically starts the Streamlit server and opens the browser when the server is ready.

It works both from source and as an EXE (PyInstaller).

app.py — Web interface (Streamlit).

UI: system selection (2/3 stars), presets, parameter input, "Current parameters" section.

Data sources: NASA PS/PSComppars, SIMBAD (auto-synchronization with input fields).

The button to start an external simulation (creates user_stars.json and causes gravity.py ).

Study mode: FAQs, Quiz, Glossary, quick answers on key terms.

gravity.py — simulator (Pygame).

Reads the user_stars config.json (mass, radius, color, number of stars, speed of time).

Simulates pairs/triples with visualization and protection against numerical "explosions".

It terminates correctly (without sys.exit()) so as not to conflict with Streamlit.

Opportunities

System selection: double or triple.

Setting the parameters of each star:

Presets (Sun, Sirius A/B, Betelgeuse, Proxima Centauri, Rigel).

NASA Exoplanet Archive (PS/PSComppars) — mass-radius parameters by hostname.

SIMBAD is a spectral type estimate (mass/radius according to the O–M map).

Manual input (the step of the +/- buttons for fields is 10,000,000 for quick changes).

The "📊 Current Star Parameters” section always reflects the current values.

The slider is ⏱️ Time Speed in the range of 1000...70000.

Launching a separate simulation window (Pygame) with trajectories.

Educational Mode: FAQ, mini-quiz, glossary, quick response on key terms.

Beautiful "cosmic" background and neat dark UI.

Quality and reliability

New NASA PS/PSComppars tables are used (instead of the outdated exoplanets) with fallback search logic (LIKE, NaN filtering).

Synchronization of parameters between the "model" and Streamlit widgets (so that the values are updated immediately).

Protection against numerical errors and division by zero in the gravity model.

The launcher start.py:

waits for the server to be ready (health check) before opening the browser;

it works correctly in the EXE, does not rely on python -m streamlit inside the assembly.

The simulation configuration is stored in user_stars.json for reproducibility

айдын, [05.10.2025 20:15]
Usage example

Local source startup (Windows 10/11 x64)
Requires Python 3.11+ installed.

# go to the
cd project folder C:\Users\nuras\Downloads\NASAspaceapps

# (if scripts are blocked)
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# create and activate
the python -mv environment.venv
.\.venv\Scripts\activate

# install dependencies
pip install --upgrade pip
pip install -r requirements.txt
# if there is no file, install:
# pip install streamlit pygame pandas numpy astroquery astropy matplotlib certifi requests

# launch the launcher (it will open the browser itself when ready)
python start.py


Launching the compiled version (EXE)

Unpack the dist/start/ assembly folder.

Launch start.exe (with SmartScreen: "Advanced → Execute").

The browser will open automatically; if not— open http://127.0.0.1:8501 .

Parameter management

In the UI, select Binary or Triple.

Set the parameters of the stars:

via Presets / NASA /SIMBAD (Internet is required for NASA/SIMBAD);

or manually (fields "Mass (kg)" and "Radius (m)"; step +/- = 10,000,000).

Click “🚀 Launch Pygame Window” to launch the simulation in a separate window.

Note: The Pygame window is not available in a cloud environment (Streamlit Community Cloud). Use a local launcher or EXE. The Internet is required for NASA/SIMBAD; presets and manual input are available without it.

# Quick start (briefly)
python -mv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python start.py
