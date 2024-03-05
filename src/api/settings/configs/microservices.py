import re
from types import SimpleNamespace
from api.settings import env

MICROSERVICE = SimpleNamespace(
    AUTH_HOST=env.str("MICROSERVICE_AUTH_HOST", default="auth"),
    AUTH_PORT=env.int("MICROSERVICE_AUTH_HOST", default=8011),
    TEAMS_HOST=env.str("MICROSERVICE_TEAMS_HOST", default="teams"),
    TEAMS_PORT=env.int("MICROSERVICE_TEAMS_HOST", default=8012),
    USERS_HOST=env.str("MICROSERVICE_USERS_HOST", default="users"),
    USERS_PORT=env.int("MICROSERVICE_USERS_HOST", default=8013),
)

MICROSERVICE_ALL_HOST = env.str("MICROSERVICE_ALL_HOST", default="")  # localhost
if MICROSERVICE_ALL_HOST:
    hosts = [host for host in vars(MICROSERVICE) if re.match(r".*_HOST$", host)]
    for host in hosts:
        setattr(MICROSERVICE, host, MICROSERVICE_ALL_HOST)
