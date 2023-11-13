import sys
sys.path.append('C:/Users/chand/Documents/Workspace/vcode/python-snippets-1/large_project/src') 

from flask import Flask, request, jsonify
from utils.util import duration
from app.demo import some_method
from config.log_config import Logger

logger = Logger()
app = Flask(__name__)

@app.route('/', defaults={'path': 'v1/main'}, methods=['GET'])
@duration
def main(path):

    # Get the HTTP method
    http_method = request.method

    # Get the headers
    headers = dict(request.headers)

    # Get the request body
    request_body = request.json if request.is_json else request.data.decode()

    # Process the request and generate the response body
    response_body = process_request(http_method, path, headers, request_body)

    logger.log_info(response_body)

    # Return the response
    return jsonify(response_body)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def catch_all(path):
    # Get the HTTP method
    http_method = request.method

    # Get the headers
    headers = dict(request.headers)

    # Get the request body
    request_body = request.json if request.is_json else request.data.decode()

    # Process the request and generate the response body
    response_body = process_request(http_method, path, headers, request_body)

    # Return the response
    return jsonify(response_body)

def process_request(http_method, path, headers, request_body):
    # Add your logic here to process the request and generate the response
    # You can use the provided parameters to determine the desired behavior

    # For demonstration purposes, let's return a generic response
    response = {
        'status': 'success',
        'message': f'Request received for {http_method} {path}',
        'headers': headers,
        'request_body': request_body,
        'response_body': 'Response from the API'
    }

    return response

if __name__ == '__main__':
    app.run()
