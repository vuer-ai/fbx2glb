# FBX to GLB conversion tools Makefile

.PHONY: help install-fbx-sdk install-fbx2gltf convert-xbot convert-all-fbx check-system status build-package publish-package troubleshoot upgrade-xbot build-upgrade-tool clean

help:
	@echo "Available commands:"
	@echo "  make install-fbx-sdk       - Download and install the FBX SDK Python bindings"
	@echo "  make install-fbx2gltf      - Install Facebook's fbx2gltf tool (requires Homebrew)"
	@echo "  make build-upgrade-tool    - Build the FBX upgrade tool (requires FBX SDK)"
	@echo "  make convert-xbot          - Convert the XBot model using the FBX SDK"
	@echo "  make convert-xbot-fbx2gltf - Convert the XBot model using fbx2gltf"
	@echo "  make upgrade-xbot          - Upgrade XBot.fbx to newer version and convert"
	@echo "  make convert-all-fbx       - Convert all FBX files in the models directory"
	@echo "  make check-system          - Check system information"
	@echo "  make status                - Check installation status of required tools"
	@echo "  make troubleshoot          - Diagnose conversion issues and provide solutions"
	@echo "  make build-package         - Build the Python package"
	@echo "  make publish-package       - Publish the package to PyPI"
	@echo "  make clean                 - Clean intermediate files and build artifacts"

# FBX SDK Installation
install-fbx-sdk:
	@echo "Installing FBX SDK Python bindings..."
	@if [ "$$(uname)" = "Darwin" ]; then \
		echo "Detected macOS..."; \
		mkdir -p temp && cd temp && \
		cp ../local/fbx202037_fbxsdk_clang_macos.pkg . && \
		SUDO_ASKPASS=/bin/echo sudo -A installer -pkg fbx202037_fbxsdk_clang_macos.pkg -target / && \
		cd .. && rm -rf temp && \
		echo "FBX SDK installed successfully"; \
	else \
		echo "This command only supports macOS. For other platforms, please download the SDK from Autodesk's website."; \
	fi

# Build FBX upgrade tool
build-upgrade-tool:
	@echo "Building FBX upgrade tool..."
	@if [ ! -d "/Applications/Autodesk/FBX SDK/2020.3.7" ]; then \
		echo "Error: FBX SDK not found. Please run 'make install-fbx-sdk' first."; \
		exit 1; \
	fi
	@cd tools && \
	FBX_SDK_PATH="/Applications/Autodesk/FBX SDK/2020.3.7" && \
	CXXFLAGS="-std=c++11 -I$(FBX_SDK_PATH)/include -Wno-error=deprecated-declarations" && \
	LDFLAGS="-L$(FBX_SDK_PATH)/lib/clang/release" && \
	LIBS="-lfbxsdk" && \
	clang++ $(CXXFLAGS) -o upgrade_fbx upgrade_fbx.cpp $(LDFLAGS) $(LIBS) && \
	echo "FBX upgrade tool built successfully: tools/upgrade_fbx"

# Convert XBot model using FBX SDK
convert-xbot:
	@echo "Converting XBot model..."
	@if [ -f "examples/XBot.fbx" ]; then \
		python -m fbx2glb.cli examples/XBot.fbx examples/XBot.glb --verbose; \
	else \
		echo "XBot model not found. Expected at examples/XBot.fbx"; \
	fi

# Upgrade XBot model and convert
upgrade-xbot:
	@echo "Upgrading and converting XBot model..."
	@if [ -f "examples/XBot.fbx" ]; then \
		if [ ! -f "tools/upgrade_fbx" ]; then \
			echo "FBX upgrade tool not found. Building it first..."; \
			make build-upgrade-tool; \
		fi; \
		echo "Step 1: Upgrading FBX file using FBX SDK..."; \
		DYLD_LIBRARY_PATH="/Applications/Autodesk/FBX SDK/2020.3.7/lib/clang/release" ./tools/upgrade_fbx examples/XBot.fbx examples/XBot_upgraded.fbx; \
		echo "Step 2: Converting upgraded FBX to GLB with axis fixing..."; \
		python -m fbx2glb.cli examples/XBot_upgraded.fbx examples/XBot.glb --fix-axis --force --verbose; \
		echo "Conversion completed successfully!"; \
	else \
		echo "XBot model not found. Expected at examples/XBot.fbx"; \
	fi

# Troubleshoot conversion issues
troubleshoot:
	@echo "=== FBX2GLB Troubleshooting ==="
	@echo ""
	@echo "1. Checking dependencies..."
	@python -m fbx2glb.cli --check-dependencies
	@echo ""
	@echo "2. Analyzing XBot.fbx file..."
	@if [ -f "examples/XBot.fbx" ]; then \
		echo "File exists: examples/XBot.fbx"; \
		python -c "from fbx2glb.converter import detect_fbx_version; print('FBX Version:', detect_fbx_version('examples/XBot.fbx'))"; \
		echo "File size: $$(ls -lh examples/XBot.fbx | awk '{print $$5}')"; \
	else \
		echo "XBot.fbx not found in examples/ directory"; \
	fi
	@echo ""
	@echo "3. Common issues and solutions:"
	@echo "   - FBX version too old: Use Blender 3.x or upgrade FBX file"
	@echo "   - Missing dependencies: Install FBX SDK or fbx2gltf"
	@echo "   - Permission issues: Check file permissions and sudo access"
	@echo ""
	@echo "4. Available conversion methods:"
	@echo "   - Blender (current): Requires FBX 7.1+ for Blender 4.x"
	@echo "   - FBX SDK: Can upgrade FBX files to newer versions"
	@echo "   - fbx2gltf: Alternative conversion tool"

# Clean intermediate files and build artifacts
clean:
	@echo "Cleaning intermediate files and build artifacts..."
	@rm -f examples/XBot_upgraded.fbx
	@rm -f tools/upgrade_fbx
	@rm -rf temp/
	@rm -rf dist/
	@rm -rf build/
	@rm -rf *.egg-info/
	@find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@find . -name "*.pyc" -delete 2>/dev/null || true

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
