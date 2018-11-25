# -*- coding: utf-8 -*-
"""
Helper fonctions
"""
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext as _


def add_dynamic_components(
    configurations,
    advanced_component_templates,
    categories,
    create_template_dict,
    course_advanced_keys,
):
    """
    Create, for each custom configuration of the LTI configurable XBlock, a link behind the
    `Advanced` components button in the Studio.

    Don't add a link for configurations that don't define a boilerplate. This type of
    configuration is useful to force a behavior on LTI consumer XBlocks matching a
    launch url pattern without proposing a specific component to the user.
    """
    seen = set()
    for configuration in configurations:
        display_name = configuration.get("display_name")
        if display_name:
            if display_name in seen:
                raise ImproperlyConfigured(
                    "LTI Xblock configurations should have unique display names: {:s}.".format(
                        display_name
                    )
                )
            seen.add(display_name)
            advanced_component_templates["templates"].append(
                create_template_dict(
                    name=display_name,
                    category="lti_consumer",
                    support_level=False,
                    boilerplate_name=display_name,
                )
            )

    # Remove overriden lti_consumer, if it was added to course advanced modules
    try:
        course_advanced_keys.pop(course_advanced_keys.index("lti_consumer"))
    except ValueError:
        pass
