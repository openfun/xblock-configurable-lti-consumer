"""Default settings for Configurable LTI Consumer"""
from django.conf import settings


# configurable-lti-consumer sample configuration
DEFAULT_CONFIGURABLE_LTI_CONSUMER_SETTINGS = {
    "Demo": {
        "display": "Demo LTI service",
        "lti_passport_credentials": {
            "oauth_consumer_key": "jisc.ac.uk",
            "shared_secret": "secret",
        },
        "default_values": {
            "lti_id": "Demo",
            "launch_target": "iframe",
            "launch_url": "http://ltiapps.net/test/tp.php",
            "custom_parameters": [],
            "button_text": "button",
            "inline_height": 800,
            "modal_height": 800,
            "modal_width": 80,
            "has_score": False,
            "weight": 0,
            "hide_launch": False,
            "accept_grades_past_due": False,
            "ask_to_send_username": True,
            "ask_to_send_email": True
            }
    },
    "Generic": {
        "display": "Generic LTI xblock",
        "default_values": {
            "lti_id": "Generic",
            "ask_to_send_username": True,
            "ask_to_send_email": True
        }
    }
}



CONFIGURABLE_LTI_CONSUMER_SETTINGS = getattr(
    settings, "CONFIGURABLE_LTI_CONSUMER_SETTINGS", DEFAULT_CONFIGURABLE_LTI_CONSUMER_SETTINGS
)
