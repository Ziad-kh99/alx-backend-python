#!/usr/bin/env python3

"""
Parameterize a unit test
"""
import unittest
from client import GithubOrgClient
from parameterized import parameterized, parameterized_class
from unittest.mock import patch

from unittest.mock import PropertyMock
from parameterized import parameterized_class
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """
    TestGithubOrgClient class
    """

    @parameterized.expand(
        [
            ("google"),
            ("abc"),
        ]
    )
    @patch("client.get_json")
    def test_org(self, url, mock_get):
        """
        test_org
        """
        res = GithubOrgClient(url)
        res.org()
        mock_get.assert_called_once()

    def test_public_repos_url(self):
        """
        test_public_repos_url
        """
        with patch.object(
            GithubOrgClient,
            "org",
            new_callable=PropertyMock,
            return_value={"repos_url": "testURL"},
        ) as mock_get:
            client_json = {"repos_url": "testURL"}
            client_repos_url = GithubOrgClient(client_json.get("repos_url"))
            res = client_repos_url._public_repos_url
            self.assertEqual(res, mock_get.return_value.get("repos_url"))
            mock_get.assert_called_once

    @patch("client.get_json", return_value=[{"name": "testName"}])
    def test_public_repos(self, mock_get):
        """
        test_public_repos
        """
        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock,
            return_value="testURL",
        ) as mock_pub:
            client_pub_repo = GithubOrgClient("testName")
            res_pub_repo = client_pub_repo.public_repos()
            self.assertEqual(res_pub_repo, ["testName"])
            mock_pub.assert_called_once
            mock_get.assert_called_once

    @parameterized.expand(
        [
            ({"license": {"key": "my_license"}}, "my_license", True),
            ({"license": {"key": "other_license"}}, "my_license", False),
        ]
    )
    def test_has_license(self, repo, license_key, expacted):
        """
        test_has_license
        """
        test_client = GithubOrgClient("test_url")
        test_license = test_client.has_license(repo, license_key)
        self.assertEqual(test_license, expacted)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"), TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration test for GithubOrgClient
    """

    @classmethod
    def setUpClass(cls):
        """
        setup the data
        """
        cls.get_patcher = patch("requests.get", side_effect="HTTPError")

    @classmethod
    def tearDownClass(cls):
        """
        cleaning up
        """
        cls.get_patcher.stop()
