from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import json
app = Flask(__name__)


@app.route('/upload')
def upload_file():
    return render_template('upload_test.html')


@app.route('/uploader', methods=['GET', 'POST'])
def uploader_file():
    if request.method == "POST":
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return 'file uploaded successfully'


@app.route('/yaml_test', methods=['POST'])
def test():
    print(request.get_json())
    return {'message': ' '}


if __name__ == '__main__':
    app.run(debug=True)
