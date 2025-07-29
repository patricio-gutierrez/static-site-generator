import unittest

from textnode import TextNode, TextType
from split_nodes_link import split_nodes_link

class TestSplitNodesLinks(unittest.TestCase):
    def test_split_links(self):
        """Test basic link splitting functionality"""
        node = TextNode(
            "This is text with a [link](https://www.example.com) and another [second link](https://www.google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.example.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://www.google.com"),
            ],
            new_nodes,
        )

    def test_split_links_no_links(self):
        """Test text node with no links"""
        node = TextNode("This is just plain text with no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_empty_text(self):
        """Test empty text node"""
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_only_link(self):
        """Test text that contains only a link"""
        node = TextNode("[solo link](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("solo link", TextType.LINK, "https://example.com")],
            new_nodes,
        )

    def test_split_links_link_at_start(self):
        """Test link at the beginning of text"""
        node = TextNode("[start link](https://start.com) followed by text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("start link", TextType.LINK, "https://start.com"),
                TextNode(" followed by text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_link_at_end(self):
        """Test link at the end of text"""
        node = TextNode("Text before [end link](https://end.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text before ", TextType.TEXT),
                TextNode("end link", TextType.LINK, "https://end.com"),
            ],
            new_nodes,
        )

    def test_split_links_empty_link_text(self):
        """Test link with empty link text"""
        node = TextNode("Before [](https://example.com) after", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Before ", TextType.TEXT),
                TextNode("", TextType.LINK, "https://example.com"),
                TextNode(" after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_empty_url(self):
        """Test link with empty URL"""
        node = TextNode("Before [link text]() after", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Before ", TextType.TEXT),
                TextNode("link text", TextType.LINK, ""),
                TextNode(" after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_consecutive_links(self):
        """Test consecutive links with no text between them"""
        node = TextNode("[first](https://first.com)[second](https://second.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("first", TextType.LINK, "https://first.com"),
                TextNode("second", TextType.LINK, "https://second.com"),
            ],
            new_nodes,
        )

    def test_split_links_multiple_nodes_input(self):
        """Test with multiple input nodes"""
        nodes = [
            TextNode("First [link1](https://link1.com) node", TextType.TEXT),
            TextNode("Second [link2](https://link2.com) node", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("First ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "https://link1.com"),
                TextNode(" node", TextType.TEXT),
                TextNode("Second ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "https://link2.com"),
                TextNode(" node", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_non_text_nodes_preserved(self):
        """Test that non-TEXT nodes are preserved unchanged"""
        nodes = [
            TextNode("Bold text", TextType.BOLD),
            TextNode("Text with [link](https://example.com)", TextType.TEXT),
            TextNode("Italic text", TextType.ITALIC),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("Bold text", TextType.BOLD),
                TextNode("Text with ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode("Italic text", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_split_links_three_links(self):
        """Test splitting text with three links"""
        node = TextNode(
            "Start [first](https://1.com) middle [second](https://2.com) middle2 [third](https://3.com) end",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("first", TextType.LINK, "https://1.com"),
                TextNode(" middle ", TextType.TEXT),
                TextNode("second", TextType.LINK, "https://2.com"),
                TextNode(" middle2 ", TextType.TEXT),
                TextNode("third", TextType.LINK, "https://3.com"),
                TextNode(" end", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_with_special_chars_in_text(self):
        """Test link with special characters in link text"""
        node = TextNode("[link: test & more!](https://special.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("link: test & more!", TextType.LINK, "https://special.com")],
            new_nodes,
        )

    def test_split_links_empty_list(self):
        """Test with empty list of nodes"""
        new_nodes = split_nodes_link([])
        self.assertListEqual([], new_nodes)

    def test_split_links_with_query_params(self):
        """Test links with query parameters and fragments"""
        node = TextNode(
            "Check [docs](https://example.com/docs?param=value#section) and [search](https://site.com/search?q=test)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Check ", TextType.TEXT),
                TextNode("docs", TextType.LINK, "https://example.com/docs?param=value#section"),
                TextNode(" and ", TextType.TEXT),
                TextNode("search", TextType.LINK, "https://site.com/search?q=test"),
            ],
            new_nodes,
        )

    def test_split_links_mixed_with_images(self):
        """Test text with both links and images (should only process links)"""
        node = TextNode(
            "Here's a [link](https://example.com) and an ![image](photo.jpg) together",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        # Should only split the link, leaving the image syntax as plain text
        self.assertListEqual(
            [
                TextNode("Here's a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" and an ![image](photo.jpg) together", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_relative_and_absolute_paths(self):
        """Test links with various path types"""
        node = TextNode(
            "Links: [local](./docs/readme.md) [absolute](/var/www/index.html) [url](https://site.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Links: ", TextType.TEXT),
                TextNode("local", TextType.LINK, "./docs/readme.md"),
                TextNode(" ", TextType.TEXT),
                TextNode("absolute", TextType.LINK, "/var/www/index.html"),
                TextNode(" ", TextType.TEXT),
                TextNode("url", TextType.LINK, "https://site.com"),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
