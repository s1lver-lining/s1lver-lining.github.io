from content.update_links import update_links
from content.add_file_links import add_file_links
from content.update_callouts import update_callouts

from page.Page import Page

class IndexPage(Page):
    """
    Regular page
    """

    def __init__(self, content_path:str, target_path:str) -> None:
        super().__init__(content_path, target_path)
        self.add_front_matter('math', 'true')

    def process_content(self, content:str) -> str:

        # Replace tabs in content with 4 spaces
        content = content.replace('\t', '    ')

        # Update the links in the content
        content = update_links(content)

        # Add file shortcode to the content
        content = add_file_links(content)

        # Replace callouts with the appropriate shortcodes
        content = update_callouts(content)

        content = content.replace("\{", " \lbrace ").replace("\}", " \\rbrace ")
        content = content.replace("\\\\", "\\\\\\\\")

        return super().process_content(content)