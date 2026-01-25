from flask import Flask, render_template, request, make_response, abort
import pdfkit

app = Flask(__name__)

config = pdfkit.configuration(
    wkhtmltopdf=r"/usr/local/bin/wkhtmltopdf"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    name = request.form['name']
    bad = ['127.0.0.1','localhost','0.0.0.0']
    if any(x in name for x in bad):
        abort(400, description="No!")
    rendered = render_template('cert.html', name=name)
    pdf = pdfkit.from_string(rendered, False, configuration=config)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=cert_{name}.pdf'
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=3333)
