from flask import Flask


def init():
    app = Flask(__name__)

    @app.route('/', methods=['GET'])
    def hello_world():
        return 'Hello, World!'

    app.run()



