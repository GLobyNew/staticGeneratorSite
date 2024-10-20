import unittest

from textnode import TextNode, TextType
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

        node_first_1 = TextNode("This is a text node", TextType.ITALIC)
        node_other_1 = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(node_first_1, node_other_1)

        node_first_2 = TextNode("This is a text1 node", TextType.IMAGE)
        node_other_2 = TextNode("This is a text1 node", TextType.IMAGE)
        self.assertEqual(node_first_2, node_other_2)

    def test_edge_cases(self):
        node_first_1 = TextNode("This is a text node", TextType.ITALIC, None)
        node_other_1 = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(node_first_1, node_other_1)

        node_first_2 = TextNode("This is a text1 node", TextType.CODE)
        node_other_2 = TextNode("This is a text1 node", TextType.CODE)
        self.assertEqual(node_first_2, node_other_2)

        node_first_3 = TextNode('', TextType.TEXT, None)
        node_other_3 = TextNode("", TextType.TEXT)
        self.assertEqual(node_first_3, node_other_3)


class Test_text_node_to_html_node(unittest.TestCase):
    def test_text_node_to_html_node_b(self):
        TestNode = TextNode("Bruh", TextType.BOLD, "google.com")
        toHtml = TestNode.text_node_to_html_node()
        self.assertEqual(toHtml.to_html(), "<b>Bruh</b>")

    def test_text_node_to_html_node_normal(self):
        TestNode = TextNode("Bruh", TextType.TEXT, "google.com")
        toHtml = TestNode.text_node_to_html_node()
        self.assertEqual(toHtml.to_html(), "Bruh")

    def test_text_node_to_html_node_error(self):
        with self.assertRaises(Exception):
            TestNode = TextNode("Bruh", TextType.USR, "google.com")

    def test_text_node_to_html_node_image(self):
        TestNode = TextNode("Cat Chuba", TextType.IMAGE,
                            "https://kappa.lol/0NdrF")
        toHtml = TestNode.text_node_to_html_node()
        self.assertEqual(toHtml.to_html(
        ), "<img src=\"https://kappa.lol/0NdrF\" alt=\"Cat Chuba\"></img>")

    def test_text_node_to_html_node_none(self):
        with self.assertRaises(Exception):
            TestNode = TextNode(None, None, None)


if __name__ == "__main__":
    unittest.main()
