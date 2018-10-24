# Configurable LTI Consumer XBlock

This XBlock inherits, enhances and replaces [edX LTI consumer
Xblock](https://github.com/edx/xblock-lti-consumer) to make available to
conceptors in CMS several pre-configured versions of LTI Consumer.
Configurations are stored in Django settings and pre-configured fields are no
longer modifiable for a given version.

## Installation

This package can be installed with `pip`:

```bash
$ pip install [--process-dependency-links] configurable_lti_consumer-xblock
```

Note that the `--process-dependency-links` `pip` option is only required to
install or test this Xblock as a standalone package. If you plan to install it
in a base Open edX installation, then you can safely miss this option as the
only package dependency should already have been resolved.

## Getting started

First things first, if you plan to work on the project itself, you will need to
clone this repository:

```
$ git clone git@github.com:openfun/xblock-configurable-lti-consumer.git
```

Once the project has been cloned on your machine, you will need to build a
custom edx-platform docker image that includes the xblock and setup a
development environment that includes all required services up and running (more
on this later):

```bash
$ cd xblock-configurable-lti-consumer
$ make bootstrap
```

If everything went well, you should now be able to access to the following
services:

- Open edX LMS: http://localhost:8072
- Open edX CMS: http://localhost:8082

with the following credentials:

```
email: admin@foex.edu
password: openedx-rox
```

## Developer guide

Once the project has been bootstrapped (see "Getting started" section), to start
working on the project, use:

```
$ make dev
```

You can stop running services _via_:

```
$ make stop
```

If for any reason, you need to drop databases and start with fresh ones, use the
`down` target:

```
$ make down
```

## Configuration example

The below example configuration instanciates 2 xblocks.

```python
CONFIGURABLE_LTI_CONSUMER_SETTINGS = {
    "Demo": {
        "display": "Demo LTI service",
        "lti_passport_credentials": {
            "oauth_consumer_key": "jisc.ac.uk",
            "shared_secret": "secret",
        },
        "default_values": {
            "lti_id": "Demo",
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
    },
    "Generic": {
        "display": "Generic LTI xblock",
        "default_values": {
            "lti_id": "Generic",
            "ask_to_send_username": True,
            "ask_to_send_email": True
        }
    }
}
```

You also need to set XBLOCK_SELECT_FUNCTION setting to enforce
configurable_lti_consumer endpoint over lti_consumer's one.


```python
try:
    from configurable_lti_consumer import filter_configurable_lti_consumer
    XBLOCK_SELECT_FUNCTION = filter_configurable_lti_consumer
except ImportError:
    pass
```

## Studio integration

For now studio integration is made by inserting `utils.configurable_xblocks`
function call in `edx-platform/cms/djangoapps/contentstore/views/component.py`.
It adds preconfigured xblocks to "Advanced" button and removes overridden
`lti_consumer` component if it had been added to advanced modules.
