## isolate_header

(Add your content here)

## output_csv

(Add your content here)

## output_TBE

(Add your content here)

## read_directory

(Add your content here)

## read_TBE

### Getting Started

#### Prerequisites

- **Rust**: Make sure you have [Rust](https://www.rust-lang.org/learn/get-started) installed.
- **Cargo**: Rust's package manager, which is bundled with the Rust installation.
- **Install VS Code extensions**: Rust Extension Pack and rust-analyzer and Cargo
- **Check environment variables**: /home/<your-username>/.cargo/bin (for example)
-  Check the installations:
    rustc --version and cargo --version


### Installation

1. Clone the repository to your local machine: git clone https://github.com/oss-slu/tbe.git
2. Go to tbe/rust/
3. Initialize a New Cargo Project - cargo init (if it's not existed)
4. This will create a Cargo.toml file
5. Then , the folder structure should be like 
        rust/
        ├── Cargo.toml
        ├── src/
        │   └── main.rs
6. Ensure you've the necessary dependencies in Cargo.toml
7. Change the path to your sample_data/example.csv as required
8. Run the project from the rust/ directory using - cargo run
9. When you run it'll build the project - Cargo.lock and target/ directory
10. If you already have Cargo.lock and no target/ dir then use " cargo build " to build the project




## strip_header

(Add your content here)

## unit_tests

(Add your content here)

## validate_TBE

(Add your content here)
