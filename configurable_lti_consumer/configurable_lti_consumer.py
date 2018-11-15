from django.conf import settings
from lti_consumer import LtiConsumerXBlock

from .defaults import DEFAULT_CONFIGURABLE_LTI_CONSUMER_SETTINGS
from .exceptions import ConfigurableLTIConsumerException


class ConfigurableLtiConsumerXBlock(LtiConsumerXBlock):
    def __init__(self, *args, **kwargs):
        super(ConfigurableLtiConsumerXBlock, self).__init__(*args, **kwargs)

        if not self._runtime.__class__.__name__ == "ImportSystem":
            # We do not need this when importing course in studio
            self.set_editable_field_names()

    @classmethod
    def get_template(cls, boilerplate):
        """
        Returns a dict that will be used by modulestore to initialize xblock
        fields
        """
        template = {}
        template["metadata"] = cls.get_configuration(boilerplate)["default_values"]
        return template

    def set_editable_field_names(self):
        """
        Remove from editable_field_names list fields that we already have configured
        """
        self.editable_field_names = list(self.editable_field_names)
        for field, _ in self.get_configuration(self.lti_id)["default_values"].items():
            self.editable_field_names.pop(self.editable_field_names.index(field))

    @classmethod
    def get_configuration(cls, name):
        """
        Retrieving component subclass configuration from Django settings
        """

        for conf_name, configuration in getattr(
            settings,
            "CONFIGURABLE_LTI_CONSUMER_SETTINGS",
            DEFAULT_CONFIGURABLE_LTI_CONSUMER_SETTINGS,
        ).items():
            if conf_name == name:
                return configuration
        else:
            raise ConfigurableLTIConsumerException(
                "Configuration '{name}' does not exist".format(name=name)
            )

    @property
    def lti_provider_key_secret(self):
        """
        Override parent's method to use credentials from Django settings if
        available instead of courses settings
        """
        configuration = self.get_configuration(self.lti_id)
        if "lti_passport_credentials" in configuration:
            return (
                configuration["lti_passport_credentials"]["oauth_consumer_key"],
                configuration["lti_passport_credentials"]["shared_secret"],
            )
        return super(ConfigurableLtiConsumerXBlock, self).lti_provider_key_secret
