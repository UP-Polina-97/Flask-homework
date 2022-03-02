from flask import request, jsonify
from app import app

class NoLuck(BaseException):
    status_code = 401
    default_message = 'No Luck'


class CantFindIt(BaseException):
    status_code = 404
    default_message = 'Cant Find It'


class ExceptionBasic(Exception):
    status_code = 0
    default_message = 'Unknown Error'

    def __init__(self, message: str = None, status_code: int = None):
        super().__init__(message)
        self.message = message
        request.status = self.status_code
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):

        return {
            'message': self.message or self.default_message
        }


class ErrorAuth(ExceptionBasic):
    status_code = 401
    default_message = 'Error Auth'

@app.errorhandler(NoLuck)
@app.errorhandler(CantFindIt)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response