import io

def read_utf8_file(file_path: str) -> str:
    with io.open(file_path, mode="r", encoding="utf-8") as file:
        return file.read()
