import os
import platform
import subprocess

# Define the file paths
source_file = "c/src/functions/tbe_batch_processor.c"
output_dir = "c/src/functions"
shared_lib = os.path.join(output_dir, "tbe_batch_processor.so")

# Detect operating system
system = platform.system()

if system == "Darwin":  # macOS
    pkg_config_output = subprocess.check_output(["pkg-config", "--cflags", "--libs", "json-c"]).decode().strip()
    compile_command = ["gcc", "-shared", "-o", shared_lib, source_file] + pkg_config_output.split()
elif system == "Windows":
    include_dir = "C:\\json-c\\include"  # Update to match the Windows JSON-C path
    lib_dir = "C:\\json-c\\lib"
    shared_lib = os.path.join(output_dir, "tbe_batch_processor.dll")
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
