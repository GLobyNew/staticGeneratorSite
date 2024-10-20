from textnode import *
from htmlnode import *





def main():
    TestNode = TextNode("Bruh", TextType.BOLD, "google.com")
    toHtml = TestNode.text_node_to_html_node()
    print(toHtml.to_html())


if __name__ == "__main__":
    main()
