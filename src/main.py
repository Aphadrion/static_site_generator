import os
import shutil
from generator import generate_pages_recursive
from copystatic import copy_files_recursive
import sys

dir_path_static = "./static"
dir_path_public = "./docs"

def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    base_path = sys.argv[1] if len(sys.argv) > 1 else "/"
    print(f"The base path is: {base_path}")

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    print("Generating web pages...")
    generate_pages_recursive("./content/", "./template.html", dir_path_public, base_path)

    print("Site generation complete!")

if __name__ == "__main__":
    main()
