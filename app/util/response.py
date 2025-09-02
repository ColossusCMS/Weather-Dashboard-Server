def create_response(result_code, result_msg, item):
    response = {
        'response': {
            'header': {
                'resultCode': result_code,
                'resultMsg': result_msg
            },
            'body': {
                'items': {
                    'item': item
                }
            }
        }
    }
    return response