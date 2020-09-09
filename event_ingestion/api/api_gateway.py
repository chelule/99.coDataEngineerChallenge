from flask import Flask, current_app
from flask_restful import Api
from event_ingestion.api.modules.events import Events
import logging

app = Flask(__name__)
api = Api(app)

api.add_resource(Events, '/events/')
if __name__ == '__main__':
    import logging
    logFormatStr = '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'
    logging.basicConfig(format=logFormatStr, filename="./log/global.log", level=logging.DEBUG)
    formatter = logging.Formatter(logFormatStr, '%m-%d %H:%M:%S')
    fileHandler = logging.FileHandler("./log/summary.log")
    fileHandler.setLevel(logging.DEBUG)
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logging.DEBUG)
    streamHandler.setFormatter(formatter)
    app.logger.addHandler(fileHandler)
    app.logger.addHandler(streamHandler)
    app.logger.info("Logging is set up.")
    app.run(debug=True)
