# FBX2GLB

A versatile toolkit for converting FBX 3D models to GLB format for web applications.

[![PyPI version](https://badge.fury.io/py/fbx2glb.svg)](https://badge.fury.io/py/fbx2glb)
[![PyPI downloads](https://img.shields.io/pypi/dm/fbx2glb.svg)](https://pypi.org/project/fbx2glb/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**📦 [Install from PyPI](https://pypi.org/project/fbx2glb/) | 🐛 [Report Issues](https://github.com/vuer-ai/fbx2glb/issues) | 📖 [Documentation](https://github.com/vuer-ai/fbx2glb#readme)**

## Features

- **Multiple Conversion Methods:**
  - Autodesk FBX SDK (if available)
  - Facebook's fbx2gltf command line tool
  - Blender (if installed)
- **Batch Processing:** Convert multiple files at once with parallel processing
- **Component Generation:** Generate React/Three.js components from 3D models
- **FBX Upgrading:** Upgrade older FBX files to newer versions for better compatibility
- **Preserve Quality:** Maintain animations, materials, textures, and skeletal data
- **Cross-Platform:** Support for macOS, Windows, and Linux

## Quick Start

### Installation

#### From PyPI (Recommended)

```bash
# Install the latest version from PyPI
pip install fbx2glb

# Or install with specific version
pip install fbx2glb==0.1.0
```

#### From Source (Development)

```bash
# Clone the repository
git clone https://github.com/vuer-ai/fbx2glb.git
cd fbx2glb

# Install in development mode
pip install -e '.[dev]'
```

### Basic Usage

```bash
# Convert a single FBX file to GLB
fbx2glb input.fbx output.glb

# Convert with axis fixing and FBX upgrading
fbx2glb input.fbx output.glb --fix-axis --upgrade-fbx

# Check available conversion methods
fbx2glb --check-dependencies

# Generate a React/Three.js component
fbx2glb-component input.fbx src/components/MyModel.tsx

# Batch convert multiple files
fbx2glb-batch source_directory output_directory --recursive
```

## Installation

### From PyPI (Recommended)

```bash
# Install the latest version
pip install fbx2glb

# Install with specific version
pip install fbx2glb==0.1.0

# Install with development dependencies
pip install fbx2glb[dev]
```

### From Source (Development)

```bash
git clone https://github.com/vuer-ai/fbx2glb.git
cd fbx2glb
pip install -e '.[dev]'
```

### Package Information

- **PyPI**: https://pypi.org/project/fbx2glb/
- **Source**: https://github.com/vuer-ai/fbx2glb
- **Documentation**: https://github.com/vuer-ai/fbx2glb#readme
- **Issues**: https://github.com/vuer-ai/fbx2glb/issues

## FBX SDK Installation (Recommended)

For the best results and FBX file upgrading capabilities, install the Autodesk FBX SDK:

### macOS

```bash
# Using the included Makefile
make install-fbx-sdk
```

### Manual Installation

1. Download the [FBX SDK](https://www.autodesk.com/developer-network/platform-technologies/fbx-sdk-2020-3) from Autodesk
2. Install the SDK for your platform
3. The package will automatically detect the SDK installation

## Project Structure

```
fbx2glb/
├── fbx2glb/              # Main Python package
│   ├── __init__.py       # Package initialization
│   ├── cli.py           # Command-line interface
│   ├── converter.py     # Core conversion logic
│   ├── batch.py         # Batch processing
│   ├── component.py     # React component generation
│   ├── utils.py         # Utility functions
│   ├── params.py        # Parameter structures
│   └── fbx_upgrader.py  # FBX file upgrading
├── tools/               # Build tools and utilities
│   ├── upgrade_fbx.cpp  # C++ source for FBX upgrade tool
│   ├── upgrade_fbx      # Compiled binary
│   └── README.md        # Tools documentation
├── examples/            # Example files and models
├── tests/              # Test suite
├── local/              # SDK installers (macOS)
├── sdk/                # SDK packages
├── Makefile            # Unified build system
└── FBX2glTF/           # Facebook's FBX2glTF (git submodule)
```

## Usage

### Command Line Interface

```bash
# Convert a single file
fbx2glb input.fbx [output.glb] [options]

# Batch conversion
fbx2glb-batch source_directory [output_directory] [options]

# Generate React/Three.js component
fbx2glb-component input.fbx [output_component.tsx] [options]
```

### Common Options

```bash
# Specify conversion method
--method fbx-sdk|fbx2gltf|blender

# Force overwrite existing files
--force

# Enable verbose output
--verbose

# Upgrade FBX file before conversion
--upgrade-fbx

# Check dependencies
--check-dependencies
```

### Python API

```python
from fbx2glb import convert_file, batch_convert, generate_component

# Convert a single file
success = convert_file("input.fbx", "output.glb", method="fbx-sdk")

# Batch convert with parallel processing
successes, failures = batch_convert(
    "source_dir", 
    "output_dir", 
    recursive=True, 
    parallel=4
)

# Generate React component
success = generate_component(
    "input.fbx", 
    "MyModel.tsx", 
    component_name="MyModel"
)
```

### Using the Makefile

The project includes a comprehensive Makefile for common tasks:

```bash
# Show all available commands
make help

# Install FBX SDK (macOS)
make install-fbx-sdk

# Build the FBX upgrade tool
make build-upgrade-tool

# Convert XBot example with FBX upgrading
make upgrade-xbot

# Convert XBot example (basic)
make convert-xbot

# Troubleshoot conversion issues
make troubleshoot

# Clean build artifacts
make clean

# Build Python package
make build-package
```

## Configuration

Create a `.fbx2glb.json` file in your project root to customize conversion behavior:

```json
{
  "defaultMethod": "fbx-sdk",
  "fallbackMethods": ["fbx2gltf", "blender"],
  "blenderPath": "/Applications/Blender.app/Contents/MacOS/Blender",
  "outputFormat": "glb",
  "preserveAnimations": true,
  "optimizeMeshes": true
}
```

## Conversion Methods

### 1. Autodesk FBX SDK (Recommended)
- **Pros:** Best quality, supports FBX upgrading, handles all FBX versions
- **Cons:** Requires SDK installation, larger file sizes
- **Use when:** You need the highest quality conversion or have old FBX files

### 2. Facebook's fbx2gltf
- **Pros:** Fast, good compression, open source
- **Cons:** Limited FBX version support
- **Use when:** You need fast conversion of modern FBX files

### 3. Blender
- **Pros:** Free, handles many formats, good for complex scenes
- **Cons:** Slower, requires Blender installation
- **Use when:** You need to process many different 3D formats

## Examples

### Basic Conversion

```bash
# Convert a single file
fbx2glb model.fbx model.glb

# Convert with specific method
fbx2glb model.fbx model.glb --method fbx2gltf

# Convert with FBX upgrading
fbx2glb old_model.fbx new_model.glb --upgrade-fbx

# Convert with axis fixing (fix orientation issues)
fbx2glb model.fbx model.glb --fix-axis
```

### Batch Processing

```bash
# Convert all FBX files in a directory
fbx2glb-batch models/ output/ --recursive

# Convert with parallel processing
fbx2glb-batch models/ output/ --parallel 4 --force
```

### Component Generation

```bash
# Generate a React component
fbx2glb-component character.fbx CharacterModel.tsx

# Generate with custom name
fbx2glb-component character.fbx CharacterModel.tsx --name CharacterModel
```

## Troubleshooting

### Common Issues

1. **FBX version too old:**
   ```bash
   # Use FBX upgrading
   fbx2glb old_model.fbx new_model.glb --upgrade-fbx
   ```

2. **No conversion methods available:**
   ```bash
   # Check what's available
   fbx2glb --check-dependencies
   
   # Install FBX SDK
   make install-fbx-sdk
   ```

3. **Blender not found:**
   ```bash
   # Specify Blender path
   fbx2glb model.fbx model.glb --blender-path /path/to/blender
   ```

### Getting Help

```bash
# Run the troubleshooting command
make troubleshoot

# Check system information
fbx2glb --check-dependencies

# Show help
fbx2glb --help
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_utils.py

# Run with coverage
pytest --cov=fbx2glb
```

### Building the Package

```bash
# Build distribution
make build-package

# Publish to PyPI (requires credentials)
make publish-package
```

## PyPI Package

This project is available as a Python package on PyPI:

### 📦 [fbx2glb on PyPI](https://pypi.org/project/fbx2glb/)

```bash
# Install the latest version
pip install fbx2glb

# Install specific version
pip install fbx2glb==0.1.0

# Install with development dependencies
pip install fbx2glb[dev]
```

### Package Features

- ✅ **Ready to use**: Install and run immediately
- ✅ **Command line tools**: `fbx2glb`, `fbx2glb-batch`, `fbx2glb-component`
- ✅ **Multiple conversion methods**: FBX SDK, fbx2gltf, Blender
- ✅ **FBX upgrading**: Upgrade old FBX files automatically
- ✅ **Axis fixing**: Fix orientation issues in converted models
- ✅ **Batch processing**: Convert multiple files efficiently
- ✅ **Component generation**: Generate React/Three.js components

### Quick Start with PyPI

```bash
# Install
pip install fbx2glb

# Convert your first model
fbx2glb model.fbx model.glb --fix-axis

# Check what's available
fbx2glb --check-dependencies
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please check the [contributing guidelines](CONTRIBUTING.md) for more information.

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Install in development mode: `pip install -e '.[dev]'`
4. Make your changes
5. Add tests for new functionality
6. Run the test suite: `pytest`
7. Submit a pull request

## Acknowledgments

- [Facebook's FBX2glTF](https://github.com/facebookincubator/FBX2glTF) for the reference implementation
- [Autodesk FBX SDK](https://www.autodesk.com/developer-network/platform-technologies/fbx-sdk-2020-3) for the official FBX processing library
- [Blender](https://www.blender.org/) for the open-source 3D software integration
