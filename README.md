# Configurable LTI Consumer XBlock

This XBlock inherits, enhances and replaces [edX LTI consumer Xblock](https://github.com/edx/xblock-lti-consumer) to make available to conceptors in CMS several preconfigured versions of
LTI Consumer. Configurations are stored in Django settings instead of course
advanced settings, and preconfigured fields are no longer modifiable for a given
version.

If this xblock is not installed or settings are not configured, courses using it
will safely fall back on regular edX LTI consumer xblock.


## Installation

This package can be installed with `pip`:

```bash
$ pip install [--process-dependency-links] configurable_lti_consumer-xblock
```

Note that the `--process-dependency-links` `pip` option is only required to
install or test this Xblock as a standalone package. If you plan to install it
in a base Open edX installation, then you can safely miss this option as the
only package dependency should already have been resolved.

## Configuration example

The below example configuration instanciates 2 xblocks.

```python
CONFIGURABLE_XBLOCKS_SETTINGS = {
    "components": [{
        "module": "lti_consumer",
        "base_class": "ConfigurableLtiConsumerXBlock",
        "subclasses": [{
            "name": "Demo LTI Service",
            "display": "Demo LTI xblock",
            "lti": {
                "key": "jisc.ac.uk",
                "secret": "secret",
            },
            "default_values": {
                "description": "Demo",
                "lti_id": "",
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
        },{
            "name": "Generic",
            "display": "Generic LTI xblock",
            "default_values": {
                "description": "Generic",
                "ask_to_send_username": True,
                "ask_to_send_email": True
            }
        }]
    }]
}
```

You also need to set XBLOCK_SELECT_FUNCTION setting to enforce
configurable_lti_consumer endpoint over lti_consumer's one.

```python
try:
    from configurable_lti_consumer import configurable_xblocks
    XBLOCK_SELECT_FUNCTION = configurable_xblocks
except ImportError:
    pass
```

## Studio integration

For now studio integration is made by inserting `utils.configurable_xblocks`
function call in `edx-platform/cms/djangoapps/contentstore/views/component.py`.
It adds to preconfigured xblocks "Advanced" button.
