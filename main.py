import subprocess
import sys
import os

os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'

if __name__ == '__main__':
    subprocess.run([
        sys.executable, '-m', 'streamlit', 'run', 
        'streamlit_app.py', 
        '--server.port', '8501',
        '--server.headless', 'true'
    ])