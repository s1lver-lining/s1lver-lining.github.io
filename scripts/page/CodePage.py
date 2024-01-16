import subprocess
import random

from settings import CODE_BLACKLIST, filename_translation_dict
from content.update_links import update_links
from content.add_file_links import add_file_links

from page.Page import Page

class CodePage(Page):
    """
    Regular page
    """

    def __init__(self, content_path:str, target_path:str, extension:str) -> None:
        super().__init__(content_path, target_path)
        self.extension = extension

        self.FORCE_BYTES = True

        self.set_layout('code')
        self.add_front_matter('math', 'true')
        self.exclude_from_index()

    def process_content_bytes(self, content:bytes) -> bytes:

        if self.extension == '.ipynb':
            content = self.process_ipynb(content)
        else:
            content = '```'.encode('utf-8') + self.extension[1:].encode('utf-8') + '\n'.encode('utf-8') + content + '\n````\n'.encode('utf-8')
        return super().process_content_bytes(content)
    
    def process_ipynb(self, content:bytes) -> bytes:
        """
        Process ipynb content
        """

        # Convert the ipynb to markdown
        proc = subprocess.run(['jupyter-nbconvert', '--to', 'markdown', '--stdin', '--stdout'], input=content, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        content = proc.stdout

        return content
    