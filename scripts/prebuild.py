#!/usr/bin/env python3

import os
import json

README_FILENAME = "README.md"
INDEX_FILENAME = "_index.md"
TOPICS_FILENAME = "topics.json"

TOOLS_DIRNAMES = ["Tools", "tools", "_files", "_Files"]
CODE_BLACKLIST = [".md", ".png", ".jpg"]

def process_tools_dir(directory: str) -> None:
    """
    Create a hugo version of the Tools directory:

    For each folder, create an empty _index.md file
    and for each file create a mardown copy with code blocks.
    
    Args:
        directory (str): Path to the Tools directory (ex: /path/to/Tools)
    """

    last_dir = os.path.basename(directory)

    # If the name of the directory is not "Tools", create an empty _index.md file
    if last_dir not in TOOLS_DIRNAMES:
        with open(os.path.join(directory, INDEX_FILENAME), 'w') as f:
            f.write(f'---\ntitle: {last_dir}\nsidebar:\n  exclude: true\nmath: true\nlayout: code-list---\n')

    # Process each file in the directory
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)

        # If the file is a directory, process it
        if os.path.isdir(file_path):
            process_tools_dir(file_path)
            continue

        path_name, file_ext = os.path.splitext(file_path)
        if file_ext in CODE_BLACKLIST or file_ext == "":
            continue

        # Create a hugo version of the file
        with open(file_path, 'rb') as f:
            content = f.read()
        with open(path_name + ".md", 'wb') as f:
            f.write(f'---\ntitle: {file}\nsidebar:\n  exclude: false\nmath: true\nlayout: code\n---\n```'.encode('utf-8') + file_ext[1:].encode('utf-8') + '\n'.encode('utf-8') + content + '\n````\n'.encode('utf-8'))


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
    if os.path.isfile(readme_file):

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
            with open(index_file, 'w') as f:
                f.write(f'---\ntitle: {last_dir}\nweight: {order}\nmath: true\n---\n{content}')
    
    # If the directory is named "Tools", create a special _index.md file
    elif last_dir in TOOLS_DIRNAMES:
        last_last_dir = os.path.basename(os.path.dirname(directory))
        with open(index_file, 'w') as f:
            f.write(f'---\ntitle: {last_last_dir} {last_dir}\nsidebar:\n  exclude: true\nmath: true\nroottoolsection: true\n---\n')
        process_tools_dir(directory)

    # If the README.md file does not exist, create an empty _index.md file that does not appear in the sidebar
    else:
        with open(index_file, 'w') as f:
            f.write(f'---\ntitle: {last_dir}\nsidebar:\n  exclude: true\nmath: true\n---\n')
    

# Prepend front matter to the _index.md file of the root directory
with open(os.path.join(base_dir, README_FILENAME), 'r') as f:
    content = f.read()
with open(os.path.join(base_dir, INDEX_FILENAME), 'w') as f:
    f.write(f'---\nlayout: sectionroot\ntoc: false\nmath: true\n---\n{content}')