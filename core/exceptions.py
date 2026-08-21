from fastapi import Request
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
    return JSONResponse(status_code=404, content={"error": exc.detail})

async def bad_request_handler(request: Request, exc: BadRequestException):
    return JSONResponse(status_code=400, content={"error": exc.detail})

async def forbidden_handler(request: Request, exc: ForbiddenException):
    return JSONResponse(status_code=403, content={"error": exc.detail})