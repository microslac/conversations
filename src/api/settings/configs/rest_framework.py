REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_PERMISSION_CLASSES": [],
    "EXCEPTION_HANDLER": "core.exceptions.handler.exception_handler",
    "DEFAULT_RENDERER_CLASSES": [
        "core.renderers.ResponseRenderer",
    ],
}
