import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://tinyelfarcanist.com")
        node2 = TextNode("This is a text node", TextType.NORMAL)
        self.assertNotEqual(node,node2)

    def test_url_none(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_dif_text_type(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        node2 = TextNode("This is an italic text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

class TestTextNodeToHTMLNode(unittest.TestCase):

    def test_to_html_normal(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        text_node_to_html_node(node)

    def test_to_html_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        text_node_to_html_node(node)
    
    def test_to_html_link(self):
        node = TextNode("This is a link text node", TextType.LINK, "https://tinyelfarcanist.com")
        text_node_to_html_node(node)

    def test_to_html_image(self):
        node = TextNode("This is bad alt text", TextType.IMAGE, "https://images.app.goo.gl/1p8FT4XxiRTeeXdP8")
        text_node_to_html_node(node)

    def test_to_html_error(self):
        node = TextNode("This is a bold text node", None)
        with self.assertRaises(Exception):
            text_node_to_html_node(node)


if __name__ == "__main__":
    unittest.main()