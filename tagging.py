import json

class TagManager:
    def __init__(self, filepath: str):
        self.file_path = filepath
        self.tag_dictionary = {}

    def unpack_file(self):
        with open(self.file_path) as f:
            self.tag_dictionary = json.load(f)

    def pack_file(self):
        with open(self.file_path) as f:
            json.dump(self.tag_dictionary, f)

    def add(self, image_file_path: str, tag: str):
        # Create tag list for image if necessary.
        if image_file_path not in self.tag_dictionary:
            self.tag_dictionary[image_file_path] = []
        
        # Add tag to tag list if not already there.
        if tag not in self.tag_dictionary[image_file_path]:
            self.tag_dictionary[image_file_path].append(tag)

        # Do nothing if tag already exists in tag list.
            
    def remove(self, image_file_path: str, tag: str):
        # Remove tag only if file exists in dictionary and if tag exists in tag list.
        if image_file_path in self.tag_dictionary:
            if tag in self.tag_dictionary[image_file_path]:
                self.tag_dictionary[image_file_path].remove(tag)