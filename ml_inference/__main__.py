from flask import Flask, request, send_file
import cv2
import numpy as np
import io
from .inference import Inference
import logging

logging.basicConfig(level=logging.DEBUG)  # adds debugging to the app

app = Flask(__name__)
inference = Inference("encoder.h5", "generator.h5")


@app.route('/infer', methods=['POST'])
def process_image():

    if 'file' not in request.files:  # checking if the file is present or not.
        return "No file found"
    file = request.files.get('file')  # get the file
    age = int(request.form.get('age'))  # get the age
    file_str = file.read()  # read the inputted file

    nparr = np.fromstring(file_str, np.uint8)  # create an array from the file
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  # reads the image array into the correct format

    infer_img = inference.infer(img_np, age)  # creates the aged image by calling the inference

    img_encoded = cv2.imencode('.png', infer_img)[1].tobytes()  # encodes the image into a returnable format

    return send_file(
        io.BytesIO(img_encoded),
        mimetype='image/png',
        as_attachment=True,
        attachment_filename='response.png')  # returns the image as a response to the client


if __name__ == '__main__':
    app.debug = True  # runs a debugger if the POST fails
    app.run()
