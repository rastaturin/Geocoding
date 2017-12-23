from flask import Flask
from flask import jsonify
import configparser

from geo_services import GeoService, NotFoundException

app = Flask(__name__)
config = configparser.ConfigParser()
config.read('./config.ini')


@app.route("/address/<address>", methods=['GET'])
def get_location(address):
    # return location for the given address
    geo_service = GeoService(config)
    try:
        location = geo_service.get_location(address)
        return jsonify(location)
    except NotFoundException:
        return jsonify({'error': 'Address not found'}), 404
    except RuntimeError:
        return jsonify({'error': 'Internal Error'}), 503
