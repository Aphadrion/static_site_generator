import unittest
from textnode import TextNode, TextType
from inlinemarkdown import *

class TestInline(unittest.TestCase):

    def test_simple_text(self):
        node = TextNode("Hello world", TextType.NORMAL)
        result = split_nodes_delimiter([node], "", TextType.NORMAL)
        assert len(result) == 1
        assert result[0].text == "Hello world"
        assert result[0].text_type == TextType.NORMAL

    def test_basic_delimiter(self):
        node = TextNode("Hello `world`", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("Hello ", TextType.NORMAL),
                TextNode("world", TextType.CODE),
            ],
            new_nodes,
        )

    def test_multiple_delimiters(self):
        node = TextNode("Hello `world` and **universe**", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("Hello ", TextType.NORMAL),
                TextNode("world", TextType.CODE),
                TextNode(" and ", TextType.NORMAL),
                TextNode("universe", TextType.BOLD),
            ],
            new_nodes,
        )

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

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
    )
    
    def test_text_to_textnodes(self):
        #node = TextNode("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",TextType.NORMAL)
        matches = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
            
        )
        self.assertListEqual([
    TextNode("This is ", TextType.NORMAL),
    TextNode("text", TextType.BOLD),
    TextNode(" with an ", TextType.NORMAL),
    TextNode("italic", TextType.ITALIC),
    TextNode(" word and a ", TextType.NORMAL),
    TextNode("code block", TextType.CODE),
    TextNode(" and an ", TextType.NORMAL),
    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
    TextNode(" and a ", TextType.NORMAL),
    TextNode("link", TextType.LINK, "https://boot.dev"),
], matches)
        

if __name__ == "__main__":
    unittest.main()