import unittest

from splitters_n_extractors import *
from textnode import TextNode, TextType
from markdown_blocks import *


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
            "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertEqual(len(result), 2)

    def test_extractor_url_2(self):
        result = extract_markdown_links(
            "[rick roll](https://i.imgur.com/aKaOqIh.gif)")
        self.assertEqual(len(result), 1)

    def test_extractor_url_3(self):
        result = extract_markdown_links(
            "!!!![rick roll](https://i.imgur.com/aKaOqIh.gif)!!!")
        self.assertEqual(len(result), 0)

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


class TestBootDevExample_EXTRACT(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

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


class TestExtractorsLinks(unittest.TestCase):
    def test_extractor_links_gen_1(self):

        nodes = [TextNode(
            "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)]
        result = split_nodes_link(nodes)

        self.assertEqual(len(result), 4)

    def test_extractor_links_gen_2(self):
        nodes = [TextNode(
            "This is text with a rickroll and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)]
        result = split_nodes_link(nodes)
        self.assertEqual(len(result), 2)

    def test_extractor_links_gen_3(self):
        nodes = [TextNode(
            "[rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)]
        result = split_nodes_link(nodes)
        self.assertEqual(len(result), 3)

    def test_extractor_links_gen_4(self):
        nodes = [TextNode(
            "[obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)]
        result = split_nodes_link(nodes)
        self.assertEqual(len(result), 1)

    def test_extractor_links_gen_5(self):
        nodes = [TextNode(
            "a [[b[i]t [tricky] text [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)]
        result = split_nodes_link(nodes)
        self.assertEqual(len(result), 2)


class TestExtractorsImages(unittest.TestCase):
    def test_extractor_image_gen_1(self):

        nodes = [TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)]
        result = split_nodes_image(nodes)

        self.assertEqual(len(result), 4)

    def test_extractor_image_gen_2(self):
        nodes = [TextNode(
            "This is text with a rickroll and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)]
        result = split_nodes_image(nodes)
        self.assertEqual(len(result), 2)

    def test_extractor_image_gen_3(self):
        nodes = [TextNode(
            "![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)]
        result = split_nodes_image(nodes)
        self.assertEqual(len(result), 3)

    def test_extractor_image_gen_4(self):
        nodes = [TextNode(
            "![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)]
        result = split_nodes_image(nodes)
        self.assertEqual(len(result), 1)

    def test_extractor_image_gen_5(self):
        nodes = [TextNode(
            "a [[b[i]t [tricky] text ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)]
        result = split_nodes_image(nodes)
        self.assertEqual(len(result), 2)

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE,
                         "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )


class BootDevExmplSplitters(unittest.TestCase):
    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE,
                         "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )


class TestConvertingRawTextToMarkdown(unittest.TestCase):
    def test_conversion(self):
        stringToTest = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        converted = text_to_textnodes(stringToTest)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE,
                         "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev")
            ],
            converted,
        )

    def test_conversion_2(self):
        stringToTest = "**text** with an *italic* word and a [link](https://boot.dev)"
        converted = text_to_textnodes(stringToTest)
        self.assertListEqual(
            [
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev")
            ],
            converted,
        )

    def test_conversion_3(self):
        stringToTest = "[link](https://boot.dev)"
        converted = text_to_textnodes(stringToTest)
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://boot.dev")
            ],
            converted,
        )

    def test_conversion_4(self):
        stringToTest = "[link](https://boot.dev)[link](https://boot.dev)[link](https://boot.dev)[link](https://boot.dev)"
        converted = text_to_textnodes(stringToTest)
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            converted,
        )


class TestBlockSeperator(unittest.TestCase):
    def test_block_separator(self):
        test_str = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        correct = ['# This is a heading', 'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
                   '* This is the first list item in a list block\n* This is a list item\n* This is another list item']
        result = markdown_to_blocks(test_str)
        self.assertListEqual(result, correct)

    def test_block_separator_2(self):
        test_str = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it."""
        correct = ['# This is a heading',
                   'This is a paragraph of text. It has some **bold** and *italic* words inside of it.']
        result = markdown_to_blocks(test_str)
        self.assertListEqual(result, correct)

    def test_block_separator_3(self):
        test_str = """# This is a heading"""
        correct = ['# This is a heading']
        result = markdown_to_blocks(test_str)
        self.assertListEqual(result, correct)

    def test_block_separator_4(self):
        test_str = """"""
        correct = []
        result = markdown_to_blocks(test_str)
        self.assertListEqual(result, correct)


if __name__ == "__main__":
    unittest.main()
