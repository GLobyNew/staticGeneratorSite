import unittest

from extractors import *


class TestImagesExtractor(unittest.TestCase):
    def test_extractor_img_1(self):
        result = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertEqual(len(result), 2)

    def test_extractor_img_2(self):
        result = extract_markdown_images(
            "![rick roll](https://i.imgur.com/aKaOqIh.gif)")
        self.assertEqual(len(result), 1)

    def test_extractor_img_3(self):
        result = extract_markdown_images(
            "!!!![rick roll](https://i.imgur.com/aKaOqIh.gif)!!!")
        self.assertEqual(len(result), 1)

    def test_extractor_img_4(self):
        result = extract_markdown_images(
            "[rick roll](https://i.imgur.com/aKaOqIh.gif)!!!")
        self.assertEqual(len(result), 0)

    def test_extractor_img_5(self):
        result = extract_markdown_images("")
        self.assertEqual(len(result), 0)

    def test_extractor_img_6(self):
        result = extract_markdown_images(
            "[rick roll](https://i.imgur.com/aKaOqIh.gif)")
        self.assertEqual(len(result), 0)


class TestURLExtractor(unittest.TestCase):
    def test_extractor_url_1(self):
        result = extract_markdown_links(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertEqual(len(result), 2)

    def test_extractor_url_2(self):
        result = extract_markdown_links(
            "![rick roll](https://i.imgur.com/aKaOqIh.gif)")
        self.assertEqual(len(result), 1)

    def test_extractor_url_3(self):
        result = extract_markdown_links(
            "!!!![rick roll](https://i.imgur.com/aKaOqIh.gif)!!!")
        self.assertEqual(len(result), 1)

    def test_extractor_url_4(self):
        result = extract_markdown_links(
            "[rick roll](https://i.imgur.com/aKaOqIh.gif)!!!")
        self.assertEqual(len(result), 1)

    def test_extractor_url_5(self):
        result = extract_markdown_links("")
        self.assertEqual(len(result), 0)

    def test_extractor_url_6(self):
        result = extract_markdown_links(
            "[rick roll](https://i.imgur.com/aKaOqIh.gif)")
        self.assertEqual(len(result), 1)


class TestBootDevExample(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )


if __name__ == "__main__":
    unittest.main()
