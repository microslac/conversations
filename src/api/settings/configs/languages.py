from api.settings import env

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/
LANGUAGE_CODE = env("LANGUAGE_CODE", default="en-us")

LANGUAGES = [
    ("en", "English"),
    ("es", "Spanish"),
    ("pt-br", "Brazilian Portuguese"),
    ("fr", "French"),
    ("fr-ca", "French (Canadian)"),
    ("de", "German"),
    ("zh-cn", "Simplified Chinese"),
    ("zh-tw", "Chinese Traditional"),
    ("tr", "Turkish"),
    ("nl", "Dutch"),
    ("hu", "Hungarian"),
    ("it", "Italian"),
    ("ko", "Korean"),
    ("ru", "Russian"),
    ("ja", "Japanese"),
    ("vi", "Vietnamese"),
    ("bs", "Bosnian"),
    ("he", "Hebrew"),
    ("ar", "Arabic"),
    ("bg", "Bulgarian"),
    ("hr", "Croatian"),
    ("cs", "Czech"),
    ("el", "Greek"),
    ("pl", "Polish"),
    ("sr", "Serbian (Latin)"),
    ("sk", "Slovak"),
    ("th", "Thai"),
    ("uk", "Ukrainian"),
    ("ro", "Romanian"),
    ("es-em", "Spanish (Spain)"),
    ("es-mx", "Spanish (Mexico)"),
    ("pt", "Portuguese (Portugal)"),
    ("en-gb", "English, United Kingdom"),
    ("ms", "Malay"),
    ("da", "Danish"),
    ("id", "Indonesian"),
]
