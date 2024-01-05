#!/usr/bin/env python3

import os
import json

from update_links import update_links

README_FILENAME = "README.md"
INDEX_FILENAME = "_index.md"
TOPICS_FILENAME = "topics.json"
ICON_FILENAME = "icon.svg"

TOOLS_DIRNAMES = ["Tools", "tools", "_files", "_Files"]
CODE_BLACKLIST = [".md", ".png", ".jpg"]

def process_tools_dir(directory: str) -> None:
    """
    Create a hugo version of the Tools directory:

    For each folder, create an empty _index.md file
    and for each file create a mardown copy with code blocks.

    The name of the code file is the name of the original file with a -<extension> suffix,
    else, hugo crashes when building file.ext and file.ext.py for example.
    This will not be nessesary anymore if we store the content of the submodules outsite of the content directory.
    
    Args:
        directory (str): Path to the Tools directory (ex: /path/to/Tools)
    """

    last_dir = os.path.basename(directory)

    # If the name of the directory is not "Tools", create an empty _index.md file
    if last_dir not in TOOLS_DIRNAMES:
        content = ""
        if os.path.isfile(os.path.join(directory, README_FILENAME)):
            with open(os.path.join(directory, README_FILENAME), 'r') as f:
                content = f.read()
        with open(os.path.join(directory, INDEX_FILENAME), 'w') as f:
            f.write(f'---\ntitle: {last_dir}\nsidebar:\n  exclude: true\nmath: true\nlayout: code-list\n---\n{content}')

    # Process each file in the directory
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)

        # If the file is a directory, process it
        if os.path.isdir(file_path):
            process_tools_dir(file_path)
            continue

        # If the file is a file, process it
        else:

            # If the file is not a code file, skip it
            path_name, file_ext = os.path.splitext(file_path)
            if not file_ext in CODE_BLACKLIST and file_ext != "":
                # Create a hugo version of the file
                with open(file_path, 'rb') as f:
                    content = f.read()

                # Check for name conflicts
                if os.path.isfile(os.path.join(directory, path_name + "-" + file_ext[1:])):
                    print(f"WARNING: {path_name + '-' + file_ext[1:]} exists in {directory} and conflicts with {file}. Skipping {file}")

                with open(path_name + "-" + file_ext[1:] + ".md", 'wb') as f:
                    f.write(f'---\ntitle: {file}\nsidebar:\n  exclude: false\nmath: true\nlayout: code\n---\n```'.encode('utf-8') + file_ext[1:].encode('utf-8') + '\n'.encode('utf-8') + content + '\n````\n'.encode('utf-8'))


def process_readme_file(directory:str, readme_file:str, index_file:str, last_dir:str) -> None:
    """
    Process the README.md file of a directory:
    - Copy the content of the README.md file to the _index.md file
    - Find the order of the folder in the $directory/../topics.json file if it exists, and add it to the front matter

    Args:
        directory (str): Path to the directory (ex: /path/to)
        readme_file (str): Path to the README.md file (ex: /path/to/README.md)
        index_file (str): Path to the _index.md file (ex: /path/to/_index.md)
        last_dir (str): Name of the directory (ex: to)
    """

    # Find the order of the folder in the $directory/../topics.json file if it exists
    order = 0
    topics_file = os.path.join(os.path.dirname(directory), TOPICS_FILENAME)
    if os.path.isfile(topics_file):
        with open(topics_file, 'r') as f:
            topics = json.load(f)
            try:
                order = topics.index(last_dir)+1
            except ValueError:
                order = -1

    # Copy the content of the README.md file to the _index.md file
    # only if the order is not -1
    if order != -1:
        with open(readme_file, 'r') as f:
            content = f.read()
        
        # Replace tabs in content with 4 spaces
        content = content.replace('\t', '    ')

        # Update the links in the content
        content = update_links(content, CODE_BLACKLIST)

        # Add the order to the front matter
        content = f'---\ntitle: {last_dir}\nweight: {order}\nmath: true\n---\n{content}'

        with open(index_file, 'w') as f:
            f.write(content)

def is_file_in_tools_dir(file: str) -> bool:
    """
    Check if a file is in the Tools directory

    Args:
        file (str): Path to the file (ex: /path/to/file)
    
    Returns:
        bool: True if the file is in the Tools directory, False otherwise
    """

    # List directories in the path
    dirs = file.split(os.sep)

    for d in dirs:
        if d in TOOLS_DIRNAMES:
            return True
    return False

def main():

    # Define the base directory as the first argument of the script
    base_dir = os.sys.argv[1]

    # Use os.walk to recursively search for README.md files
    for directory, _, _ in os.walk(base_dir):

        # Define the path of the _index.md and README.md files
        readme_file = os.path.join(directory, README_FILENAME)
        index_file = os.path.join(directory, INDEX_FILENAME)

        # Last directory name
        last_dir = os.path.basename(directory)

        # If the README.md file exists, pour it to _index.md
        if os.path.isfile(readme_file) and not is_file_in_tools_dir(readme_file):
            process_readme_file(directory, readme_file, index_file, last_dir)
        
        # If the directory is named "Tools", create a special _index.md file
        elif last_dir in TOOLS_DIRNAMES:
            last_last_dir = os.path.basename(os.path.dirname(directory))
            with open(index_file, 'w') as f:
                f.write(f'---\ntitle: {last_last_dir} {last_dir}\nsidebar:\n  exclude: true\nmath: true\nroottoolsection: true\nlayout: code-list\n---\n')
            process_tools_dir(directory)

        # If the README.md file does not exist, create an empty _index.md file that does not appear in the sidebar
        elif not is_file_in_tools_dir(readme_file):
            with open(index_file, 'w') as f:
                f.write(f'---\ntitle: {last_dir}\nsidebar:\n  exclude: true\nmath: true\n---\n')
        

    # Prepend front matter to the _index.md file of the root directory
    with open(os.path.join(base_dir, README_FILENAME), 'r') as f:
        content = f.read()
    with open(os.path.join(base_dir, INDEX_FILENAME), 'w') as f:
        f.write(f'---\nlayout: sectionroot\ntoc: false\nmath: true\n---\n{content}')

if __name__ == "__main__":
    main()