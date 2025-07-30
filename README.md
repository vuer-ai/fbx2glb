# FBX2GLB

A versatile toolkit for converting FBX 3D models to GLB format for web applications.

## Features

- Convert FBX files to GLB format using multiple methods:
  - Autodesk FBX SDK (if available)
  - Facebook's fbx2gltf command line tool
  - Blender (if installed)
- Batch conversion of multiple files
- Generate React/Three.js components from 3D models
- Preserve animations, materials, and textures
- Support for various FBX versions

## Installation

### Basic Installation

```bash
pip install fbx2glb
```

### With Development Dependencies

```bash
pip install fbx2glb[dev]
```

## FBX SDK Installation (Optional)

For the best results, install the Autodesk FBX SDK:

### macOS

```bash
# Using the included Makefile
make -f scripts/Makefile install-fbx-sdk
```

### Windows

Download and install the [FBX SDK](https://www.autodesk.com/developer-network/platform-technologies/fbx-sdk-2020-3) from Autodesk.

## Usage

### Command Line

```bash
# Convert a single file
fbx2glb input.fbx [output.glb]

# Batch conversion
fbx2glb-batch source_directory [output_directory] --recursive

# Generate React/Three.js component
fbx2glb-component input.fbx [output_component.tsx]
```

### Python API

```python
from fbx2glb import convert_file, batch_convert, generate_component

# Convert a single file
convert_file("input.fbx", "output.glb")

# Batch convert
batch_convert("source_dir", "output_dir", recursive=True)

# Generate component
generate_component("input.fbx", "MyModel.tsx", component_name="MyModel")
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

## Examples

Check the `examples` directory for sample models and usage examples.

## License

MIT License

## Contributing

Contributions are welcome! Please check the [contributing guidelines](CONTRIBUTING.md) for more information.
