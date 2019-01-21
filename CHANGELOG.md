# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic
Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] - 2019-01-21

### Added

- Allow defining the LTI launch url as a regex. The idea is to dynamically generate a random url
  that matches this regex, each time an XBlock is added.

## [1.0.0-rc.4] - 2019-01-18

### Fixed

- Add front-end package data to manifest.in so it is collected during the build

## [1.0.0-rc.3] - 2019-01-18

### Fixed

- Fix CI bug that generated distribution packages not in line with git tag

## [1.0.0-rc.2] - 2019-01-15

### Added

- Add iframeResizer to automatically fit the height of the LTI iframe to its content.

### Fixed

- Remove header on top of the LTI window as it seems useless. We want to let the LTI service
  control the totality of the content displayed by the XBlock.

## [1.0.0-rc.1] - 2018-11-28

This is a first release candidate for production.

[unreleased]: https://github.com/openfun/xblock-configurable-lti-consumer/compare/v1.1.0...master
[1.1.0]: https://github.com/openfun/xblock-configurable-lti-consumer/compare/v1.0.0-rc.4...v1.1.0
[1.0.0-rc.4]: https://github.com/openfun/xblock-configurable-lti-consumer/compare/v1.0.0-rc.3...v1.0.0-rc.4
[1.0.0-rc.3]: https://github.com/openfun/xblock-configurable-lti-consumer/compare/v1.0.0-rc.2...v1.0.0-rc.3
[1.0.0-rc.2]: https://github.com/openfun/xblock-configurable-lti-consumer/compare/v1.0.0-rc.1...v1.0.0-rc.2
[1.0.0-rc.1]: https://github.com/openfun/xblock-configurable-lti-consumer/compare/v0.2.1...v1.0.0-rc.1