#!/usr/bin/env python3
"""
Unit test cases for nodict.py
Students should not modify this file.
"""

__author__ = "madarp"

import sys
import unittest
import importlib
import inspect

# suppress __pycache__ and .pyc files
sys.dont_write_bytecode = True

# Ensure python 3+
assert sys.version_info[0] >= 3

# curriculum devs: change this to 'soln.nodict' to test solution
PKG_NAME = 'nodict'

# alias for module under test
nodict = None
classes = None
funcs = None


def import_helper(pkg_name):
    """Attempts to import the pkg at runtime"""
    module = importlib.import_module(pkg_name)
    # make a dictionary of each function in the test module
    classes = {
        k: v for k, v in inspect.getmembers(
            module, inspect.isclass
            )
        }
    funcs = {
        k: v for k, v in inspect.getmembers(
            module, inspect.isfunction
            )
        }
    return module, classes, funcs


class TestNode(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Performs module import and suite setup at test-runtime"""
        global nodict
        nodict, classes, funcs = import_helper(PKG_NAME)
        cls.assertIn(
            cls, "Node", classes,
            "Missing required class: Node"
            )

    def test_node_instance(self):
        """Check if we can create an instance"""
        nd = nodict.Node("Kevin")
        self.assertIsNotNone(nd, "Unable to create a Node instance")

    def test_comparison_eq(self):
        """Check if comparisons work"""
        wallace = nodict.Node("Wallace")
        grommit = nodict.Node("Grommit")
        other_wallace = nodict.Node("Wallace")
        self.assertNotEqual(wallace, grommit)
        self.assertEqual(wallace, other_wallace)

    def test_repr(self):
        """Check if the __repr__ method is correct"""
        melvin = nodict.Node("Melvin")
        self.assertEqual(
            repr(melvin), "Node(Melvin, None)"
        )


class TestNoDict(unittest.TestCase):
    """Main test fixture for nodict module"""
    @classmethod
    def setUpClass(cls):
        """Performs module import and suite setup at test-runtime"""
        global nodict
        nodict, classes, funcs = import_helper(PKG_NAME)
        cls.assertIn(
            cls, "NoDict", classes,
            "Missing required class: NoDict"
            )

    def test_instance(self):
        """Check if we can create an instance"""
        nd = nodict.NoDict()
        self.assertIsNotNone(nd, "Unable to create a NoDict instance")

    def test_default_buckets(self):
        """Check if NoDict creates 10 buckets by default"""
        d = nodict.NoDict()
        self.assertIsInstance(
            d.buckets, list,
            "The buckets should be a list of lists"
            )
        self.assertEqual(
            len(d.buckets), 10,
            "There should be 10 buckets created by default"
            )

    def test_more_buckets(self):
        """Check if NoDict creates other bucket sizes"""
        d = nodict.NoDict(512)
        self.assertEqual(
            len(d.buckets), 512,
            "There should be 512 buckets created."
            )

    def test_repr(self):
        """Check if the __repr__ method is correct"""
        d = nodict.NoDict(1)  # create a NoDict with just 1 bucket
        self.assertEqual(repr(d), "NoDict.0:[]")

    def test_add(self):
        """Checks the NoDict.add() method"""
        d = nodict.NoDict(1)
        d.add("Ralphie", "BB gun")
        expected_node = nodict.Node("Ralphie", "BB gun")
        actual_node = d.buckets[0][0]
        self.assertEqual(actual_node, expected_node)

    def test_get(self):
        d = nodict.NoDict()
        d.add("Groucho", 50)
        self.assertEqual(d.get("Groucho"), 50)

    def test_key_error(self):
        """Checks if KeyError is raised"""
        d = nodict.NoDict()
        with self.assertRaises(KeyError):
            d.get("Kevin")

    def test_getitem(self):
        """Checks if __getitem__ is implemented"""
        d = nodict.NoDict()
        d.add("Harpo", 52)
        self.assertEqual(d["Harpo"], 52)

    def test_setitem(self):
        """Checks if __setitem__ is implemented"""
        d = nodict.NoDict()
        d["Harpo"] = 52
        self.assertEqual(d.get("Harpo"), 52)

    def test_no_duplicates(self):
        """Check that duplicates are not allowed"""
        # New Node of same name: new value should overwrite previous value
        d = nodict.NoDict()
        d.add("Zeppo", 54)
        self.assertEqual(d.get("Zeppo"), 54)
        d.add("Zeppo", 56)
        self.assertEqual(d.get("Zeppo"), 56)

    def test_doc_strings(self):
        """Checking for docstrings on all methods"""
        d = nodict.NoDict()
        for name, func in inspect.getmembers(d, inspect.ismethod):
            self.assertIsNotNone(
                func.__doc__,
                f"Please add a docstring in the {name} method"
            )


if __name__ == '__main__':
    unittest.main()
