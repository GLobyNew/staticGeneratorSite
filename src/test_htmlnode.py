import unittest

from htmlnode import HTMLNode, ParentNode, LeafNode


class TestTextNode(unittest.TestCase):
    def test_to_html(self):
        html_obj = HTMLNode("p", "Test value", None, {
                            "href": "https://www.google.com", "target": "_blank", })
        html_str = html_obj.props_to_html()
        self.assertIsInstance(html_str, str)

    def test_to_html_with_child(self):
        html_obj_child = HTMLNode("p", "Test value", None, {
                                  "href": "https://www.google.com", "target": "_blank", })
        html_obj = HTMLNode("span", "", html_obj_child, {
                            "href": "https://www.google.com", "target": "_blank", "img": "https://youtube.com"})
        html_str = html_obj.props_to_html()
        self.assertIsInstance(html_str, str)

    def test_to_html_with_child_nones(self):
        html_obj_child = HTMLNode("p")
        html_obj = HTMLNode(None, None, html_obj_child, {
                            "href": "https://www.google.com", "target": "_blank", "img": "https://youtube.com"})
        html_str = html_obj.props_to_html()
        self.assertIsInstance(html_str, str)

    def test_to_html_with_child_nones(self):
        html_obj = HTMLNode()
        html_str = html_obj.props_to_html()
        self.assertIsInstance(html_str, str)


class TestLeafNode(unittest.TestCase):
    def test_leaf(self):
        leaf_obj = LeafNode("p", "This is a paragraph of text.")
        leaf_str = leaf_obj.to_html()
        self.assertEqual(leaf_str, "<p>This is a paragraph of text.</p>")

    def test_leaf_with_props(self):
        leaf_obj = LeafNode("a", "Click me!", {
                            "href": "https://www.google.com"})
        leaf_str = leaf_obj.to_html()
        self.assertEqual(
            leaf_str, "<a href=\"https://www.google.com\">Click me!</a>")

    def test_leaf_with_mult_props(self):
        leaf_obj = LeafNode("a", "Click me!", {
                            "href": "https://www.google.com", "alt": "sheesh"})
        leaf_str = leaf_obj.to_html()
        self.assertEqual(
            leaf_str, "<a href=\"https://www.google.com\" alt=\"sheesh\">Click me!</a>")

    def test_to_html_no_children(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")


class TestParentNode(unittest.TestCase):
    def test_parent(self):
        node = ParentNode("div", [
            LeafNode("p", "Hello"),
            ParentNode("ul", [
                LeafNode("li", "Item 1"),
                LeafNode("li", "Item 2")
            ]),
            LeafNode("p", "Goodbye")
        ])
        self.assertEqual(node.to_html(
        ), "<div><p>Hello</p><ul><li>Item 1</li><li>Item 2</li></ul><p>Goodbye</p></div>")

    def test_parent_double_li(self):
        node = ParentNode("div", [
            LeafNode("p", "Hello"),
            ParentNode("ul", [
                LeafNode("li", "Item 1"),
                LeafNode("li", "Item 2")
            ]),
            ParentNode("ul", [
                LeafNode("li", "Item 1"),
                LeafNode("li", "Item 2")
            ]),
            LeafNode("p", "Goodbye")
        ])
        self.assertEqual(node.to_html(
        ), "<div><p>Hello</p><ul><li>Item 1</li><li>Item 2</li></ul><ul><li>Item 1</li><li>Item 2</li></ul><p>Goodbye</p></div>")

    def test_parent_with_NoneValues(self):
        with self.assertRaises(ValueError):
            node = ParentNode("div", [
                LeafNode("p", "Hello"),
                ParentNode("ul", [
                    LeafNode(None, None),
                    LeafNode(None, "Item 2")
                ]),
                LeafNode("p", "Goodbye")
            ])
            node.to_html()

    def test_parent_with_NoneValues_2(self):
        with self.assertRaises(ValueError):
            node = ParentNode(None, [
                LeafNode("p", "Hello"),
                ParentNode("ul", [
                    LeafNode("li", "Item 1"),
                    LeafNode("li", "Item 2")
                ]),
                LeafNode("p", "Goodbye")
            ])
            node.to_html()

    def test_parent_with_NoneValues_3(self):
        with self.assertRaises(ValueError):
            node = ParentNode("div", None)
            node.to_html()


if __name__ == "__main__":
    unittest.main()
