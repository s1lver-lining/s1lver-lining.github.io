import os

class Page():
    def __init__(self, content_path:str, target_path:str) -> None:
        """
        Initialize a Page object

        Args:
            content_path (str): Path to the content file
            target_path (str): Path to the target file
        """
        self.content_path = content_path
        self.target_path = target_path
        self.front_matter = {}
        self.FORCE_BYTES = False

    def get_content_path(self) -> str:
        """
        Return the content path

        Returns:
            str: Path to the content file
        """
        return self.content_path
    
    def get_target_path(self) -> str:
        """
        Return the target path

        Returns:
            str: Path to the target file
        """
        return self.target_path
    
    def get_front_matter(self) -> dict:
        """
        Return the front matter

        Returns:
            dict: Front matter
        """
        return self.front_matter
    
    def add_front_matter(self, key:str, value:str) -> None:
        """
        Add a key/value pair to the front matter

        Args:
            key (str): Key
            value (str): Value
        """
        self.front_matter[key] = value

    def set_layout(self, layout:str) -> None:
        """
        Set the layout

        Args:
            layout (str): Layout
        """
        self.add_front_matter('layout', layout)

    def set_title(self, title:str) -> None:
        """
        Set the title

        Args:
            title (str): Title
        """
        self.add_front_matter('title', title)

    def set_toc(self, toc:bool) -> None:
        """
        Set the table of contents

        Args:
            toc (bool): Table of contents
        """
        self.add_front_matter('toc', toc)

    def set_weight(self, weight:int) -> None:
        """
        Set the weight

        Args:
            weight (int): Weight
        """
        self.add_front_matter('weight', weight)

    def exclude_from_index(self) -> None:
        """
        Exclude the page from the search index
        """
        self.add_front_matter('excludeSearch', 'true')
        self.front_matter['sidebar'] = {'exclude': 'true'}
    
    def process_content(self, content:str) -> str:
        """
        Process the content

        Args:
            content (str): Content of the page

        Returns:
            str: Processed content
        """
        return content
    
    def process_content_bytes(self, content:bytes) -> bytes:
        """
        Process the content

        Args:
            content (bytes): Content of the page

        Returns:
            bytes: Processed content
        """
        return content
    
    def dict_to_yaml(self, int_dict:dict, indent:int=0) -> str:
        """
        Convert a dictionary to a YAML string

        Args:
            dict (dict): Dictionary to convert

        Returns:
            str: YAML string
        """
        yaml = ''
        for key, value in int_dict.items():
            if isinstance(value, dict):
                yaml += '  '*indent + f'{key}:\n'
                yaml += self.dict_to_yaml(value, indent+1)
            else:
                yaml += '  '*indent + f'{key}: {value}\n'
        return yaml
    
    def create_front_matter(self) -> str:
        """
        Generate the front matter from the parameters

        Returns:
            str: Front matter
        """
        front_matter = ''
        if self.front_matter != {}:
            front_matter += '---\n'
            front_matter += self.dict_to_yaml(self.front_matter)
            front_matter += '---\n'
        return front_matter

    def write(self) -> None:
        """
        Write the page to the target file
        """
        if self.FORCE_BYTES:
            self.write_bytes()
        else:
            # Read the content
            content = ""
            if self.content_path != "":
                if os.path.isfile(self.content_path):
                    with open(self.content_path, 'r') as f:
                        content = f.read()

            # Process the content
            content = self.process_content(content)

            # Create the front matter
            front_matter = self.create_front_matter()

            # Write the content to the target file
            with open(self.target_path, 'w') as f:
                f.write(front_matter + content)

    def write_bytes(self) -> None:
        """
        Write the page to the target file as bytes
        """

        # Read the content
        content = b""
        if self.content_path != "":
            if os.path.isfile(self.content_path):
                with open(self.content_path, 'rb') as f:
                    content = f.read()

        # Process the content
        content = self.process_content_bytes(content)

        # Create the front matter
        front_matter = self.create_front_matter()

        # Write the content to the target file
        with open(self.target_path, 'wb') as f:
            f.write(front_matter.encode('utf-8') + content)
    
