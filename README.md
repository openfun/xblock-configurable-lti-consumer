# Configurable LTI Consumer XBlock

This XBlock is built on top of [edX LTI consumer
Xblock](https://github.com/edx/xblock-lti-consumer) to ease its configuration by Instructors.

Here are a few examples of what this module brings to Open edX:

- Pre-configure LTI services that can be added in one-click from the `Advanced` component button,
- Enforced configuration for some LTI Services by targetting a launch url pattern,
- Enforced default configuration for all LTI Services for better control, security or ergonomy,
- Platform-level LTI credentials configuration available to all courses.
  courses.


## Installation

This package can be installed with `pip`:

```bash
$ pip install configurable_lti_consumer-xblock
```

Edx's [lti_consumer-xblock](https://github.com/edx/xblock-lti-consumer) is
required as an extra dependency if you are willing to install or test this
XBlock as a standalone package. You can install it separately with `pip`:

```bash
$ pip install git+https://github.com/edx/xblock-lti-consumer@v1.1.8#egg=lti-consumer-xblock
```

If you plan to install it in a base Open edX installation, this dependency will
already be available, and thus you don't need to execute the above command.

## Getting started

First things first, if you plan to work on the project itself, you will need to
clone this repository:

```
$ git clone git@github.com:openfun/xblock-configurable-lti-consumer.git
```

Once the project has been cloned on your machine, you will need to build a
custom [edx-platform docker image](https://github.com/openfun/openedx-docker) that
includes the configurable LTI consumer XBlock and setup a development environment that
includes all required services up and running (more on this later):

```bash
$ cd xblock-configurable-lti-consumer
$ make bootstrap
```

If everything went well, you should now be able to access the following services:

- Open edX LMS: http://localhost:8072
- Open edX CMS: http://localhost:8082

with the following credentials:

```
email: admin@example.com
password: admin
```

## Configuration examples

A typical LTI configuration looks like this:

```python
LTI_XBLOCK_CONFIGURATIONS = [
    {
        "display_name": "Marsha Video",
        "oauth_consumer_key": "InsecureOauthConsumerKey",
        "shared_secret": "InsecureSharedSecret",
        "is_launch_url_regex": True,
        "automatic_resizing": True,
        "inline_ratio": 0.5625,
        "hidden_fields": [
            "lti_id",
            "description",
            "launch_target",
            "custom_parameters",
            "button_text",
            "modal_height",
            "modal_width",
            "has_score",
            "weight",
            "hide_launch",
            "accept_grades_past_due",
            "ask_to_send_username",
            "ask_to_send_email",
        ],
        "defaults": {
            "custom_parameters": [],
            "ask_to_send_username": True,
            "weight": 0,
            "modal_height": 400,
            "ask_to_send_email": True,
            "accept_grades_past_due": False,
            "button_text": "button",
            "has_score": False,
            "hide_launch": False,
            "launch_target": "iframe",
            "modal_width": 80,
            "launch_url": "https://marsha\.education/lti/videos/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
            "lti_id": "marsha",
        },
    },
    {
        "pattern": ".*ltiapps\.net.*",
        "hidden_fields": ["launch_target"],
        "defaults": {"launch_target": "modal"},
    },
    {
        "display_name": "LTI consumer",
        "pattern": ".*",
        "hidden_fields": ["ask_to_send_username", "ask_to_send_email"],
        "automatic_resizing": False,
        "defaults": {
            "ask_to_send_email": True,
            "launch_target": "new_window",
            "ask_to_send_username": True,
        },
    },
]
```

This configuration does several things:

- it adds a "Marsha Video" link behind the `Advanced` component button in the Studio to add a
  video in one click. The video is automatically added to the
  [Marsha](https://github.com/openfun/marsha) instance pointed by the launch url,
- it forces all LTI consumer XBlocks that are pointing to `ltiapps.net` to use a modal,
- it proposes all other LTI consumer XBlocks to open in a new window as a default and forces
  to ask before sending the user's username and email.

The order of each configuration in this list is important because we will use, for a given
XBlock, the first configuration pattern that matches its launch url.

Note that the workbench included in the present repository is running this configuration
(see [config/settings.yml.dist](./config/settings.yml.dist)) on the official France Université Numérique
[Open edX extended Docker image](https://github.com/openfun/openedx-docker).


## Integration to Open edX Studio

For now, this project requires a small fork of [edx/edx-platform](github.com/edx/edx-platform)
if you want to add, for some of your configurations, preconfigured options in the
`Advanced` component button of the Studio.

In our opinion, this small fork is worth applying because:

- it will save you from installing many XBlocks and helps keep your Open edX installation manageable,
- it allows you to automatically add a specific link for each LTI service you want to offer to your
  instructors. They don't need to activate LTI and provide the credentials for each course... they
  don't need to provide the launch url of the service for each XBlock they add...

For `open-release/hawthorn.1`, the patch to apply is available here:
https://gist.github.com/sampaccoud/f15083325cec4f14a53bfb78fb4b4e42


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


## License

This work is released under the AGPL 3.0 License (see [LICENSE](./LICENSE)).
