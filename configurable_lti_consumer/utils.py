# -*- coding: utf-8 -*-
"""
Helper fonctions
"""

from django.conf import settings


def add_dynamic_components(CONFIGURABLE_XBLOCKS_SETTINGS, advanced_component_templates,
       categories, create_template_dict, course_advanced_keys):
    """
    Reads CONFIGURABLE_XBLOCKS_SETTINGS configuration to create related button
    in studio to instanciate configured xblocks
    """
    if CONFIGURABLE_XBLOCKS_SETTINGS:
        for component in CONFIGURABLE_XBLOCKS_SETTINGS['components']:
            for class_info in component["subclasses"]:
                display_name = class_info["display"]
                advanced_component_templates['templates'].append(
                    create_template_dict(
                        name=display_name,
                        category=component["module"],
                        support_level=False,
                        boilerplate_name=class_info["name"]
                        )
                )
            # Remove original overrided component
            try:
                course_advanced_keys.pop(
                    course_advanced_keys.index(component['module'])
                )
            except ValueError:
                pass


def configurable_xblocks(identifier, all_entry_points):
    """
    This function is passed to XBload.load_class method to filter multiple
    Python endpoints for same xblock. So we use it to select our preconfigured
    xblocks over the one they override.

    Args:
        identifier: the name of the endpoint
        all_entry_points: list of corresponding endpoints classes

    Returns:
        Selected xblock endpoint class
    """
    if len(all_entry_points) > 1:
        for component in settings.CONFIGURABLE_XBLOCKS_SETTINGS["components"]:
            if component["module"] == identifier:
                endpoint = next(endpoint
                    for endpoint in all_entry_points
                    if endpoint.attrs[0] == component["base_class"])
                return endpoint

    return all_entry_points[0]
