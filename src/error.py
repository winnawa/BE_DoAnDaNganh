class APIError(Exception):
    def __init__(self): pass           
        

class NotFoundError(APIError):
    def __init__(self,message):
        self.message = message 

class BadRequestError(APIError):
    def __init__(self,message):
        self.message = message

class InternalServerError(APIError):
    def __init__(self,message):
        self.message = message

class UnauthorizedError(APIError):
    def __init__(self,message):
        self.message = message


class ErrorMapper:
    def __init__():pass

    @staticmethod
    def mappError(error: APIError):

        if type(error) is BadRequestError:
            return {
                "message": error.message
            },400

        if type(error) is UnauthorizedError:
            return {
                "message": error.message
            },401

        if type(error) is NotFoundError:
            return {
                "message": error.message
            },404

        if type(error) is InternalServerError:
            return {
                "message": error.message
            },500