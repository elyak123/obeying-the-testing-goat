from django.core.urlresolvers import resolve
from django.test              import TestCase
from lists.views              import home_page
from django.http              import HttpRequest

class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')