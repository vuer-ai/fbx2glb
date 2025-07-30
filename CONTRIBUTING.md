# Contributing to fbx2glb

Thank you for considering contributing to fbx2glb! This document outlines the process for contributing to the project.

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/fortyfive-ai/fbx2glb.git
   cd fbx2glb
   ```

2. Create a virtual environment and install development dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   ```

3. Set up pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Code Style

We use Black for code formatting and isort for import sorting. You can run these tools with:

```bash
black src tests
isort src tests
```

## Testing

Run tests with pytest:

```bash
pytest
```

## Pull Request Process

1. Fork the repository and create a branch for your feature or bug fix
2. Write tests for your changes
3. Ensure all tests pass
4. Submit a pull request

## Release Process

For maintainers:

1. Update version in `pyproject.toml` and `src/fbx2glb/__init__.py`
2. Create a new entry in CHANGELOG.md
3. Commit changes and tag the release:
   ```bash
   git tag -a v0.1.0 -m "Release v0.1.0"
   git push origin v0.1.0
   ```
4. Build and upload to PyPI:
   ```bash
   python -m build
   python -m twine upload dist/*
   ```

## Code of Conduct

Please be respectful and inclusive when contributing to this project. Harassment or other disrespectful behavior will not be tolerated.

## License

By contributing to this project, you agree that your contributions will be licensed under the project's MIT License.
