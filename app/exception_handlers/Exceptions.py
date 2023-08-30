from werkzeug.exceptions import HTTPException

class InvalidEventException(HTTPException):
    code = 400
    description = "Invalid Event object"

class InvalidTrackingPlanException(HTTPException):
    code = 400
    description = "Invalid Tracking plan object"

