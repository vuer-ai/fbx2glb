# FBX to GLB conversion tools Makefile

.PHONY: help install-fbx-sdk install-fbx2gltf convert-xbot convert-all-fbx check-system status build-package publish-package

help:
	@echo "Available commands:"
	@echo "  make install-fbx-sdk       - Download and install the FBX SDK Python bindings"
	@echo "  make install-fbx2gltf      - Install Facebook's fbx2gltf tool (requires Homebrew)"
	@echo "  make convert-xbot          - Convert the XBot model using the FBX SDK"
	@echo "  make convert-xbot-fbx2gltf - Convert the XBot model using fbx2gltf"
	@echo "  make convert-all-fbx       - Convert all FBX files in the models directory"
	@echo "  make check-system          - Check system information"
	@echo "  make status                - Check installation status of required tools"
	@echo "  make build-package         - Build the Python package"
	@echo "  make publish-package       - Publish the package to PyPI"

# FBX SDK Installation
install-fbx-sdk:
	@echo "Installing FBX SDK Python bindings..."
	@if [ "$$(uname)" = "Darwin" ]; then \
		echo "Detected macOS..."; \
		mkdir -p temp && cd temp && \
		curl -O https://www.autodesk.com/content/dam/autodesk/www/adn/fbx/20202/fbx20202_fbxpythonsdk_macos.pkg && \
		sudo installer -pkg fbx20202_fbxpythonsdk_macos.pkg -target / && \
		cd .. && rm -rf temp && \
		echo "FBX SDK installed successfully"; \
	else \
		echo "This command only supports macOS. For other platforms, please download the SDK from Autodesk's website."; \
	fi

# Install fbx2gltf
install-fbx2gltf:
	@echo "Installing fbx2gltf..."
	@if [ "$$(uname)" = "Darwin" ]; then \
		if command -v brew >/dev/null 2>&1; then \
			brew install fbx2gltf; \
		else \
			echo "Homebrew not found. Please install Homebrew first or install fbx2gltf manually."; \
		fi \
	else \
		echo "This command only supports macOS with Homebrew. For other platforms, please install fbx2gltf manually."; \
	fi

# Convert XBot model using FBX SDK
convert-xbot:
	@echo "Converting XBot model..."
	@if [ -f "examples/XBot/XBot.fbx" ]; then \
		python -m fbx2glb.cli examples/XBot/XBot.fbx examples/XBot/XBot.glb --verbose; \
	else \
		echo "XBot model not found. Expected at examples/XBot/XBot.fbx"; \
	fi

# Convert XBot model using fbx2gltf
convert-xbot-fbx2gltf:
	@echo "Converting XBot model with fbx2gltf..."
	@if [ -f "examples/XBot/XBot.fbx" ]; then \
		python -m fbx2glb.cli examples/XBot/XBot.fbx examples/XBot/XBot.glb --method fbx2gltf --verbose; \
	else \
		echo "XBot model not found. Expected at examples/XBot/XBot.fbx"; \
	fi

# Convert all FBX files
convert-all-fbx:
	@echo "Converting all FBX files..."
	@python -m fbx2glb.batch public/models --recursive --verbose

# Check system info
check-system:
	@echo "System Information:"
	@echo "OS: $$(uname -s) $$(uname -r)"
	@echo "Python: $$(python --version 2>&1)"
	@echo "pip: $$(pip --version 2>&1)"
	@if command -v brew >/dev/null 2>&1; then \
		echo "Homebrew: $$(brew --version | head -1)"; \
	else \
		echo "Homebrew: Not installed"; \
	fi
	@if command -v fbx2gltf >/dev/null 2>&1; then \
		echo "fbx2gltf: Installed"; \
	else \
		echo "fbx2gltf: Not installed"; \
	fi
	@if command -v blender >/dev/null 2>&1; then \
		echo "Blender: $$(blender --version | head -1)"; \
	else \
		echo "Blender: Not found in PATH"; \
	fi

# Check installation status
status:
	@echo "Checking installation status..."
	@python -m fbx2glb.cli --check-dependencies

# Build Python package
build-package:
	@echo "Building Python package..."
	@pip install build
	@python -m build

# Publish to PyPI
publish-package:
	@echo "Publishing to PyPI..."
	@pip install twine
	@python -m twine upload dist/*
