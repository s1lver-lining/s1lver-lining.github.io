import re
import settings

def update_links(content:str) -> str:
    """
    Update the links to local ressources in the content to be valid using lower case urls
    
    Args:
        content (str): The content of a README.md file
        code_blacklist (list): List of extenstions that are not code files
        filename_translation_dict (dict): Dictionary of filename translations

    Returns:
        str: The content of the README.md file with updated links
    """

    # Get potential links to other resources in the content: Search for [text](link)
    links = re.findall(r"\[([^\]]+)\]\(([^\)]+)\)", content)

    # Add src="" links: Search for src="link"
    links += re.findall(r"(src)=\"([^\"]+)\"", content)

    # For each link, update the link if the link is a local link
    for link in links:
        prev_link = link[1].strip()
        # Link to a local markdown file -> Same file link
        if prev_link.endswith("README.md") and not "http" in prev_link:

            # If the link have at least a directory, use it as a link
            if "/" in prev_link:
                new_link = "".join(prev_link.split("README.md")).lower().replace(" - ", "-").replace("%20-%20", "-").replace(" ", "-").replace("%20", "-")
                settings.filename_translation_dict[new_link.split("/")[-2]] = prev_link.split("/")[-2].replace("%20", " ")
                content = content.replace(prev_link, new_link)
            continue

        # Relative link to a local file -> make the link lower case
        if prev_link.startswith(".") and not prev_link.startswith("./_img"):
            new_link = prev_link.lower().replace(" - ", "-").replace("%20-%20", "-").replace(" ", "-").replace("%20", "-")

            # If the file have an extension, replace the last dot by a dash
            if "." in new_link.split("/")[-1]:
                filename = new_link.split("/")[-1]
                extension = filename.split(".")[-1].split("#")[0].split("?")[0]
                full_extension = "." + extension
                if full_extension not in settings.CODE_BLACKLIST:
                    new_link = new_link[::-1].replace(".", "-", 1)[::-1]
                    settings.filename_translation_dict[new_link.split("/")[-1]] = filename
            content = content.replace(prev_link, new_link)
            continue

    return content