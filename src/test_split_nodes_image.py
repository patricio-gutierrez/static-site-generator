import unittest

from textnode import TextNode, TextType
from split_nodes_image import split_nodes_image

class TestSplitNodesImages(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_no_images(self):
        """Test text node with no images"""
        node = TextNode("This is just plain text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_images_empty_text(self):
        """Test empty text node"""
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_images_only_image(self):
        """Test text that contains only an image"""
        node = TextNode("![solo image](https://example.com/image.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("solo image", TextType.IMAGE, "https://example.com/image.png")],
            new_nodes,
        )

    def test_split_images_image_at_start(self):
        """Test image at the beginning of text"""
        node = TextNode("![start image](image.png) followed by text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("start image", TextType.IMAGE, "image.png"),
                TextNode(" followed by text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_image_at_end(self):
        """Test image at the end of text"""
        node = TextNode("Text before ![end image](final.jpg)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text before ", TextType.TEXT),
                TextNode("end image", TextType.IMAGE, "final.jpg"),
            ],
            new_nodes,
        )

    def test_split_images_empty_alt_text(self):
        """Test image with empty alt text"""
        node = TextNode("Before ![](image.png) after", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Before ", TextType.TEXT),
                TextNode("", TextType.IMAGE, "image.png"),
                TextNode(" after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_empty_url(self):
        """Test image with empty URL"""
        node = TextNode("Before ![alt text]() after", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Before ", TextType.TEXT),
                TextNode("alt text", TextType.IMAGE, ""),
                TextNode(" after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_consecutive_images(self):
        """Test consecutive images with no text between them"""
        node = TextNode("![first](img1.png)![second](img2.jpg)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("first", TextType.IMAGE, "img1.png"),
                TextNode("second", TextType.IMAGE, "img2.jpg"),
            ],
            new_nodes,
        )

    def test_split_images_multiple_nodes_input(self):
        """Test with multiple input nodes"""
        nodes = [
            TextNode("First ![image1](img1.png) node", TextType.TEXT),
            TextNode("Second ![image2](img2.jpg) node", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("First ", TextType.TEXT),
                TextNode("image1", TextType.IMAGE, "img1.png"),
                TextNode(" node", TextType.TEXT),
                TextNode("Second ", TextType.TEXT),
                TextNode("image2", TextType.IMAGE, "img2.jpg"),
                TextNode(" node", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_non_text_nodes_preserved(self):
        """Test that non-TEXT nodes are preserved unchanged"""
        nodes = [
            TextNode("Bold text", TextType.BOLD),
            TextNode("Text with ![image](img.png)", TextType.TEXT),
            TextNode("Italic text", TextType.ITALIC),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("Bold text", TextType.BOLD),
                TextNode("Text with ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "img.png"),
                TextNode("Italic text", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_split_images_three_images(self):
        """Test splitting text with three images"""
        node = TextNode(
            "Start ![first](1.png) middle ![second](2.jpg) middle2 ![third](3.gif) end",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("first", TextType.IMAGE, "1.png"),
                TextNode(" middle ", TextType.TEXT),
                TextNode("second", TextType.IMAGE, "2.jpg"),
                TextNode(" middle2 ", TextType.TEXT),
                TextNode("third", TextType.IMAGE, "3.gif"),
                TextNode(" end", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_with_special_chars_in_alt(self):
        """Test image with special characters in alt text"""
        node = TextNode("![image: test & more!](special.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("image: test & more!", TextType.IMAGE, "special.png")],
            new_nodes,
        )

    def test_split_images_empty_list(self):
        """Test with empty list of nodes"""
        new_nodes = split_nodes_image([])
        self.assertListEqual([], new_nodes)
