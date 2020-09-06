from flask import Flask, request
from flask_restful import Resource, Api
import boto3
import requests
import json

app = Flask(__name__)
api = Api(app)


@app.route('/event', methods=['POST'])
def event():
    url = "http://localhost:8082/topics/events"
    headers = {
        "Content-Type": "application/vnd.kafka.json.v1+json"
    }
    data = {
        "records":
            [
                {
                    "value": {
                        "Event_Type": request.form.get('Event_Type'),
                        "Event_Version": request.form.get('Event_Version'),
                        "User_ID": request.form.get('User_ID'),
                        "Listing_ID": request.form.get('Listing_ID'),
                        "Server_Time": request.form.get('Server_Time'),
                        "Device_Type": request.form.get('Device_Type'),

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
