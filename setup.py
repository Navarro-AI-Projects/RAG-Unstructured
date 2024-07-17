import os
import subprocess
import sys
from create_folders import create_directories
def setup_application():

    with open('.env', 'w') as f:
        f.write(f"GOOGLE_API_KEY=AIzaSyDOwjhFu5JiIacrkOZ_AGrxG0hbuNrHkmA")

    # Get the path to the current directory
    current_dir = os.path.dirname(os.path.realpath(__file__))
    documents_index_path, local_qdrant_path = create_directories()

    # Create a virtual environment
    venv_dir = os.path.join(current_dir, ".venv")
    subprocess.run([sys.executable, "-m", "venv", venv_dir])

    # Install requirements
    #pip_path = os.path.join(venv_dir, "bin", "pip" if os.name != 'nt' else "Scripts\\pip.exe")
    # pip_path = os.path.join(venv_dir, "bin" if os.name != 'nt' else "Scripts", "pip" if os.name != 'nt' else "pip.exe")
    # requirements_path = os.path.join(current_dir, "requirements.txt")
    # subprocess.run([pip_path, "install", "-r", requirements_path])

    # Run the api.py script
    python_path = os.path.join(venv_dir, "bin" if os.name != 'nt' else "Scripts", "python" if os.name != 'nt' else "python.exe")
    api_path = os.path.join(current_dir, "main.py")
    api_process = subprocess.Popen([python_path, api_path])

    # Start the Streamlit application in a new terminal
    streamlit_path = os.path.join(venv_dir, "bin" if os.name != 'nt' else "Scripts", "streamlit" if os.name != 'nt' else "streamlit.exe")
    ui_path = os.path.join(current_dir, "user_interface.py")
    if os.name == 'nt':
        streamlit_process = subprocess.Popen(["start", "cmd", "/k", streamlit_path, "run", ui_path], shell=True)
    else:
        streamlit_process = subprocess.Popen(["gnome-terminal", "--", streamlit_path, "run", ui_path])

    # Wait for both processes to finish
    api_process.wait()
    streamlit_process.wait()

if __name__ == "__main__":
    setup_application()