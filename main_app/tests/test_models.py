from django.test import TestCase
from main_app.models import Post


def add_two_numbers(a, b):
    return a + b


class TestExample(TestCase):

    def test_add_two_numbers(self):
        self.assertEqual(add_two_numbers(2, 2), 4)

class ModelsTestCase(TestCase):
    def post_has_author(self):
        """Posts have author when created"""
        post = Post.objects.create(title="Test Post")
        post.author = "John Doe"
        post.body = "Testing this post"
        post.save()
        