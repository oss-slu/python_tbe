import os
import platform
import subprocess

# Define the file paths
source_file = "c/src/functions/tbe_batch_processor.c"
output_dir = "c/src/functions"
include_dir = "/opt/homebrew/Cellar/json-c/0.18/include/json-c"  # macOS default
lib_dir = "/opt/homebrew/Cellar/json-c/0.18/lib"                # macOS default

# Detect operating system
system = platform.system()

if system == "Darwin":  # macOS
    shared_lib = os.path.join(output_dir, "tbe_batch_processor.so")
    compile_command = [
        "gcc", "-shared", "-o", shared_lib, source_file,
        f"-I{include_dir}",
        f"-L{lib_dir}", "-ljson-c"
    ]
elif system == "Windows":
    # Adjust paths for Windows
    shared_lib = os.path.join(output_dir, "tbe_batch_processor.dll")
    include_dir = "C:\\json-c\\include"  # Update with your JSON-C path
    lib_dir = "C:\\json-c\\lib"          # Update with your JSON-C path
    compile_command = [
        "gcc", "-shared", "-o", shared_lib, source_file,
        f"-I{include_dir}",
        f"-L{lib_dir}", "-ljson-c"
    ]
else:
    raise OSError(f"Unsupported operating system: {system}")

# Run the compile command
try:
    print(f"Compiling shared library for {system}...")
    subprocess.run(compile_command, check=True)
    print(f"Shared library compiled: {shared_lib}")
except subprocess.CalledProcessError as e:
    print(f"Compilation failed: {e}")
