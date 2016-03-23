from django import forms

from crow.models import Comment

EMPTY_COMMENT_ERROR = "Please add a comment."


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text', )
        error_messages = {
            'text': {'required': EMPTY_COMMENT_ERROR}
        }

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author')
        self.layer = kwargs.pop('layer')
        super().__init__(*args, **kwargs)

    def save(self):
        comment = super().save(commit=False)
        comment.author = self.author
        comment.layer = self.layer
        comment.save()
        return comment
