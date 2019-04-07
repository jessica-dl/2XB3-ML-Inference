from flask import Flask, Response, request, send_file
import cv2
import numpy as np
import os
from werkzeug import secure_filename
import jsonpickle

app = Flask(__name__)


@app.route('/infer', methods=['POST'])
def process_image():
    # checking if the file is present or not.
    if 'file' not in request.files:
        return "No file found"
    file = request.files.get('file')
    file_str = file.read()

    nparr = np.fromstring(file_str, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  # cv2.IMREAD_COLOR in OpenCV 3.1

    response = {'message': 'image received. size={}x{}'.format(img_np.shape[1], img_np.shape[0])}
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")

    '''
    
    filename = secure_filename(file.filename)
    cv2.imwrite(os.path.join('C:\\Jessica\\Downloads\\', filename), img_np)
    img_file = StringIO()
    img_file.write(cv2.imencode('.png', img_np)[1].tobytes())
    
    return send_file(
        StringIO(cv2.imencode('.png', img_np)[1].tostring()).seek(0),
        mimetype='image/png',
        as_attachment=True,
        attachment_filename='response.png')

    return send_file(cv2.imencode('.png', img_np)[1].tobytes(), mimetype='image/png')
    '''

@app.route('/', methods=['GET'])
def get_request():
    return 'Hello World'


if __name__ == '__main__':
    app.debug = True
    app.run()
