import os
from flask import Flask, request
from werkzeug.utils import secure_filename

#upload_dir = r"C:\Users\Administrator\Desktop\docker_v\upload_dir"
upload_dir = r"/flask/upload_dir"

app = Flask(__name__)
app.config['upload_dir'] = upload_dir

@app.route('/')
def hello_world():
    return 'hello_kjw'

@app.route('/file_upload', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        f = request.files['file']
        fname = secure_filename(f.filename)
        path = os.path.join(app.config['upload_dir'], fname)
        f.save(path)
        return "file upload complete"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port = '5000', debug= True)
