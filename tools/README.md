# Tools Directory

This directory contains build tools and utilities for the fbx2glb project.

## FBX Upgrade Tool

### Files
- `upgrade_fbx.cpp` - C++ source code for the FBX file upgrade utility
- `upgrade_fbx` - Compiled binary (built from the source)

### Purpose
The FBX upgrade tool is used to upgrade FBX files to newer versions before conversion to GLB format. This is particularly useful when dealing with older FBX files that may not be compatible with modern conversion tools.

### Building
To build the upgrade tool, run:
```bash
make build-upgrade-tool
```

This requires the Autodesk FBX SDK to be installed. If it's not installed, run:
```bash
make install-fbx-sdk
```

### Usage
The upgrade tool is automatically used by the main conversion process when running:
```bash
make upgrade-xbot
```

Or it can be used manually:
```bash
./tools/upgrade_fbx input.fbx output.fbx
```

### Requirements
- Autodesk FBX SDK 2020.3.7 or later
- C++ compiler (clang++ on macOS)
- macOS (currently only supported platform) 