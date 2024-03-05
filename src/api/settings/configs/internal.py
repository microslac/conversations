from api.settings import env

INTERNAL_KEY = env.str("INTERNAL_KEY", default="internal")
