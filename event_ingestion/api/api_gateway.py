from flask import Flask, request
from flask_restful import Resource, Api
import boto3
import requests
import json

app = Flask(__name__)
api = Api(app)
URL = 'http://localhost:8082/topics/test'


@app.route('/event', methods=['POST'])
def event():
    url = "http://localhost:8082/topics/test"
    headers = {
        "Content-Type": "application/vnd.kafka.json.v1+json"
    }
    data = {
        "records":
            [
                {
                    "value": {
                        "foo": request.form.get('Event_Version')
                    }
                }
            ]
    }
    r = requests.post(url=url,
                      headers=headers,
                      data=json.dumps(data))

    print(r.status_code)
    return '200'


if __name__ == '__main__':
    app.run(debug=True)
