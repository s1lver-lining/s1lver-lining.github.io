from settings import CODE_BLACKLIST, filename_translation_dict
from content.update_links import update_links
from content.add_file_links import add_file_links

from page.Page import Page

class CodeIndexPage(Page):
    """
    Listing of code files
    """

    def __init__(self, content_path:str, target_path:str) -> None:
        super().__init__(content_path, target_path)
        self.set_layout('code-list')
        self.add_front_matter('math', 'true')
        self.exclude_from_index()