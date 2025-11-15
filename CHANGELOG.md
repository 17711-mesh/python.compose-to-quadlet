# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-11-15

### Added
- Initial version of the `compose-to-quadlet` tool.
- Converts `docker-compose.yml` files to Quadlet units.
- Supports services, volumes, and networks.
- Generates `.container`, `.volume`, `.network`, and `.target` files.
- CLI interface with `click`.
