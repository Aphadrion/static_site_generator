import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_attributes(self):
        print(self)

    def test_print(self):
        node1 = HTMLNode("p", "It happened in 1789", None, None)
        node = HTMLNode("h1", "The french revolution", node1, None) 
        #print(node)
    
    def test_multiple_children(self):
        node1 = HTMLNode("p", "It happened in 1789", None)
        node2 = HTMLNode("p", "That's all I know about it", None)
        node = HTMLNode("h1", "The french revolution", (node1, node2), None)
        print(node)

    def test_leaf(self):
        leafnode = LeafNode("p","this is another paragraph")
        print(leafnode.to_html()) 

    def test_leaf_props(self):
        leafnode = LeafNode("a","this is clickable", {"href": "https://www.google.com"})
        print(leafnode.to_html()) 

    def test_parent_multiple_children(self):
        node1 = ParentNode("p", None, None)
        node2 = ParentNode("p", None, None)
        node = ParentNode("h1", None, (node1, node2))
        print(node)

    def test_parents_nested(self):
        node1 = ParentNode("p", None, None)
        node2 = ParentNode("a", None, node1)
        node = ParentNode("h1", None, (node2))
        print(node)

    def test_parent_example(self):
        node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "More text"),
        ],
        )

        print(node.to_html())

if __name__ == "__main__":
    unittest.main()