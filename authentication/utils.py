def jwt_response_payload_handler(token, user=None):
    return {
        'sessionId': token,
        'success': True
    }