#!/bin/bash

# Define the base directory as the first argument of the script
base_dir="$1"

# Use find to recursively search for README.md files
find "$base_dir" -type d | while read -r directory; do

    # Define the path of the _index.md and README.md files
    readme_file="$directory/README.md"
    index_file="$directory/_index.md"


    # If the README.md file exists, pour it to _index.md
    if [ -f "$readme_file" ]; then

        # Last directory name
        last_dir=$(basename "$directory")

        # Find the order of the folder in the $directory/../topics.json file if it exists
        order=0
        topics_file="$(dirname "$directory")/topics.json"
        if [ -f "$topics_file" ]; then
            order=$(awk -v RS=',|\\[|\\]' -v keyword="$last_dir" 'BEGIN {found=-1} {if ($0 ~ keyword) {found=NR-1; exit}} END {print found}' "$topics_file")
            order=$((order+0))
        fi

        # Copy the content of the README.md file to the _index.md file
        # only if the order is not -1
        if [ "$order" -ne "-1" ]; then
            printf -- '---\ntitle: %s\nweight: %s\nmath: true\n---\n' "$last_dir" "$order" | cat - "$readme_file" > "$index_file"
        fi
    
    # If the README.md file does not exist, create an empty _index.md file that does not appear in the sidebar
    else
        printf -- '---\ntitle: %s\nsidebar:\n  exclude: true\nmath: true\n---\n' "$last_dir" > "$index_file"
    fi



done

# Prepend front matter to the _index.md file of the root directory
printf -- '---\nlayout: sectionroot\ntoc: false\nmath: true\n---\n' | cat - "$base_dir/README.md" > "$base_dir/_index.md"

