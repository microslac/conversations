REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_PERMISSION_CLASSES": [],
    "EXCEPTION_HANDLER": "micro.jango.exceptions.handler.exception_handler",
    "DEFAULT_RENDERER_CLASSES": [
        "micro.jango.renderers.ResponseRenderer",
    ],
}
