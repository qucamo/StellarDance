import os
import subprocess
import webbrowser
import time
from pathlib import Path

project_path = Path(__file__).resolve().parent
os.chdir(project_path)

print("🚀 Launching Stellar Dance Interface...")
print(f"Project folder: {project_path}")
print("Starting Streamlit server...")

process = subprocess.Popen(
    ["python", "-m", "streamlit", "run", "app.py", "--server.headless", "true"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

time.sleep(3)

webbrowser.open("http://localhost:8501")

process.wait()


