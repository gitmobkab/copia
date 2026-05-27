# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [0.3.2] - 2026-05-27

### Fixed
- Fixed a bug where the generator `uuid` would crash in the `copia run --dumps json` command and other generators that returned non-basic types (like `datetime` objects)


### Changed

- Now passing the `--dumps` flag will directly dump the generated values and disable non-error logs.
- Improved the SQL formatter to be more accurate to the actual SQL syntax.


## [0.3.1] - 2026-05-18

### Fixed

- Fixed bugs when using the `run` command `--skip-config` and `--skip-confirm` flags.
- Fixed json formatter to return proper json text
- Fixed error message in the csv formatter

### Changed

- Downgrade minimum required python version to 3.11.
- Updated the exits codes.
- the generator suggestions system to be more forgiving

## [0.3.0] - 2026-05-15

### Added

- security improvements against sql injections
- official postgres adapter
- unique keyword and generated values
- a `copia run` command

### Changed

- the tui can now be launch with `copia tui` rather than `copia`
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