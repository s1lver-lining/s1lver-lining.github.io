import subprocess
import os

from page.Page import Page

class CodePage(Page):
    """
    Regular page
    """

    def __init__(self, content_path:str, target_path:str, extension:str, use_cache=True) -> None:
        super().__init__(content_path, target_path)
        self.extension = extension
        self.FORCE_BYTES = True
        self.use_cache = use_cache

        self.set_layout('code')
        self.add_front_matter('math', 'true')
        self.exclude_from_index()
        self.set_toc(False)

    def process_content_bytes(self, content:bytes) -> bytes:

        if self.extension == '.ipynb':
            content = self.process_ipynb(content)
        if self.extension == '.pdf':
            content = 'Use the above buttons to interact with this file'.encode('utf-8')
        else:
            content = '```'.encode('utf-8') + self.extension[1:].encode('utf-8') + '\n'.encode('utf-8') + content + '\n````\n'.encode('utf-8')
        return super().process_content_bytes(content)
    
    def process_ipynb(self, input_content:bytes) -> bytes:
        """
        Process ipynb content
        """
        output_content = ""

        if self.use_cache:
            # Check if the cache exists
            cache_filename = self.target_path + '.cache'

            # Get the last modification date of the cache file if it exists
            cache_mtime = 0
            if os.path.exists(cache_filename):
                cache_mtime = os.path.getmtime(cache_filename)

            # Get the last modification date of the source file
            source_mtime = os.path.getmtime(self.content_path)

            # If the cache is up to date, use it
            if cache_mtime >= source_mtime and os.path.exists(cache_filename):
                with open(cache_filename, 'rb') as f:
                    return f.read()
                
        # Convert the ipynb to markdown
        proc = subprocess.run(['jupyter-nbconvert', '--to', 'markdown', '--stdin', '--stdout'], input=input_content, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output_content = proc.stdout

        # Save the cache
        with open(cache_filename, 'wb') as f:
            f.write(output_content)

        return output_content    
