from load_tbe_file import load_tbe_file

def main():
    file_path = "../data/example.tbe"
    data = load_tbe_file(file_path)
    print("Metadata:", data["metadata"])
    print("TBL1 Data:", data["tbl_data"]["TBL1"])
    print("TBL2 Attachments:", data["tbl_data"]["TBL2"]["attachments"])

if __name__ == "__main__":
    main()