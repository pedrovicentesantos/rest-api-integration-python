from flask import jsonify

def bad_request(message):
    response = jsonify({
        'error': {
            'message': message
        }
    })
    response.status_code = 400
    return response

def not_found(message):
    response = jsonify({
        'error': {
            'message': message
        }
    })
    response.status_code = 404
    return response

def ok(data):
    response = jsonify({
        'data': data
    })
    response.status_code = 200
    return response

def internal_server_error(message):
    response = jsonify({
        'error': {
            'message': message
        }
    })
    response.status_code = 500
    return response

def no_content():
    response = jsonify({})
    response.status_code = 204
    return response