from api.settings import env

RABBITMQ_ENABLED = env.bool("RABBITMQ_ENABLED", default=False)
RABBITMQ_HOST = env.str("RABBITMQ_HOST", default="")
RABBITMQ_PORT = env.int("RABBITMQ_PORT", default=0)
RABBITMQ_USERNAME = env.str("RABBITMQ_USERNAME", default="")
RABBITMQ_PASSWORD = env.str("RABBITMQ_PASSWORD", default="")
