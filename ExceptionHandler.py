from pydantic import ValidationError
from starlette.responses import JSONResponse
from fastapi import Request


def register_exception_handlers(app):
    @app.exception_handler(ValidationError)
    async def validation_exception_handler(request: Request, exc: ValidationError):
        return JSONResponse(
            status_code=422,
            content={"detail": exc.errors()},
        )
