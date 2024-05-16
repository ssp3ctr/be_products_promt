from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from util.translations import load_translations
from babel.support import Translations

class LocaleMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        user_language = request.headers.get('Accept-Language', 'en')
        request.state.translations = load_translations(user_language)
        response = await call_next(request)
        return response

    
