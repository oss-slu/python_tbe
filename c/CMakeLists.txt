# Specify the minimum version for CMake
cmake_minimum_required(VERSION 3.10)

# Define the project name
project(tbe_c)

# Place in build directorycd 
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})

# Add the executable and its source files
add_executable(main
    ../src/main.c
    ../src/functions/isolate_header.c
    ../src/functions/output_TBE.c
)

target_include_directories(main PRIVATE ../include/)