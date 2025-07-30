import unittest

from block_to_block_type import block_to_block_type
from block_type import BlockType

class TestBlockToBlockType(unittest.TestCase):
    def test_block_types_basic_functionality(self):
        """Test all basic block types are correctly identified"""
        # Heading
        self.assertEqual(block_to_block_type("# This is a heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## This is a heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### This is a heading"), BlockType.HEADING)

        # Code block
        self.assertEqual(block_to_block_type("```\ncode here\n```"), BlockType.CODE)

        # Simple cases
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("- This is a list item"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("1. This is an ordered item"), BlockType.ORDERED_LIST)

        # Paragraph (default)
        self.assertEqual(block_to_block_type("This is just a paragraph"), BlockType.PARAGRAPH)

    def test_quote_blocks_require_all_lines(self):
        """Test that quote blocks require ALL lines to start with >"""
        # Valid quote block - all lines start with >
        valid_quote = "> Line 1\n> Line 2\n> Line 3"
        self.assertEqual(block_to_block_type(valid_quote), BlockType.QUOTE)

        # Invalid quote block - not all lines start with >
        invalid_quote = "> Line 1\nLine 2\n> Line 3"
        self.assertEqual(block_to_block_type(invalid_quote), BlockType.PARAGRAPH)

    def test_unordered_list_requires_all_lines(self):
        """Test that unordered lists require ALL lines to start with '- '"""
        # Valid unordered list - all lines start with "- "
        valid_list = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(valid_list), BlockType.UNORDERED_LIST)

        # Invalid unordered list - not all lines start with "- "
        invalid_list = "- Item 1\nItem 2\n- Item 3"
        self.assertEqual(block_to_block_type(invalid_list), BlockType.PARAGRAPH)

    def test_ordered_list_strict_incrementing(self):
        """Test that ordered lists require strict incrementing from 1"""
        # Valid ordered list - strict incrementing from 1
        valid_ordered = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(valid_ordered), BlockType.ORDERED_LIST)

        # Single item ordered list
        single_item = "1. Only item"
        self.assertEqual(block_to_block_type(single_item), BlockType.ORDERED_LIST)

        # Invalid - doesn't start at 1
        wrong_start = "5. First item\n6. Second item\n7. Third item"
        self.assertEqual(block_to_block_type(wrong_start), BlockType.PARAGRAPH)

        # Invalid - skipped number
        skipped_number = "1. First item\n3. Second item\n4. Third item"
        self.assertEqual(block_to_block_type(skipped_number), BlockType.PARAGRAPH)

        # Invalid - wrong order
        wrong_order = "1. First item\n3. Second item\n2. Third item"
        self.assertEqual(block_to_block_type(wrong_order), BlockType.PARAGRAPH)

    def test_edge_cases_and_paragraph_fallback(self):
        """Test edge cases and paragraph fallback behavior"""
        # Heading must have space after #
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)

        # Too many # for heading
        self.assertEqual(block_to_block_type("####### Too many"), BlockType.PARAGRAPH)

        # Code block must start AND end with ```
        self.assertEqual(block_to_block_type("```code but no end"), BlockType.PARAGRAPH)

        # Mixed content defaults to paragraph
        mixed_content = "Some text\n> Quote line\n- List item"
        self.assertEqual(block_to_block_type(mixed_content), BlockType.PARAGRAPH)

        # Empty string
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
