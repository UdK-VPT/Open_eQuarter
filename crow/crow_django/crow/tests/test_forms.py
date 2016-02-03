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
        },
            author=self.user,
            layer=self.layer)

        self.assertTrue(form.is_valid())

        comment = form.save()
        self.assertEqual(len(Comment.objects.all()), 1)
        self.assertEqual(Comment.objects.first(), comment)
        self.assertEqual(Comment.objects.first().text, 'This is a comment')

    def test_blank_data(self):
        form = CommentForm({}, author=self.user, layer=self.layer)
        self.assertFalse(form.is_valid())
        self.assertIn("Please add a comment.", form.errors['text'])

    def test_if_multiple_comments_can_be_added_by_same_user(self):
         form1 = CommentForm({
             'text': 'This is a first comment',
         },
             author=self.user,
             layer=self.layer,
         )
         form1.save()

         form2 = CommentForm({
             'text': 'This is a second comment',
         },
             author=self.user,
             layer=self.layer,
         )
         form2.save()

         saved_comments = Comment.objects.all()
         self.assertEqual(len(saved_comments), 2)
