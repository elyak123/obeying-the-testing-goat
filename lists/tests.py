from django.core.urlresolvers import resolve
from django.test              import TestCase
from lists.views              import home_page
from lists.models             import Item
from django.http              import HttpRequest

class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertIn('A new list item', response.content.decode())

class ItemModelTest(TestCase):
    def test_saving_and_retreaving_items(self):
        first_item = Item()
        first_item.text ="The first (ever) list item"
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)