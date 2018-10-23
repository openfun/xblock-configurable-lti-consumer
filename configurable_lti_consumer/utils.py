# -*- coding: utf-8 -*-
"""
Helper fonctions
"""

from django.conf import settings


def add_dynamic_components(
    CONFIGURABLE_LTI_CONSUMER_SETTINGS,
    advanced_component_templates,
    categories,
    create_template_dict,
    course_advanced_keys,
):
    """
    Reads CONFIGURABLE_LTI_CONSUMER_SETTINGS to create related buttons
    in studio to instanciate configured xblocks.
    When this xblock is installed, configurations are added to studio
    even if it is not in course advanced modules
    """
    for name, configuration in CONFIGURABLE_LTI_CONSUMER_SETTINGS.items():
        advanced_component_templates["templates"].append(
            create_template_dict(
                name=configuration["display"],
                category="lti_consumer",
                support_level=False,
                boilerplate_name=name,
            )
        )
    # Remove overrided lti_consumer, if it was added to course advanced modules
    try:
        course_advanced_keys.pop(course_advanced_keys.index("lti_consumer"))
    except ValueError:
        pass
