#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import setup


def package_data(pkg, roots):
    """Generic function to find package_data.
    All of the files under each of the `roots` will be declared as package
    data for package `pkg`.
    """
    data = []
    for root in roots:
        for dirname, _, files in os.walk(os.path.join(pkg, root)):
            for fname in files:
                data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}


setup(name="xblock-configurable-lti-consumer",
      version="1.2.5+eucalyptus",
      description="This Xblock adds configurability over the original lti_consumer XBlock from edx",
      author="Open FUN (France Universite Numérique)",
      author_email="fun.dev@fun-mooc.fr",
      license="AGPL 3.0",
      url="https://github.com/openfun/xblock-configurable-lti-consumer",
      platforms=["any"],
      packages=[
        "configurable_lti_consumer",
      ],
    install_requires=[
        "XBlock",
        "exrex==0.10.5",
    ],
    entry_points={
        "xblock.v1": [
            "lti_consumer = configurable_lti_consumer:ConfigurableLtiConsumerXBlock",
        ]
    },
    package_data=package_data("configurable_lti_consumer", [
          "static",
          "templates",
          ]
    ),
)
