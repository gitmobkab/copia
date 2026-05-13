# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- official postgres adapter
- unique keyword and generated values

### Changed

- the dsl syntax now explicitly require parantheses after the name of a generator
- the `ref` generator is now called `fetch` as the name is more intuitive
- the cli logs messages appereance

### Removed

- tests on profile keys `host`, `database` and `user` for more flexibility

## [0.2.1] - 2026-04-26

### Fixed

- fixed the directive to use copia config schema file in the documentation and example file. Sorry about that :D

## [0.2.0] - 2026-04-26

### Added

- Generation settings screen (`s`) — change locale and toggle fast generation mid-session

## [0.1.1] - 2026-04-20

### Fixed
- corrected a typo in the README file.
    (yes, i know, sorry for my bad english)

## [0.1.0] - 2026-04-20

- Initial release