import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_link(self):
        node = LeafNode("a", "This is a link", {"href": "https://boot.dev"})
        self.assertEqual(node.to_html(), '<a href="https://boot.dev">This is a link</a>')

    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", "")
        with self.assertRaises(ValueError):
            self.assertEqual(node.to_html(), "All leaf nodes must have a value")

if __name__ == "__main__":
    unittest.main()
