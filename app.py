import os
from flask import Flask, render_template, request, send_file
from flask_wtf.csrf import CSRFProtect
from flask.helpers import send_from_directory
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
csrf = CSRFProtect(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        signature_data = request.form['signature']
        save_signature(signature_data)
        return "Signature saved successfully."
    return render_template('index.html')


def save_signature(signature_data):
    signature_bytes = base64.b64decode(signature_data)
    signature_path = os.path.join(app.config['UPLOAD_FOLDER'], 'signature.jpeg')
    with open(signature_path, 'wb') as file:
        file.write(signature_bytes)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)
