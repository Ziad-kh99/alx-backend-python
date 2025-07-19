#!/usr/bin/env python3
import unittest
import utils
from parameterized import parameterized

class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b"),
    ])

    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(utils.access_nested_map(nested_map, path), expected)

    def test_access_nested_map_exception(self, nested_map, path, expected_key):
        with self.assertRaises(KeyError) as cm:
            utils.access_nested_map(nested_map, path)

        self.assertEqual(str(cm.exception), f"'{expected_key}'")
