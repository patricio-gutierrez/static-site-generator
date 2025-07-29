import unittest

from markdown_to_blocks import markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
            md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\n    This is the same paragraph on a new line",
                    "- This is a list\n    - with items",
                ],
            )

    def test_markdown_to_blocks_empty_input(self):
        """Test with empty string and whitespace-only input"""
        blocks = markdown_to_blocks("")
        self.assertEqual(blocks, [])

        blocks = markdown_to_blocks("   \n\n   \n\n   ")
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_single_block(self):
        """Test with single block (no double newlines)"""
        md = "This is a single paragraph with no separators"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single paragraph with no separators"])

    def test_markdown_to_blocks_multiple_empty_lines(self):
        """Test with multiple consecutive empty lines between blocks"""
        md = """First block




Second block



Third block"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First block",
                "Second block",
                "Third block",
            ]
        )

if __name__ == '__main__':
    unittest.main()
