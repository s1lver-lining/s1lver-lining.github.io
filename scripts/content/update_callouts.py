if __name__ == '__main__':
    import sys
    sys.path.append('.')
    sys.path.append('..')

import argparse
import settings
import re

def extract_callouts(content:str) -> list:
    """
    Extract callouts from content

    A callout is in the form
    > *[type]* [name]
    > [content]
    > ...

    Args:
        content (str): Content of the file

    Returns:
        list: List of callouts (start, end) inclusive where start and end are line numbers (starting at 0) 
    """

    callouts = []
    lines = content.split('\n')
    start = 0
    end = 0
    current_indent = 0
    in_callout = False
    for i, line in enumerate(lines):
        if re.match(r'^([ ]*)> \*', line):
            current_indent = len(re.match(r'^([ ]*)> \*', line).group(1))
            if (line.startswith(' '*current_indent + '> *')) and line[current_indent+3] != '*' and "*" in line[current_indent+3:]:
                if in_callout:
                    end = i-1
                    while lines[end] == '' or lines[end] == ' '*current_indent + '>' or lines[end] == ' '*current_indent:
                        end -= 1
                    callouts.append((start, end, current_indent))
                    start = i
                    end = i
                else:
                    start = i
                    in_callout = True
        elif line.startswith(' '*current_indent + '>'):
            if in_callout:
                end = i
        else:
            if in_callout:
                end = i-1
                while lines[end] == '' or lines[end] == ' '*current_indent + '>' or lines[end] == ' '*current_indent:
                    end -= 1
                callouts.append((start, end, current_indent))
                in_callout = False
                current_indent = 0
    if in_callout:
        callouts.append((start, end, current_indent))
    return callouts

def create_callout_shortcode(content:str, callout:tuple) -> str:
    """
    Gerenate a callout shortcode

    Args:
        content (str): Content of the file
        callout (tuple): Callout offset (start, end) inclusive where start and end are line numbers (starting at 0)

    Returns:
        str: Callout shortcode
    """

    lines = content.split('\n')
    result_lines = []
    start  = callout[0]
    end    = callout[1]
    indent = callout[2]
    callout_type = lines[start][1:].split('*')[1].strip(":").strip()
    callout_name = lines[start][1:].split('*')[2].strip(":").strip()

    if callout_type.lower() in settings.CALLOUT_LIST:

        result_lines.append(" "*indent + "{{< callout/" + callout_type.lower() + " name=\"" + callout_name + "\" >}}")
        started = False
        for i in range(start+1, end+1):
            if lines[i] != (" "*indent + ">") or started:
                result_lines.append(lines[i][indent+1:])
                started = True
        while result_lines[-1] == "":
            result_lines.pop()
        result_lines.append(" "*indent + "{{< /callout/" + callout_type.lower() + " >}}")

    else:
        result_lines = lines[start:end+1]
    return '\n'.join(result_lines)

def update_callouts(content:str) -> str:
    """
    Update callouts in content

    Args:
        content (str): Content of the file

    Returns:
        str: Updated content
    """

    callouts = extract_callouts(content)
    content_lines = content.split('\n')
    updated_content = content
    for callout in callouts:
        updated_content = updated_content.replace('\n'.join(content_lines[callout[0]:callout[1]+1]), create_callout_shortcode(content, callout))
    return updated_content

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Add links to files in the content of the README.md file')
    parser.add_argument('file', help='Path to the file')
    args = parser.parse_args()

    content = ''
    with open(args.file, 'r') as f:
        content = f.read()

    print(extract_callouts(content))
    print(update_callouts(content))