from flask import jsonify, Response
from .exceptions import *
from typing import Union
from werkzeug.exceptions import *
import traceback

def flashed_exception_handler(e: APIException) -> Union[Response, int]:
    return jsonify(e.to_dto()), int(e.http_code)

def __map_http_exception_to_flashed_exception(e: HTTPException) -> APIException:
    resp: Response = e.get_response()

    if resp.status_code == 404:
        return NotFoundException()

    return APIException(
        flash_message=e.name,
        http_code=resp.status_code
    )

def generic_exception_handler(e: Exception) -> Union[Response, int]:
    raisable: APIException = APIException()

    if isinstance(e, APIException):
        raisable = e
    elif isinstance(e, HTTPException):
        raisable = __map_http_exception_to_flashed_exception(e)
    else:
        print(f"Caught exception: {traceback.format_exc()}")

    return flashed_exception_handler(raisable)