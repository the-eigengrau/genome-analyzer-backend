import predictor
import time
import os
import pathlib

from flask import Flask
from flask import request
from flask import abort
from flask import jsonify
from flask_cors import CORS, cross_origin


from werkzeug.utils import secure_filename

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
#app = Flask(__name__)
# Max 128 mb file upload
app.config['MAX_CONTENT_LENGTH'] = 128 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = '/tmp/cyberbionicus'
pathlib.Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}



# Serve the react files
# https://blog.miguelgrinberg.com/post/how-to-deploy-a-react--flask-project

@app.route('/_ah/warmup', methods=['GET'])
def index():
    coronamodel = load('coronamodel.joblib')
    
@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/')
def index():
    #This will serve the index of the react site.
    #--------------------------------------------
    #return app.send_static_file('index.html')
    return "Hello, World!"

@app.route('/sample', methods=['GET'])
def sample():
        prediction = str(predictor.CoronaSample()[0])
        print('Prediction completed. About to return response')
        return prediction

@app.route('/predict_upload', methods=['POST'])
def predict_upload():
    if 'file' not in request.files:
        abort(406)
    file = request.files['file']
    # if user does not select file, browser also
    # submits an empty part without filename
    if file.filename == '':
        abort(406)
    if file:
        filename = file.filename
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        print('POST request received')
        prediction = str(predictor.CoronaClassifier(path)[0])
        print('Prediction completed. About to return response')
        return prediction

@app.route('/predict_get', methods=['GET'])
def predict_get():
    print('GET request received')
    response = jsonify({'prediction': prediction})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    app.run(debug=True)
