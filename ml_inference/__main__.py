from flask import Flask, request, send_file
import cv2
import numpy as np
import io
from .inference import Inference
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
inference = Inference("encoder.h5", "generator.h5")


@app.route('/infer', methods=['POST'])
def process_image():
    # checking if the file is present or not.
    if 'file' not in request.files:
        return "No file found"
    file = request.files.get('file')
    age = int(request.form.get('age'))
    file_str = file.read()

    nparr = np.fromstring(file_str, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    infer_img = inference.infer(img_np, age)

    img_encoded = cv2.imencode('.png', infer_img)[1].tobytes()

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
