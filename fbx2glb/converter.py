"""
Core FBX to GLB conversion functionality.
"""

import os
import sys
import tempfile
import subprocess
import logging
from pathlib import Path
from typing import Optional, Dict, Any, Tuple, List, Callable

from .utils import find_conversion_tool, setup_logging

# Check for FBX SDK availability
try:
    import fbx
    FBX_SDK_AVAILABLE = True
except ImportError:
    FBX_SDK_AVAILABLE = False

logger = logging.getLogger(__name__)


def detect_fbx_version(file_path: str) -> str:
    """
    Detect the version of an FBX file.

    Args:
        file_path: Path to the FBX file

    Returns:
        String with FBX version information
    """
    try:
        with open(file_path, 'rb') as f:
            data = f.read(1024)  # Read the first 1KB

            # Check if it's a binary FBX (starts with 'Kaydara FBX Binary')
            if b'Kaydara FBX Binary' in data:
                # In binary FBX, the version is typically at byte offset 23
                try:
                    version = int.from_bytes(data[23:27], byteorder='little')
                    return f"Binary FBX {version / 1000}"  # Convert to standard format (e.g., 7400 -> 7.4)
                except Exception:
                    return "Binary FBX (version unknown)"
            else:
                # ASCII FBX - look for version pattern
                text_data = data.decode('utf-8', errors='ignore')

                # Look for version pattern
                import re
                version_match = re.search(r'FBXVersion: (\d+)', text_data)
                if version_match:
                    version = int(version_match.group(1))
                    return f"ASCII FBX {version / 1000}"

                # Alternative version pattern
                alt_version_match = re.search(r';FBX (\d+)', text_data)
                if alt_version_match:
                    version = int(alt_version_match.group(1))
                    return f"ASCII FBX {version}"

                return "ASCII FBX (version unknown)"
    except Exception as e:
        logger.error(f"Error detecting FBX version: {str(e)}")
        return "Unknown FBX format"


def convert_file(
    input_file: str,
    output_file: Optional[str] = None,
    method: Optional[str] = None,
    force: bool = False,
    verbose: bool = False,
    **kwargs
) -> bool:
    """
    Convert an FBX file to GLB format.

    Args:
        input_file: Path to the input FBX file
        output_file: Path to the output GLB file (optional)
        method: Conversion method to use ('fbx-sdk', 'fbx2gltf', 'blender')
        force: Force overwrite if output file exists
        verbose: Enable verbose output
        **kwargs: Additional method-specific parameters

    Returns:
        True if conversion was successful, False otherwise
    """
    # Setup logging
    log_level = logging.DEBUG if verbose else logging.INFO
    setup_logging(log_level)

    # Validate input file
    if not os.path.exists(input_file):
        logger.error(f"Input file '{input_file}' does not exist")
        return False

    # Determine output file if not specified
    if not output_file:
        input_base = os.path.splitext(input_file)[0]
        output_file = f"{input_base}.glb"

    # Check if output file exists
    if os.path.exists(output_file) and not force:
        logger.error(f"Output file '{output_file}' already exists. Use force=True to overwrite.")
        return False

    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Determine conversion method
    if not method:
        if FBX_SDK_AVAILABLE:
            method = 'fbx-sdk'
        else:
            method = find_conversion_tool()

    logger.info(f"Converting '{input_file}' to '{output_file}' using {method}")

    # Perform conversion
    if method == 'fbx-sdk':
        success = convert_with_fbx_sdk(input_file, output_file, verbose, **kwargs)
    elif method == 'fbx2gltf':
        success = convert_with_fbx2gltf(input_file, output_file, verbose, **kwargs)
    elif method == 'blender':
        success = convert_with_blender(input_file, output_file, verbose, **kwargs)
    else:
        logger.error(f"Unsupported conversion method: {method}")
        return False

    if success:
        input_size = os.path.getsize(input_file) / (1024 * 1024)  # MB
        output_size = os.path.getsize(output_file) / (1024 * 1024)  # MB
        compression_ratio = (1 - (output_size / input_size)) * 100 if input_size > 0 else 0

        logger.info(f"Conversion successful: {input_file} → {output_file}")
        logger.info(f"File size: {input_size:.2f} MB → {output_size:.2f} MB ({compression_ratio:.1f}% reduction)")
        return True
    else:
        logger.error(f"Conversion failed: {input_file}")
        return False


