"""cover app api with testcases"""
import unittest
import app


class TestGithubApi(unittest.TestCase):
    """ test grapql github queries"""
    def test_get_github_name_positive(self):
        """ test if exists user with specified login """
        self.assertIsNotNone(app.get_github_name("dhh")["user"])

    def test_get_github_name_concrete(self):
        """ test if exists user with specified login """
        self.assertEqual(app.get_github_name("dhh")["user"]["name"], "David Heinemeier Hansson")

    def test_get_github_name_negative(self):
        """ test if user that not exist return None """
        self.assertIsNone(app.get_github_name("undefined_user12345")["user"])

    def test_get_github_repos_count_positive(self):
        """ test that repository count for specified existed user is not None """
        self.assertIsNotNone(app.get_github_repos_count("dhh")["count"])

    def test_get_github_repos_count_negative(self):
        """ test that status code is 500 for not  existed user  """
        self.assertEqual(app.get_github_repos_count("undefined_user12345")["status"], 500)

    def test_get_github_repos_info_positive(self):
        """ test that repo info is not None for existed user  """
        self.assertIsNotNone(app.get_github_repos_info("dhh")["repo_info"])

    def test_get_github_repos_info_negative(self):
        """ test that response is with 500 status code for not existed user  """
        self.assertEqual(app.get_github_repos_info("undefined_user12345")["status"], 500)


if __name__ == '__main__':
    unittest.main()
