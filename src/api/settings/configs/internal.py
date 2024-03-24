from api.settings import env

INTERNAL_KEY = env.str("MICROSERVICE_INTERNAL_KEY", default="internal")
