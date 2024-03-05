import unittest
from os import remove
from os.path import exists
from tagging import TagHandler

class TestTagging(unittest.TestCase):
    def test_file_creation(self):
        # Prepare variables
        default_tag_file_location = "data/tags.json"
        test_tag_file_location = "tests/tags.json"

        # Perform test
        tag_handler = TagHandler()
        self.assertTrue(exists(default_tag_file_location),
                        "Default file is missing.")
        tag_handler_2 = TagHandler(test_tag_file_location)
        self.assertTrue(exists(test_tag_file_location),
                        "Specific file is missing.")
        
        # Clean up
        remove(test_tag_file_location)

    def test_adding_and_removing_tags(self):
        # Prepare variables
        test_tag_file_location = "tests/tags.json"

        # Perform test
        tag_handler = TagHandler(test_tag_file_location)

        tag_handler.add("test1.png", "Photograph")
        tag_handler.add("test1.png", "Portrait")

        tag_handler.add("test2.png", "Photograph")
        tag_handler.add("test2.png", "Landscape")
        tag_handler.add("test2.png", "Rocks")

        test1_tags = tag_handler.get("test1.png")
        test2_tags = tag_handler.get("test2.png")

        self.assertTrue("Photograph" in test1_tags)
        self.assertTrue("Portrait" in test1_tags)
        self.assertFalse("Rocks" in test1_tags)
        
        self.assertTrue("Photograph" in test2_tags)
        self.assertTrue("Landscape" in test2_tags)
        self.assertTrue("Rocks" in test2_tags)
        self.assertFalse("Portrait" in test2_tags)

        # Clean up
        remove(test_tag_file_location)
        
    def test_existing_file(self):
        # Prepare variables
        test_tag_file_location = "tests/tags.json"
        
        # Perform test
        tag_handler = TagHandler(test_tag_file_location)

        tag_handler.add("test1.png", "Photograph")
        tag_handler.add("test1.png", "Portrait")

        tag_handler.add("test2.png", "Photograph")
        tag_handler.add("test2.png", "Landscape")
        tag_handler.add("test2.png", "Rocks")

        tag_handler.pack()

        tag_handler_2 = TagHandler(test_tag_file_location)

        test1_tags = tag_handler_2.get("test1.png")
        test2_tags = tag_handler_2.get("test2.png")

        self.assertTrue("Photograph" in test1_tags)
        self.assertTrue("Portrait" in test1_tags)
        self.assertFalse("Rocks" in test1_tags)
        
        self.assertTrue("Photograph" in test2_tags)
        self.assertTrue("Landscape" in test2_tags)
        self.assertTrue("Rocks" in test2_tags)
        self.assertFalse("Portrait" in test2_tags)

        # Clean up
        remove(test_tag_file_location)

if __name__ == '__main__':
    unittest.main()
    # TODO: Add Cleanup for file that has been created.