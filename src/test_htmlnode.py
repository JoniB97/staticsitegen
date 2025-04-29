import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    def test_repr(self):
        node = HTMLNode("a", "Click here", [], {"href": "https://www.google.com", "target": "_blank"})
        expected = 'HTMLNode(tag="a", value="Click here", children=None, props=" href=\"https://www.google.com\" target=\"_blank\"")'
        self.assertEqual(repr(node), expected)

    def test_eq_true(self):
        node1 = HTMLNode("p", "Hello", [], {"class": "text"})
        node2 = HTMLNode("p", "Hello", [], {"class": "text"})
        self.assertEqual(node1, node2)

    def test_eq_false(self):
        node1 = HTMLNode("p", "Hello", [], {"class": "text"})
        node2 = HTMLNode("div", "Hello", [], {"class": "text"})
        self.assertNotEqual(node1, node2)

    def test_to_html_raises(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

if __name__ == "__main__":
    unittest.main()
