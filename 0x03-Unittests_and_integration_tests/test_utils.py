#!/usr/bin/env python3

"""
module test
"""

import unittest
from unittest.mock import patch


from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """
    test a access_nested_map function
    """

    @parameterized.expand(
        [
            ({"a": 1}, ("a",), 1),
            ({"a": {"b": 2}}, ("a",), {"b": 2}),
            ({"a": {"b": 2}}, ("a", "b"), 2),
        ]
    )
    def test_access_nested_map(self, nested_map, path, expected):
        """
        assert_equal(access_nested_map(nested_map, path), expected)
        """

        res = access_nested_map(nested_map, path)
        self.assertEqual(res, expected)

    @parameterized.expand(
        [
            ({}, ("a",), "a"),
            ({"a": 1}, ("a", "b"), "b"),
        ]
    )
    def test_access_nested_map_exception(self, nested_map, path, expected):
        """
        except a KeyError is raised
        """

        with self.assertRaises(KeyError) as error:
            access_nested_map(nested_map, path)
        self.assertEqual(error.exception.args[0], expected)


class TestGetJson(unittest.TestCase):
    """
    test class for get_json func

    """

    @parameterized.expand(
        [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]
    )
    def test_get_json(self, url, expected):
        """
        mock requests.get and return expected result
        """

        with patch("requests.get") as req_patch:
            req_patch.return_value.json.return_value = expected
            self.assertEqual(get_json(url), expected)

        req_patch.assert_called_once_with(url)


class TestMemoize(unittest.TestCase):
    """
    test memoize decorators func
    """

    class TestClass:
        def a_method(self):
            return 42

        @memoize
        def a_property(self):
            return self.a_method()

    def test_memoize(self):
        """
        Parameterize & patch
        """
        test_instance = self.TestClass()
        with patch.object(test_instance, "a_method") as mock_method:
            test_instance.a_property()
            test_instance.a_property()
            test_instance.a_method.assert_called_once()
