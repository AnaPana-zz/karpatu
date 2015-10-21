import os
import unittest

from karpatu import app


class MainTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass


class ViewsTestCase(MainTestCase):

    def test_main_view(self):
        response = self.app.get('/')
        assert response.status_code == 200
        assert 'Старая Гута' in response.data.decode('utf-8')


class MainMenuTestCase(MainTestCase):

    def test_index_main_menu(self):
        response = self.app.get('/')
        assert """<li class="active">        <a href="/">Главная</a>    </li>""" in \
               response.data.decode('utf-8').replace("\n", "")

    def test_rent_main_menu(self):
        response = self.app.get('/rent/')
        assert """<li class="active">        <a href="/rent/">Снять жилье</a>    </li>""" in \
               response.data.decode('utf-8').replace("\n", "")


if __name__ == '__main__':
    unittest.main()