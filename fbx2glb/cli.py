"""
Command-line interface for fbx2glb.
"""

import os
import sys
import argparse
import logging
from pathlib import Path

from .converter import convert_file
from .utils import setup_logging, check_dependencies

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Convert FBX files to GLB format')
    parser.add_argument('input_file', help='Path to input FBX file')
    parser.add_argument('output_file', nargs='?', help='Path to output GLB file (optional)')
    parser.add_argument('--method', choices=['fbx-sdk', 'fbx2gltf', 'blender'], 
                       help='Conversion method to use')
    parser.add_argument('--force', '-f', action='store_true', help='Force overwrite if output file exists')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')

    # Advanced options
    parser.add_argument('--draco', action='store_true', help='Use Draco compression (fbx2gltf only)')
    parser.add_argument('--no-texture-optimization', action='store_true', help='Disable texture optimization (fbx2gltf only)')
    parser.add_argument('--keep-attribute-info', action='store_true', help='Keep attribute info (fbx2gltf only)')
    parser.add_argument('--blender-path', help='Path to Blender executable')

    # Utility commands
    parser.add_argument('--check-dependencies', action='store_true', help='Check for required dependencies and exit')
    parser.add_argument('--version', action='store_true', help='Show version information and exit')

    return parser.parse_args()


def main() -> int:
    """Main entry point for single file conversion."""
    args = parse_args()

    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    setup_logging(log_level)

    # Handle utility commands
    if args.check_dependencies:
        deps = check_dependencies()
        print("FBX2GLB Dependencies:")
        print(f"  FBX SDK: {'✅' if deps['fbx_sdk'] else '❌'}")
        print(f"  fbx2gltf: {'✅' if deps['fbx2gltf'] else '❌'}")
        print(f"  Blender: {'✅' if deps['blender'] else '❌'}")
        print(f"  NumPy: {'✅' if deps['numpy'] else '❌'}")

        # Check if at least one conversion method is available
        if not (deps['fbx_sdk'] or deps['fbx2gltf'] or deps['blender']):
            print("\n❌ No conversion methods available. Please install at least one of:")
            print("  - Autodesk FBX SDK Python bindings")
            print("  - Facebook's fbx2gltf command line tool")
            print("  - Blender")
            return 1
        else:
            print("\n✅ At least one conversion method is available.")
            return 0

    if args.version:
        from . import __version__
        print(f"fbx2glb version {__version__}")
        return 0

    # Validate input file
    if not os.path.exists(args.input_file):
        logger.error(f"Input file '{args.input_file}' does not exist")
        return 1

    # Extract kwargs for additional parameters
    kwargs = {
        'draco': args.draco,
        'no_texture_optimization': args.no_texture_optimization,
        'keep_attribute_info': args.keep_attribute_info,
        'blender_path': args.blender_path
    }

    # Perform conversion
    success = convert_file(
        args.input_file,
        args.output_file,
        method=args.method,
        force=args.force,
        verbose=args.verbose,
        **kwargs
    )

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
