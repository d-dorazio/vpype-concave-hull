# vpype-concave-hull

[`vpype`](https://github.com/abey79/vpype) plug-in to create the concave hull
of a set of points.


## Examples

```bash
# save the concave hull calculated from all the layers onto a new one
$ vpype random -n 20 -a 20cm 20cm concave-hull -t NEW show

# save the concave hull of layer 1 only onto layer 2
$ vpype random -n 20 -a 20cm 20cm concave-hull -l 1 -l 2 show
```


## Installation

See the [installation instructions](https://vpype.readthedocs.io/en/latest/install.html) for information on how
to install `vpype`.

If *vpype* was installed using pipx, use the following command:

```bash
$ pipx inject vpype vpype-concave-hull
```

If *vpype* was installed using pip in a virtual environment, activate the virtual environment and use the following command:

```bash
$ pip install vpype-concave-hull
```

Check that your install is successful:

```
$ vpype concave-hull --help
[...]
```

## Documentation

The complete plug-in documentation is available directly in the CLI help:

```bash
$ vpype concave-hull --help
```


## Development setup

Here is how to clone the project for development:

```bash
$ git clone https://github.com/d-dorazio/vpype-concave-hull.git
$ cd vpype-concave-hull
```

Create a virtual environment:

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install --upgrade pip
```

Install `vpype-concave-hull` and its dependencies (including `vpype`):

```bash
$ pip install -e .
$ pip install -r dev-dependencies.txt
```


## License

See the [LICENSE](LICENSE) file for details.
