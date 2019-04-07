from flask import Flask, request, send_file
import cv2
import numpy as np
import io

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
    img_encoded = cv2.imencode('.png', img_np)[1].tobytes()

    return send_file(
        io.BytesIO(img_encoded),
        mimetype='image/png',
        as_attachment=True,
        attachment_filename='response.png')


@app.route('/', methods=['GET'])
def get_request():
    return 'Hello World'


if __name__ == '__main__':
    app.debug = True
    app.run()
