import re

from django.conf import settings

from xblock.fragment import Fragment

from xblockutils.resources import ResourceLoader

from lti_consumer import LtiConsumerXBlock

from .exceptions import ConfigurableLTIConsumerException


class ConfigurableLtiConsumerXBlock(LtiConsumerXBlock):
    """Overriding the LTI consumer XBlock to make it configurable from Django settings."""

    @property
    def editable_fields(self):
        """
        Remove, from editable fields, the fields that we have already configured in settings.

        The `launch_url` field should always be in editable fields so our setting configurations
        are just light overrides and the XBlock is still explicitly just an LTI consumer XBlock.
        To say it differently, a specific LTI consumer XBlock reverts to its normal behavior as
        soon as you change its launch url... and you can do it manually even after adding the
        XBlock via a specific link behind the `Advanced` components button.

        It means that the links proposed when clicking on the `Advanced` components button are
        just shortcuts and everything works normally with an understandable workflow.
        """
        editable_fields = super(ConfigurableLtiConsumerXBlock, self).editable_fields
        hidden_fields = self.get_configuration(self.launch_url).get("hidden_fields", [])
        return (field for field in editable_fields if field not in hidden_fields)

    @classmethod
    def get_template(cls, boilerplate):
        """
        Returns a dictionary that will be used by the modulestore to initialize xblock fields.
        We need this so that the value of our preconfigured fields is set in Mongodb when
        creating the XBlock:
        - this is absolutely required for the `launch_url` field because it is used to associate
          the xblock with a configuration,
        - this is still desired for other preconfigured fields because it ensures that the xblock
          will look the same if the course is exported and re-imported to an instance of Open edX
          on which the configurable XBlock module is not installed. Note that if the values are
          modified in settings after running it for a while, the existing XBlock will still hold
          in Mongodb the default values at the time of their creation.
        """
        for configuration in getattr(settings, "LTI_XBLOCK_CONFIGURATIONS", []):
            if configuration.get("display_name") == boilerplate:
                break
        else:
            configuration = {}

        template = {}
        template["metadata"] = configuration.get("defaults", {})
        return template

    def __getattribute__(self, item):
        """
        First look for the value of a field in our XBlock settings and default to the normal
        behavior which is to retrieve the value stored in Mongodb.
        """
        # We always need to get the `launch_url` from Mongodb because it is used to associate the
        # XBlock with a configuration.
        if item != "launch_url" and item in LtiConsumerXBlock.editable_field_names:
            # Better ask for forgiveness than ask for permission...
            try:
                return self.get_configuration(self.launch_url)["defaults"][item]
            except KeyError:
                pass
        return super(ConfigurableLtiConsumerXBlock, self).__getattribute__(item)

    @classmethod
    def get_configuration(cls, launch_url):
        """
        Try finding from the settings a configuration that matches this xblock by the value of
        its `launch_url` field.
        The result of this method never changes for a given `launch_url`, so since it is a bit
        costly, it is a good idea to record each result in a class cache.
        """
        # we need a serializable value to use as our cache key
        launch_url = launch_url or ""

        # First, try returning the value direcly from the cache
        try:
            return getattr(cls, "_configuration_cache", {})[launch_url]
        except KeyError:
            pass

        # Then, look for the configuration in Django settings
        for configuration in getattr(settings, "LTI_XBLOCK_CONFIGURATIONS", []):

            pattern = configuration.get("pattern")
            # If we defined a value but no pattern for `launch_url`, create an exact pattern
            # to limit the configuration to only its exact `launch_url`.
            # If we defined no pattern and no value for `launch_url`, use the "^.*$" pattern
            # which will match anything.
            if not pattern:
                default_url = configuration.get("defaults", {}).get("launch_url", ".*")
                pattern = r"^{}$".format(default_url)

            if re.match(pattern, launch_url):
                # This configuration is matching, let's use it!
                break
        else:
            # If we didn't find a configuration matching the launch url, return an empty configuration
            configuration = {}

        # Initialize the class cache if it's not yet present
        if not getattr(cls, "_configuration_cache", None):
            cls._configuration_cache = {}

        # Save the result in cache for next time and return it
        cls._configuration_cache[launch_url] = configuration
        return configuration

    @property
    def lti_provider_key_secret(self):
        """
        Override parent's method to use credentials from Django settings if
        available instead of courses settings
        """
        configuration = self.get_configuration(self.launch_url)
        if configuration.get("oauth_consumer_key") and configuration.get(
            "shared_secret"
        ):
            return (configuration["oauth_consumer_key"], configuration["shared_secret"])
        return super(ConfigurableLtiConsumerXBlock, self).lti_provider_key_secret

    def student_view(self, context):
        """
        LMS and CMS view for configurable_lti_consumer.
        Will make a post request to lti_launch_handler view with
        LTI parameters and open response in an iframe or a new window
        depending on the xblock instance configuration.
        Arguments:
            context (dict): XBlock context
        Returns:
            xblock.fragment.Fragment: XBlock HTML fragment
        """
        fragment = Fragment()
        configurable_lti_consumer_loader = ResourceLoader(__name__)
        lti_consumer_loader = ResourceLoader(
            "lti_consumer"
        )  # ressource loader of inherited lti_consumer
        context.update(self._get_context_for_template())
        fragment.add_content(
            configurable_lti_consumer_loader.render_mako_template(
                "/templates/html/student.html", context
            )
        )
        fragment.add_css(lti_consumer_loader.load_unicode("static/css/student.css"))
        fragment.add_javascript(
            lti_consumer_loader.load_unicode("static/js/xblock_lti_consumer.js")
        )

        if context["inline_height"]:
            fragment.initialize_js("LtiConsumerXBlock")
        else:  # iframe height will be set by iframeResizer lib
            fragment.add_javascript(
                configurable_lti_consumer_loader.load_unicode(
                    "static/js/vendor/iframeResizer.min.js"
                )
            )
            fragment.add_javascript(
                configurable_lti_consumer_loader.load_unicode(
                    "static/js/configurable_xblock_lti_consumer.js"
                )
            )
            fragment.initialize_js("configurableLTIConsumerXblockIframeResizerInit")

        return fragment
