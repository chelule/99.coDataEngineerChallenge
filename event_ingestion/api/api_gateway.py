from flask import Flask
from flask_restful import Api
from event_ingestion.api.modules.events import Events

app = Flask(__name__)
api = Api(app)

api.add_resource(Events, '/events/')

if __name__ == '__main__':
    app.run(debug=True)
