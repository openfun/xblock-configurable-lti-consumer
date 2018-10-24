# This file includes overrides to build the `development` environment for the LMS starting from the
# settings of the `production` environment

from docker_run_production import *
from .utils import Configuration

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

WEBPACK_CONFIG_PATH = "webpack.dev.config.js"

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
# helper function that will be passed to XBlock.load_class
# method to filter multiple Python endpoints for the same xblock (lti_consumer)
XBLOCK_SELECT_FUNCTION = filter_configurable_lti_consumer