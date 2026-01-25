import os
from flask import Flask, request, session, render_template, redirect, url_for
from utils import utils

app = Flask(__name__)
app.secret_key = os.urandom(24)

utils.init_base_dir()

@app.route('/')
def index():
    ws_id = session.get('user_id', 'New Session')
    return render_template('index.html', ws_id=ws_id)

@app.route('/upload', methods=['POST'])
def upload():
    ws = utils.get_user_workspace(session)
    if 'file' not in request.files:
        return render_template('index.html', error="No file part", ws_id=session['user_id'])
    
    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', error="No selected file", ws_id=session['user_id'])

    zip_path = os.path.join(ws, "upload.zip")
    file.save(zip_path)

    try:
        utils.extract_archive(zip_path, ws)
        return render_template('index.html', msg="Archive deployed to workspace!", ws_id=session['user_id'])
    except Exception as e:
        return render_template('index.html', error=f"Extraction failed: {str(e)}", ws_id=session['user_id'])

@app.route('/run')
def run():
    ws = utils.get_user_workspace(session)
    output, error = utils.run_maintenance_script(ws)
    
    if error:
        return render_template('index.html', error=error, ws_id=session['user_id'])
    return render_template('index.html', output=output, ws_id=session['user_id'])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)