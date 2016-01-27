from django.test import TestCase
from django.contrib.auth import get_user_model

from crow.models import Layer, Comment
from crow.forms import CommentForm


class CommentFormTest(TestCase):

    def setUp(self):
        self.layer = Layer()
        self.layer.name = 'Commented'
        self.layer.save()
        User = get_user_model()
        self.user = User.objects.create_user(username='Commenter', password='Test')

    def test_valid_data(self):
        form = CommentForm({
            'text': 'This is a comment',
        }, author=self.user, layer=self.layer)

        self.assertTrue(form.is_valid())

        comment = form.save()
        self.assertEqual(len(Comment.objects.all()), 1)
        self.assertEqual(Comment.objects.first(), comment)
        self.assertEqual(Comment.objects.first().text, 'This is a comment')

    def test_blank_data(self):
        form = CommentForm({}, author=self.user, layer=self.layer)
        self.assertFalse(form.is_valid())
        self.assertIn("Please add a comment.", form.errors['text'])
