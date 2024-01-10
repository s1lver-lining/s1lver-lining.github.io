import argparse
import os
import re

def extract_paragraphs(content:str) -> list:
    """
    Extract paragraphs from content

    A paragraph is a string starting with * or - followed by indented lines

    Args:
        content (str): Content of the file

    Returns:
        list: List of paragraph offsets (start, end) inclusive where start and end are line numbers (starting at 0) 
    """
    paragraphs = []
    lines = content.split('\n')
    start = 0
    end = 0
    in_paragraph = False
    for i, line in enumerate(lines):
        if line.startswith('* ') or line.startswith('- '):
            if in_paragraph:
                end = i-1
                while lines[end] == '' or lines[end] == "  ":
                    end -= 1
                paragraphs.append((start, end))
                start = i
                end = i
            else:
                start = i
                in_paragraph = True
        elif line.startswith('  ') or line.startswith('\t') or line == '':
            if in_paragraph:
                end = i
        else:
            if in_paragraph:
                end = i-1
                while lines[end] == '' or lines[end] == "  ":
                    end -= 1
                paragraphs.append((start, end))
                in_paragraph = False
    if in_paragraph:
        paragraphs.append((start, end))
    return paragraphs

def extract_links(content:str, paragraph:tuple) -> list:
    """
    Extract links from a paragraph

    Args:
        content (str): Content of the file
        paragraph (tuple): Paragraph offset (start, end) inclusive where start and end are line numbers (starting at 0)

    Returns:
        list: List of links (line, link) where line is the line number (starting at 0) and link is the link
    """
    links = []
    lines = content.split('\n')
    link_regex = r"\[([^\]]+)\]\(([^\)]+)\)"

    for i in range(paragraph[0], paragraph[1]+1):
        line = lines[i]
        matches = re.findall(link_regex, line)
        for m in matches:
            links.append((i, m[1]))
    return links


def create_file_shortcode(filename:str, path:str) -> str:
    """
    Create a file shortcode

    Args:
        filename (str): Filename
        path (str): Path to the file

    Returns:
        str: File shortcode
    """
    if path.endswith("/"):
        return "{{< local-links/folder name=\"" + filename + "\" path=\"" + path + "\" >}}"
    return "{{< local-links/file name=\"" + filename + "\" path=\"" + path + "\" >}}"
        

def add_file_links(content:str, filename_translation_dict:dict) -> str:
    """
    Add links to mentioned files at the bottom of content paragraphs

    Args:
        content (str): Content of the file
        filename_translation_dict (dict): Dictionary of filename translations
    """
    paragraphs = extract_paragraphs(content)
    result_lines = content.split('\n')
    offset = 0
    for p in paragraphs:
        links = extract_links(content, p)
        local_links = [l for l in links if l[1].startswith('.')]
        if len(local_links) > 0:
            result_lines.insert(p[1]+offset+1, "    {{< local-links/container >}}")
            offset += 1
            for l in local_links:
                filename = os.path.basename(l[1].strip("/"))
                if filename in filename_translation_dict:
                    filename = filename_translation_dict[filename]
                shortcode = "        " + create_file_shortcode(filename, l[1])
                result_lines.insert(p[1]+offset+1, shortcode)
                offset += 1
            result_lines.insert(p[1]+offset+1, "    {{< /local-links/container >}}")
            offset += 1
    return '\n'.join(result_lines)
                


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add links to mentioned files at the bottom of content paragraphs')
    parser.add_argument('file', help='Path to the file (ex: /path/to/file)')
    args = parser.parse_args()

    with open(args.file, 'r') as f:
        content = f.read()

    paragraphs = extract_paragraphs(content)
    for p in paragraphs:
        print((p[0]+1, p[1]+1), extract_links(content, p))
    print(add_file_links(content))