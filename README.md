# FBX2GLB

A versatile toolkit for converting FBX 3D models to GLB format for web applications.

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

```bash
# Clone the repository
git clone https://github.com/fortyfive-ai/fbx2glb.git
cd fbx2glb

# Install in development mode
pip install -e '.[dev]'
```

### Basic Usage

```bash
# Convert a single FBX file to GLB
python -m fbx2glb.cli examples/XBot.fbx examples/XBot.glb

# Check available conversion methods
python -m fbx2glb.cli --check-dependencies

# Generate a React/Three.js component
python -m fbx2glb.component examples/XBot.fbx src/components/XBotModel.tsx
```

## Installation

### Basic Installation

```bash
pip install fbx2glb
```

### Development Installation

```bash
git clone https://github.com/fortyfive-ai/fbx2glb.git
cd fbx2glb
pip install -e '.[dev]'
```

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
python -m fbx2glb.cli model.fbx model.glb

# Convert with specific method
python -m fbx2glb.cli model.fbx model.glb --method fbx2gltf

# Convert with FBX upgrading
python -m fbx2glb.cli old_model.fbx new_model.glb --upgrade-fbx
```

### Batch Processing

```bash
# Convert all FBX files in a directory
python -m fbx2glb.batch models/ output/ --recursive

# Convert with parallel processing
python -m fbx2glb.batch models/ output/ --parallel 4 --force
```

### Component Generation

```bash
# Generate a React component
python -m fbx2glb.component character.fbx CharacterModel.tsx

# Generate with custom name
python -m fbx2glb.component character.fbx CharacterModel.tsx --name CharacterModel
```

## Troubleshooting

### Common Issues

1. **FBX version too old:**
   ```bash
   # Use FBX upgrading
   python -m fbx2glb.cli old_model.fbx new_model.glb --upgrade-fbx
   ```

2. **No conversion methods available:**
   ```bash
   # Check what's available
   python -m fbx2glb.cli --check-dependencies
   
   # Install FBX SDK
   make install-fbx-sdk
   ```

3. **Blender not found:**
   ```bash
   # Specify Blender path
   python -m fbx2glb.cli model.fbx model.glb --blender-path /path/to/blender
   ```

### Getting Help

```bash
# Run the troubleshooting command
make troubleshoot

# Check system information
python -m fbx2glb.cli --check-dependencies
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
