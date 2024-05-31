#!/usr/bin/env python3

"""
Load an html file and strip specified elements from it.
"""

import os
import argparse
import re
from bs4 import BeautifulSoup
from bs4.element import Comment

def strip_elements(html:str, elements:list) -> str:
    """
    Strip elements from an html file.

    Args:
        html (str): Path to the html file
        elements (list): List of elements to strip from the html file

    Returns:
        str: The stripped html
    """

    with open(html, "r") as f:
        soup = BeautifulSoup(f, "html.parser")

    # Remove specified elements
    for element in elements:
        tag, class_ = element
        for e in soup.find_all(tag, class_=re.compile(class_)):
            e.decompose()

    # Remove comments
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment.extract()

    return str(soup)

def main():
    parser = argparse.ArgumentParser(description="Strip elements from an html file")
    parser.add_argument("html", help="Path to the html file")
    args = parser.parse_args()

    elements = [("div", "nav-container"), # Navbar
                ("aside", "sidebar-container"), # Left sidebar
                ("a", "text-xs font-medium text-gray-500"), # View on GitHub link
                ("div", "mt-1.5 flex items-center gap-1 overflow-hidden"), # Breadcumbs
                ("button", "code-copy-btn"), # Copy code button
                ("title", ""), # Title
                ]

    stripped = strip_elements(args.html, elements)

    print(stripped)

if __name__ == "__main__":
    main()