from flask import jsonify, Response
from .exceptions import *
from typing import Union
from werkzeug.exceptions import *

def flashed_exception_handler(e: FlashedException) -> Union[Response, int]:
    return jsonify(e.to_dto()), int(e.http_code)

def __map_http_exception_to_flashed_exception(e: HTTPException) -> FlashedException:
    resp: Response = e.get_response()

    if resp.status_code == 404:
        return NotFoundException()
    # elif resp.status_code

    return FlashedException(
        flash_message=e.name,
        http_code=resp.status_code
    )

def generic_exception_handler(e: Exception) -> Union[Response, int]:
    raisable: FlashedException = FlashedException()

    if isinstance(e, FlashedException):
        raisable = e
    elif isinstance(e, HTTPException):
        raisable = __map_http_exception_to_flashed_exception(e)

    return flashed_exception_handler(raisable)