import subprocess
import os
import sys

os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
os.environ['STREAMLIT_SERVER_EMAIL'] = ''

subprocess.Popen([
    sys.executable, '-m', 'streamlit', 'run',
    'streamlit_app.py',
    '--server.port', '8501',
    '--server.headless', 'true',
    '--browser.gatherUsageStats', 'false'
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("Streamlit应用已启动，请在浏览器中访问 http://localhost:8501")
