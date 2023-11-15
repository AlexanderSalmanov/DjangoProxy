import requests


SITE_CREATION_EXCEPTIONS = (
    requests.exceptions.SSLError,
    requests.exceptions.ConnectionError,
    requests.exceptions.InvalidSchema,
    requests.exceptions.HTTPError,
)
DEFAULT_MEDIA_TAGS = ["link", "script", "img"]
