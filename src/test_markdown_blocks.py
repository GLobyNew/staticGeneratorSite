import unittest
from markdown_blocks import markdown_to_html_node

from htmlnode import HTMLNode, ParentNode, LeafNode


class TestTextNode(unittest.TestCase):
    def test_markdown_to_html_node_1(self):
        test_str = """Just some text with **bold** and *italic* markdowns"""
        res = markdown_to_html_node(test_str).to_html()
        self.assertEqual(
            res, "<div><p>Just some text with <b>bold</b> and <i>italic</i> markdowns</p></div>")

    def test_markdown_to_html_node_2(self):
        test_str = """# Just some text with `code` and *italic* markdowns"""
        res = markdown_to_html_node(test_str).to_html()
        self.assertEqual(
            res, "<div><h1>Just some text with <code>code</code> and <i>italic</i> markdowns</h1></div>")

    def test_markdown_to_html_node_3(self):
        test_str = """# This is big opportunity

But also there is a list:

1. One
2. Two
3. Three

```Maybe even **some** code?```

Jeez I will order a *pizza* if it's working!"""
        should_be = "<div><h1>This is big opportunity</h1><p>But also there is a list:</p><ol><li>One</li><li>Two</li><li>Three</li></ol><pre><code>Maybe even <b>some</b> code?</code></pre><p>Jeez I will order a <i>pizza</i> if it's working!</p></div>"
        res = markdown_to_html_node(test_str).to_html()
        print(res)
        self.assertEqual(res, should_be)


if __name__ == "__main__":
    unittest.main()
