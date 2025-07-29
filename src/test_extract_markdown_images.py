import unittest
from extract_markdown_images import extract_markdown_images


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_images(self):
        matches = extract_markdown_images(
            "Here are two images: ![first](image1.png) and ![second](image2.jpg)"
        )
        self.assertListEqual([("first", "image1.png"), ("second", "image2.jpg")], matches)

    def test_extract_images_empty_alt_text(self):
        matches = extract_markdown_images(
            "Image with empty alt text: ![](https://example.com/image.png)"
        )
        self.assertListEqual([("", "https://example.com/image.png")], matches)

    def test_extract_images_empty_url(self):
        matches = extract_markdown_images(
            "Image with empty URL: ![alt text]()"
        )
        self.assertListEqual([("alt text", "")], matches)

    def test_extract_images_no_images(self):
        matches = extract_markdown_images(
            "This text has no images at all, just regular text."
        )
        self.assertListEqual([], matches)

    def test_extract_images_with_spaces_in_alt_text(self):
        matches = extract_markdown_images(
            "Image with spaces: ![image with spaces](test.png)"
        )
        self.assertListEqual([("image with spaces", "test.png")], matches)

    def test_extract_images_with_special_characters(self):
        matches = extract_markdown_images(
            "Special chars: ![image: description & more!](path/to/image-file_01.png)"
        )
        self.assertListEqual([("image: description & more!", "path/to/image-file_01.png")], matches)

    def test_extract_images_mixed_with_links(self):
        matches = extract_markdown_images(
            "Here's a [link](http://example.com) and an ![image](photo.jpg) together"
        )
        self.assertListEqual([("image", "photo.jpg")], matches)

    def test_extract_images_malformed_syntax(self):
        # Test cases that shouldn't match
        matches = extract_markdown_images(
            "These won't match: [not an image](test.png) !image](missing-bracket.png) ![incomplete"
        )
        self.assertListEqual([], matches)

    def test_extract_images_nested_brackets(self):
        # Test with brackets in alt text or URL (shouldn't match due to regex)
        matches = extract_markdown_images(
            "Complex: ![alt [with] brackets](url) ![normal](test.png)"
        )
        # The regex won't match the first one due to nested brackets, only the second
        self.assertListEqual([("normal", "test.png")], matches)

    def test_extract_images_relative_and_absolute_paths(self):
        matches = extract_markdown_images(
            "Paths: ![local](./images/local.png) ![absolute](/var/www/absolute.jpg) ![url](https://site.com/remote.gif)"
        )
        expected = [
            ("local", "./images/local.png"),
            ("absolute", "/var/www/absolute.jpg"),
            ("url", "https://site.com/remote.gif")
        ]
        self.assertListEqual(expected, matches)

    def test_extract_images_multiline_text(self):
        text = """This is a multiline string
        with an ![image1](first.png) on one line
        and another ![image2](second.jpg) on another line."""
        matches = extract_markdown_images(text)
        self.assertListEqual([("image1", "first.png"), ("image2", "second.jpg")], matches)

    def test_extract_images_empty_string(self):
        matches = extract_markdown_images("")
        self.assertListEqual([], matches)


if __name__ == "__main__":
    unittest.main()
