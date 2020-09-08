from flask import request, current_app
from flask_restful import Resource
import requests
import json


class Events(Resource):
    def post(self):
        try:
            url = "http://localhost:8087/topics/events"
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
            if r.status_code != 200:
                raise Exception('Posting to kafka return status code ' + str(r.status_code))
            else:
                current_app.logger.debug('Successfully posted event to kafka.')
        except Exception as e:
            current_app.logger.error('Error while submitting events to kafka :\n' + str(e))
