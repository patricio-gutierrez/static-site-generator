import unittest

from textnode import TextNode, TextType
from text_to_textnodes import text_to_textnodes

class TestTextToTextnodes(unittest.TestCase):
    def test_text_to_textnodes_basic_formatting(self):
        """Test basic text formatting with bold, italic, and code"""
        text = "This is **bold** and _italic_ and `code` text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(expected, result)

    def test_text_to_textnodes_images_and_links(self):
        """Test text with images and links"""
        text = "Check out this [link](https://example.com) and this ![image](photo.jpg)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("Check out this ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" and this ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "photo.jpg"),
        ]
        self.assertListEqual(expected, result)

    def test_text_to_textnodes_plain_text(self):
        """Test plain text with no formatting"""
        text = "This is just plain text with no special formatting"
        result = text_to_textnodes(text)
        expected = [TextNode("This is just plain text with no special formatting", TextType.TEXT)]
        self.assertListEqual(expected, result)

    def test_text_to_textnodes_nested_formatting(self):
        """Test text with overlapping formatting elements"""
        text = "**Bold text** and _italic text_ and `code text`"
        result = text_to_textnodes(text)
        expected = [
            TextNode("Bold text", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code text", TextType.CODE),
        ]
        self.assertListEqual(expected, result)

    def test_text_to_textnodes_everything_mixed(self):
        """Test complex text with all formatting types combined"""
        text = "**Bold** text with _italic_ and `code` plus [link](https://test.com) and ![img](pic.png)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("Bold", TextType.BOLD),
            TextNode(" text with ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" plus ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://test.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "pic.png"),
        ]
        self.assertListEqual(expected, result)


if __name__ == "__main__":
    unittest.main()
