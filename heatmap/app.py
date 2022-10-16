import imp
import traceback

from numpy import empty
from flask import Flask , request
from image_to_text import predict_step # Importing the class flask
from werkzeug.utils import secure_filename
import os
# app is the object or instance of Flask
app = Flask(__name__)
# app.route informs Flask about the URL to be used by function

path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'uploads')

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/img2txt/', methods = ['POST'])
def upload_file():
   if request.method == 'POST':
        f = request.files['file']
        f.filename.split('\\')
        filename = secure_filename(f.filename.split('\\')[-1])
        print("Filename",filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print("File path",file_path)
        f.save(file_path)
        try:
            out_text = predict_step(file_path)
        except Exception:
            return f"Error occurred:\n {traceback.print_exc()}", 500
        finally:
            return out_text,200
      
if __name__ == '__main__':
   app.run(debug = True, host ='0.0.0.0', port=5000)