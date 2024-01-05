import re

def update_links(content:str, code_blacklist:list) -> str:
    """
    Update the links to local ressources in the content to be valid using lower case urls
    
    Args:
        content (str): The content of a README.md file
        code_blacklist (list): List of extenstions that are not code files

    Returns:
        str: The content of the README.md file with updated links
    """

    # Get potential links to other resources in the content: Search for [text](link)
    links = re.findall(r"\[([^\]]+)\]\(([^\)]+)\)", content)

    # Add src="" links: Search for src="link"
    links += re.findall(r"(src)=\"([^\"]+)\"", content)

    # For each link, update the link if the link is a local link
    for link in links:

        # Link to a local markdown file -> Same file link
        if link[1].endswith("README.md") and not "http" in link[1]:

            # If the link have at least a directory, use it as a link
            if "/" in link[1]:
                new_link = "".join(link[1].split("README.md")).lower().replace(" ", "-").replace("%20", "-")
                content = content.replace(link[1], new_link)
            continue

        # Relative link to a local file -> make the link lower case
        if link[1].startswith(".") and not link[1].startswith("./_img"):
            new_link = link[1].lower().replace(" ", "-").replace("%20", "-")

            # If the file have an extension, replace the last dot by a dash
            if "." in new_link.split("/")[-1]:
                extension = "." + new_link.split("/")[-1].split(".")[-1].split("#")[0].split("?")[0]
                if extension not in code_blacklist:
                    new_link = new_link[::-1].replace(".", "-", 1)[::-1]
            content = content.replace(link[1], new_link)
            continue

    return content