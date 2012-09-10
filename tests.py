__author__ = 'Richie Foreman <richie.foreman@gmail.com>'

import unittest
import py4chan

BOARD = 'wsg'
TEST_THREAD = 1
py4chan.SSL = False

class Test_Py4Chan(unittest.TestCase):

    def test_get_thread(self):
        posts = py4chan.get_thread(BOARD, TEST_THREAD)
        for post in posts:
            self.assertTrue(isinstance(post, py4chan.Post))

    def test_https_file_is_https(self):
        py4chan.SSL = True

        posts = py4chan.get_thread(BOARD, TEST_THREAD)
        for post in posts:
            if post.get_file_url():
                self.assertIn('https', post.get_file_url())

    def test_file_url(self):
        posts = py4chan.get_thread(BOARD, TEST_THREAD)

        for post in posts:
            url = post.get_file_url()
            if url is not None:
                self.assertIn('images.4chan.org', url)
                headers, _ = py4chan.http.request(url)
                self.assertEqual(headers["status"], "200")

    def test_transport_options(self):

        old_setting = py4chan.SSL

        py4chan.SSL = True
        self.assertTrue(py4chan._get_transport(), 'https')
        self.assertIn('https', py4chan._get_api_root())

        py4chan.SSL = False
        self.assertTrue(py4chan._get_transport(), 'http')
        self.assertIn('http', py4chan._get_api_root())

        py4chan.SSL = old_setting

    def test_missing_thread_raises_404(self):
        try:
            posts = py4chan.get_thread(BOARD, 'over9000')
            for p in posts:
                pass
        except py4chan.HttpException, e:
            self.assertEqual(e[0],404)
            self.assertRaises(py4chan.HttpException)

if __name__ == '__main__':
    unittest.main()
