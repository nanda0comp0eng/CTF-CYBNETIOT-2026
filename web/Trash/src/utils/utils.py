import os
import uuid
import subprocess
from libarchive.zip import ZipFile

BASE_DIR = "/tmp/workspaces"

def init_base_dir():
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)

def get_user_workspace(session):
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    
    user_path = os.path.join(BASE_DIR, session['user_id'])
    extract_path = os.path.join(user_path, "files")
    
    if not os.path.exists(extract_path):
        os.makedirs(extract_path, exist_ok=True)
        with open(os.path.join(user_path, "status.py"), "w") as f:
            f.write("print('Status: System is stable.')")
            
    return user_path

def extract_archive(zip_path, extract_path):
    target_dir = os.path.join(extract_path, "files")
    if not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)
        
    with ZipFile(zip_path, mode="r") as archive:
        archive.extractall(path=target_dir)

def run_maintenance_script(workspace_path):
    script_path = os.path.join(workspace_path, "status.py")
    try:
        output = subprocess.check_output(
            ["python3", script_path], 
            stderr=subprocess.STDOUT, 
            timeout=2
        )
        return output.decode(), None
    except Exception as e:
        return None, str(e)