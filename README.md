# Compose to Quadlet

> A tool to convert Docker Compose files to Podman Quadlet systemd units.

## Table of Contents

- [Synopsis](#synopsis)
- [Requirements](#requirements)
- [Installation](#installation)
- [Build](#build)
- [Testing](#testing)
- [Usage](#usage)
- [Changelog](#changelog)
- [License](#license)
- [Author Information](#author-information)

## Synopsis

`compose-to-quadlet` is a Python-based command-line tool that reads a Docker Compose file (`docker-compose.yml`) and generates corresponding `.container`, `.volume`, and `.network` files for use with Podman Quadlet.

This allows you to manage your multi-container applications as systemd services without manually writing unit files.

## Requirements

- Python 3.11+
- `pip` (for installation)

## Installation

To install the tool from the source repository, clone it and use `pip`:

```bash
git clone https://github.com/17711-mesh/python.compose-to-podman.git
cd python.compose-to-podman
pip install .
```

## Build

This project uses `setuptools` and can be built from source into a standard Python wheel.

1.  **Install the build tool:**
    ```bash
    pip install build
    ```

2.  **Build the package:**
    ```bash
    python -m build
    ```
    This will create a `dist/` directory containing the `.whl` and `.tar.gz` distribution files.

## Testing

The project includes a test suite based on `pytest`.

1.  **Install development dependencies:**
    The test dependencies are not included in the main package. To run the tests, first install `pytest`:
    ```bash
g
    pip install pytest
    ```

2.  **Run the tests:**
    ```bash
    pytest
    ```

## Usage

After installation, you can use the `compose-to-quadlet` command:

```bash
compose-to-quadlet --help
```

**Example:**

```bash
compose-to-quadlet docker-compose.yml --output-dir my-quadlets --stack-name my-app
```

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed history of changes.

## License

>
> MIT License
>
> Copyright (c) 2025, 🐌 [The 17711 Frame](https://17711.org)
> 
> Permission is hereby granted, free of charge, to any person obtaining a copy
> of this software and associated documentation files (the "Software"), to deal
> in the Software without restriction, including without limitation the rights
> to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
> copies of the Software, and to permit persons to whom the Software is
> furnished to do so, subject to the following conditions:
> 
> The above copyright notice and this permission notice shall be included in all
> copies or substantial portions of the Software.
> 
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
> AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
> LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
> OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
> SOFTWARE.
> 

## Author Information

This project is maintained by [The 17711 Frame](https://17711.org).