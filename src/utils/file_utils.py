import io

def read_utf8_file(file_path: str) -> str:
    """
    Reads the entire content of a file using UTF-8 encoding.

    This utility function ensures that files are opened with the correct encoding,
    preventing common issues with special characters.

    Args:
        file_path (str): The absolute or relative path to the file to read.

    Returns:
        str: The content of the file as a string.

    Raises:
        FileNotFoundError: If the file does not exist.
        IOError: If there is an error reading the file.
    """
    with io.open(file_path, mode="r", encoding="utf-8") as file:
        return file.read()
