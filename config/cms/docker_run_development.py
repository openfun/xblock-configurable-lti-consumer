# This file includes overrides to build the `development` environment for the CMS, starting from
# the settings of the `production` environment

from docker_run_production import *
from lms.envs.fun.utils import Configuration

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


# configurable-lti-consumer configuration
CONFIGURABLE_XBLOCKS_SETTINGS = {
    "components": [{
        "module": "lti_consumer",
        "base_class": "ConfigurableLtiConsumerXBlock",
        "subclasses": [{
            "name": "Generic",
            "display": "Generic LTI xblock",
            "default_values": {
                "lti_id": "Generic",
                "ask_to_send_username": True,
                "ask_to_send_email": True
            }
        }]
    }]
}

CONFIGURABLE_XBLOCKS_SETTINGS = config(
    "CONFIGURABLE_XBLOCKS_SETTINGS", default=CONFIGURABLE_XBLOCKS_SETTINGS, formatter=json.loads
)
from configurable_lti_consumer import configurable_xblocks
# helper function that will be passed to XBock.load_class
# method to filter multiple Python endpoints for the same xblock (lti_consumer)
XBLOCK_SELECT_FUNCTION = configurable_xblocks