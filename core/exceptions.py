from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class NotFoundException(Exception):
    def __init__(self, detail: str = "Not found"):
        self.detail = detail


class BadRequestException(Exception):
    def __init__(self, detail: str = "Bad request"):
        self.detail = detail


class ForbiddenException(Exception):
    def __init__(self, detail: str = "Forbidden"):
        self.detail = detail


async def not_found_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=404,
        content={
            "error": exc.detail
        }
    )


async def bad_request_handler(request: Request, exc: BadRequestException):
    return JSONResponse(
        status_code=400,
        content={
            "error": exc.detail
        }
    )


async def forbidden_handler(request: Request, exc: ForbiddenException):
    return JSONResponse(
        status_code=403,
        content={
            "error": exc.detail
        }
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    errors = []

    for error in exc.errors():
        field = error["loc"][-1]

        if field == "email":
            message = "Email không hợp lệ"
        elif field == "password":
            message = "Mật khẩu không hợp lệ"
        elif field == "full_name":
            message = "Họ tên không hợp lệ"
        else:
            message = "Dữ liệu không hợp lệ"

        errors.append({
            "field": field,
            "message": message
        })

    return JSONResponse(
        status_code=422,
        content={
            "error": "Dữ liệu không hợp lệ",
            "details": errors
        }
    )