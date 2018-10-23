"""
Helper function that will be passed to XBlock.load_class
method to filter multiple Python endpoints for the same xblock (lti_consumer)
"""


def filter_configurable_lti_consumer(identifier, all_entry_points):
    """
    This function is passed to XBlock.load_class method to filter multiple
    Python endpoints for same xblock. So we use it to select
    configurable_lti_consumer over lti_consumer it overrides.

    Args:
        identifier: the name of the endpoint
        all_entry_points: list of corresponding endpoints classes

    Returns:
        Selected xblock endpoint class
    """
    if len(all_entry_points) > 1:
        if identifier == "lti_consumer":
            endpoint = next(
                endpoint
                for endpoint in all_entry_points
                if endpoint.attrs[0] == "ConfigurableLtiConsumerXBlock"
            )
            return endpoint

    return all_entry_points[0]
