import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container", "id": "main"})
        self.assertEqual(parent_node.to_html(), '<div class="container" id="main"><span>child</span></div>')

    def test_to_html_error_cases(self):
        child_node = LeafNode("span", "child")

        # Test no tag error
        parent_node_no_tag = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node_no_tag.to_html()

        # Test no children error
        parent_node_no_children = ParentNode("div", [])
        with self.assertRaises(ValueError):
            parent_node_no_children.to_html()

    def test_to_html_with_multiple_children(self):
        child1 = LeafNode("span", "First child")
        child2 = LeafNode("p", "Second child")
        child3 = LeafNode("b", "Third child")
        parent_node = ParentNode("div", [child1, child2, child3])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>First child</span><p>Second child</p><b>Third child</b></div>"
        )

if __name__ == "__main__":
    unittest.main()
