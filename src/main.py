import os
import shutil

from page import generate_pages_recursive


def delete_directory_contents(dir: str):
    """
    Deletes all contents of the specified directory.

    Args:
        dir (str): The directory whose contents are to be deleted.
    """
    if os.path.exists(dir):
        for filename in os.listdir(dir):
            file_path = os.path.join(dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
        print(f"All contents of '{dir}' have been deleted.")
    else:
        raise FileNotFoundError(f"Directory '{dir}' does not exist.")


def copy_single_file(src: str, dest: str):
    """
    Copies a single file from src to dest.

    Args:
        src (str): Source file path.
        dest (str): Destination file path.
    """
    try:
        _ = shutil.copy2(src, dest)
        print(f"File copied from {src} to {dest}")
    except Exception as e:
        print(f"Failed to copy {src} to {dest}. Reason: {e}")


def create_directory(name: str, dest: str):
    """
    Creates a directory named 'name' inside the 'dest' directory.

    Args:
        name (str): Name of the directory to create.
        dest (str): Destination directory where the new directory will be created.
    """
    path = os.path.join(dest, name)
    try:
        os.makedirs(path, exist_ok=True)
        print(f"Directory '{name}' created at {path}")
    except Exception as e:
        print(f"Failed to create directory {path}. Reason: {e}")


def iterate_and_copy_files(src_dir: str, dest_dir: str):
    """
    Iterates over all files in src_dir and copies them to dest_dir.

    Args:
        src_dir (str): Source directory path.
        dest_dir (str): Destination directory path.
    """
    if not os.path.exists(src_dir):
        raise FileNotFoundError(f"Source directory '{src_dir}' does not exist.")

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for item in os.listdir(src_dir):
        s = os.path.join(src_dir, item)
        d = os.path.join(dest_dir, item)
        if os.path.isdir(s):
            create_directory(item, dest_dir)
            iterate_and_copy_files(s, d)
        else:
            copy_single_file(s, d)

    print(f"All contents from '{src_dir}' have been copied to '{dest_dir}'.")


def main():
    static_dir = "static"
    public_dir = "public"
    delete_directory_contents(public_dir)
    iterate_and_copy_files(static_dir, public_dir)
    generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()