def convert_with_fbx_sdk(
    input_file: str,
    output_file: str,
    verbose: bool = False,
    **kwargs
) -> bool:
    """
    Convert FBX to GLB using the Autodesk FBX SDK
    """
    if not FBX_SDK_AVAILABLE:
        logger.error("Error: FBX SDK Python bindings not available.")
        return False

    try:
        # Initialize FBX SDK
        sdk_manager = fbx.FbxManager.Create()
        if not sdk_manager:
            logger.error("Error: Unable to create FBX Manager")
            return False

        if verbose:
            logger.debug(f"FBX SDK version: {fbx.FbxManager.GetVersion()}")

        # Create an IOSettings object
        ios = fbx.FbxIOSettings.Create(sdk_manager, fbx.IOSROOT)
        sdk_manager.SetIOSettings(ios)

        # Create an importer
        importer = fbx.FbxImporter.Create(sdk_manager, "")

        # Initialize the importer
        import_status = importer.Initialize(input_file, -1, sdk_manager.GetIOSettings())
        if not import_status:
            logger.error(f"Error: Unable to initialize FBX importer: {importer.GetStatus().GetErrorString()}")
            return False

        # Create a new scene
        scene = fbx.FbxScene.Create(sdk_manager, "")

        # Import the contents of the file into the scene
        importer.Import(scene)
        importer.Destroy()

        # Create an exporter
        exporter = fbx.FbxExporter.Create(sdk_manager, "")

        # Initialize the exporter
        # Unfortunately, FBX SDK doesn't directly support GLB export
        # We'll convert to FBX 7.4 binary format first
        temp_fbx = tempfile.NamedTemporaryFile(suffix=".fbx", delete=False).name
        export_status = exporter.Initialize(temp_fbx, -1, sdk_manager.GetIOSettings())

        if not export_status:
            logger.error(f"Error: Unable to initialize FBX exporter: {exporter.GetStatus().GetErrorString()}")
            return False

        # Export the scene
        exporter.Export(scene)
        exporter.Destroy()

        # Now convert the temp FBX to GLB using fbx2gltf or Blender
        conversion_tool = find_conversion_tool()
        if conversion_tool == 'fbx2gltf':
            result = convert_with_fbx2gltf(temp_fbx, output_file, verbose)
            os.unlink(temp_fbx)  # Clean up temp file
            return result
        elif conversion_tool == 'blender':
            result = convert_with_blender(temp_fbx, output_file, verbose)
            os.unlink(temp_fbx)  # Clean up temp file
            return result
        else:
            logger.error("Error: No suitable conversion tool found for FBX to GLB conversion")
            os.unlink(temp_fbx)  # Clean up temp file
            return False

    except Exception as e:
        logger.error(f"Error during FBX SDK conversion: {str(e)}")
        return False
    finally:
        # Destroy the SDK manager
        if 'sdk_manager' in locals():
            sdk_manager.Destroy()

    return True


def convert_with_fbx2gltf(
    input_file: str,
    output_file: str,
    verbose: bool = False,
    **kwargs
) -> bool:
    """
    Convert FBX to GLB using Facebook's fbx2gltf tool
    """
    try:
        cmd = ['fbx2gltf', '--binary', '--input', input_file, '--output', output_file]

        # Add additional arguments
        if kwargs.get('draco'):
            cmd.append('--draco')

        if kwargs.get('keep_attribute_info'):
            cmd.append('--keep-attribute-info')

        if kwargs.get('no_texture_optimization'):
            cmd.append('--no-texture-optimization')

        if verbose:
            logger.debug(f"Running command: {' '.join(cmd)}")
            result = subprocess.run(cmd)
        else:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode != 0:
            logger.error(f"Error during fbx2gltf conversion. Return code: {result.returncode}")
            if not verbose and result.stderr:
                logger.error(f"Error output: {result.stderr.decode('utf-8')}")
            return False

        # fbx2gltf adds .glb extension automatically, so we need to check if we need to rename
        if not output_file.endswith('.glb'):
            actual_output = f"{output_file}.glb"
            if os.path.exists(actual_output):
                os.rename(actual_output, output_file)

        return True
    except Exception as e:
        logger.error(f"Error during fbx2gltf conversion: {str(e)}")
        return False


def convert_with_blender(
    input_file: str,
    output_file: str,
    verbose: bool = False,
    **kwargs
) -> bool:
    """
    Convert FBX to GLB using Blender
    """
    # Create a temporary Python script for Blender
    blender_script = tempfile.NamedTemporaryFile(suffix=".py", delete=False)

    # Write conversion script to the temp file
    with open(blender_script.name, 'w') as f:
        f.write(f"""
import bpy
import sys
import os

# Clear default objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Import FBX
bpy.ops.import_scene.fbx(filepath="{input_file}", 
                         use_custom_props=True,
                         use_custom_props_enum_as_string=True,
                         use_anim=True, 
                         use_anim_action_all=True,
                         use_image_search=True)

# Export as GLB
bpy.ops.export_scene.gltf(filepath="{output_file}",
                         export_format='GLB',
                         export_animations=True,
                         export_anim_single_armature=True,
                         export_nla_strips=True,
                         export_texcoords=True,
                         export_normals=True,
                         export_materials='EXPORT',
                         export_colors=True,
                         export_cameras=True,
                         export_yup=True)

print("Conversion completed successfully")
""")

    try:
        # Find Blender executable
        blender_path = kwargs.get('blender_path')

        if not blender_path:
            for path in ['/Applications/Blender.app/Contents/MacOS/Blender', 'blender']:
                try:
                    result = subprocess.run([path, '--version'], 
                                          stdout=subprocess.PIPE, 
                                          stderr=subprocess.PIPE)
                    if result.returncode == 0:
                        blender_path = path
                        break
                except (FileNotFoundError, subprocess.SubprocessError):
                    continue

        if not blender_path:
            logger.error("Error: Blender executable not found")
            return False

        # Run Blender with the script
        cmd = [blender_path, '--background', '--python', blender_script.name]

        if verbose:
            logger.debug(f"Running command: {' '.join(cmd)}")
            result = subprocess.run(cmd)
        else:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode != 0:
            logger.error(f"Error during Blender conversion. Return code: {result.returncode}")
            if not verbose and result.stderr:
                logger.error(f"Error output: {result.stderr.decode('utf-8')}")
            return False

        return os.path.exists(output_file)
    except Exception as e:
        logger.error(f"Error during Blender conversion: {str(e)}")
        return False
    finally:
        # Clean up the temporary script
        os.unlink(blender_script.name)


if __name__ == "__main__":
    # Simple CLI for testing
    if len(sys.argv) < 2:
        print("Usage: python converter.py input.fbx [output.glb]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    success = convert_file(input_file, output_file, verbose=True)
    sys.exit(0 if success else 1)
