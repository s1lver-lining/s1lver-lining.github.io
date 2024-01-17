
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