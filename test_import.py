import fbx2glb
print("Package attributes:", dir(fbx2glb))
print("__version__ exists:", hasattr(fbx2glb, "__version__"))
print("convert_file exists:", hasattr(fbx2glb, "convert_file"))
print("__version__:", getattr(fbx2glb, "__version__", None))
print("convert_file:", getattr(fbx2glb, "convert_file", None))