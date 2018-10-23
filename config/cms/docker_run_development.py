# This file includes overrides to build the `development` environment for the CMS, starting from
# the settings of the `production` environment

from docker_run_production import *
from lms.envs.fun.utils import Configuration

from configurable_lti_consumer import filter_configurable_lti_consumer

# Load custom configuration parameters from yaml files
config = Configuration(os.path.dirname(__file__))

DEBUG = True
REQUIRE_DEBUG = True

EMAIL_BACKEND = config(
    "EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)

PIPELINE_ENABLED = False
STATICFILES_STORAGE = "openedx.core.storage.DevelopmentStorage"

ALLOWED_HOSTS = ["*"]

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

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

CONFIGURABLE_LTI_CONSUMER_SETTINGS = config(
    "CONFIGURABLE_LTI_CONSUMER_SETTINGS", default=DEFAULT_CONFIGURABLE_LTI_CONSUMER_SETTINGS, formatter=json.loads
)
# helper function that will be passed to XBlock.load_class
# method to filter multiple Python endpoints for the same xblock (lti_consumer)
XBLOCK_SELECT_FUNCTION = filter_configurable_lti_consumer
