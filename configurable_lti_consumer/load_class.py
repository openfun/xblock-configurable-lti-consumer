"""
Helper function that will be passed to the XBlock.load_class method to filter multiple Python
entry points for the same XBlock (lti_consumer).
"""
from xblock.plugin import AmbiguousPluginError, PluginMissingError
from xmodule import modulestore


def filter_configurable_lti_consumer(identifier, all_entry_points):
    """
    This function is passed to XBlock.load_class method to filter multiple
    Python entry points for same XBlock. So we use it to select
    configurable_lti_consumer over lti_consumer it overrides.

    Args:
        identifier: the name of the entry point
        all_entry_points: list of corresponding entry point classes

    Returns:
        Selected XBlock entry point class
    """
    if len(all_entry_points) > 1:
        if identifier == "lti_consumer":
            return next(
                entry_point
                for entry_point in all_entry_points
                if entry_point.attrs[0] == "ConfigurableLtiConsumerXBlock"
            )
        else:
            raise AmbiguousPluginError(all_entry_points)

    if len(all_entry_points) == 0:
        raise PluginMissingError(identifier)

    return all_entry_points[0]


# We have to monkey patch the default_select method because it does not respect the
# XBLOCK_SELECT_FUNCTION setting everywhere in Open edX... like here
# github.com/edx/edx-platform/blob/master/common/lib/xmodule/xmodule/modulestore/__init__.py
modulestore.default_select = filter_configurable_lti_consumer
