from flask import Flask, request
from flask_restful import Resource, Api
import boto3

app = Flask(__name__)
api = Api(app)


@app.route('/event', methods=['POST'])
def form():

    return '200'


if __name__ == '__main__':
    app.run(debug=True)
