from flask import Flask, render_template, request, make_response, abort
import subprocess
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dns')
def dns():
    name = request.args.get('url')
    bad = ['`','|','&','cat','ls','dir','tail','more','less','grep','awk','flag','"',"'"]
    if any(c in name for c in bad):
        abort(400, description="No!")
    result = subprocess.run(f"dig {name}", shell=True, capture_output=True, text=True)
    return render_template('result.html', result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=7777)
