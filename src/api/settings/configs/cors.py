from corsheaders.defaults import default_headers

from api.settings import env

CORS_ALLOWED_HEADERS = default_headers + ()
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=())
CORS_ALLOW_CREDENTIALS = env.bool("CORS_ALLOW_CREDENTIALS", default=False)
CORS_ALLOW_ALL_ORIGINS = env.bool("CORS_ALLOW_ALL_ORIGINS", default=False)
