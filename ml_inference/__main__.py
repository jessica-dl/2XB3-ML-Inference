from flask import Flask, request

app = Flask(__name__)


@app.route('/infer', methods=['POST'])
def process_image():
    print(request.files)
    # checking if the file is present or not.
    if 'file' not in request.files:
        return "No file found"

    def age_face(img):
        return img

    img = request.files['file']
    new_img = age_face(img)
    img_name = new_img[-10:]

    try:
        send_file(new_img, attachment_filename=img_name)
    except Exception as e:
        return str(e)


@app.route('/', methods=['GET'])
def get_request():
    return 'Hello World'


if __name__ == '__main__':
    app.run()
