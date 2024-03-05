from os import environ, system
from pathlib import Path
from sys import argv, path

import django
from django.conf import settings
from django.core.management import call_command

PROJECT_ROOT = Path(__file__).resolve().parent.parent / "src"
MANAGE_PY = PROJECT_ROOT / "manage.py"


def noop(*args, **kwargs):
    pass  # noqa


def boot_django():
    path.append(str(PROJECT_ROOT))
    environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")
    django.setup()


def __getattr__(cmd: str):
    args = argv[1:]
    boot_django()
    if cmd.endswith("server"):
        if not any(":" in arg for arg in args):
            args.append(f"0.0.0.0:{settings.API_PORT}")
        system(f"python {MANAGE_PY} {cmd} {' '.join(args)}")
    else:
        call_command(cmd, args)
    return noop
