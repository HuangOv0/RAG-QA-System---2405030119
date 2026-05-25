import subprocess
import os

os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
subprocess.run(['streamlit', 'run', 'streamlit_app.py', '--server.port', '8501'])