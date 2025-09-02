from enum import Enum

class ResultCode(Enum):
    SUCCESS = 200
    
    BAD_REQUEST = 400
    FORBIDDEN = 403
    NOT_FOUND = 404
    
    INTERNAL_SERVER_ERROR = 500
    BAD_GATEWAY = 502
    GATEWAY_TIMEOUT = 504