import os
import webbrowser
import time

print("🚀 Launching Stellar Dance Streamlit app...")

# Automatically open the web browser to the Streamlit URL
time.sleep(1)
webbrowser.open("http://localhost:8501")

# Run Streamlit app
os.system("streamlit run app.py")
