from django import forms
from book.models import Book, Comment, Parent
from django.db.migrations.state import get_related_models_tuples
from django.utils.translation import gettext_lazy as _



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        

        fields = ['name', 'content']
        
        labels = {
            'content': _(''),
        }
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'comment_form'}
                ),
        }



class CommentChilderenForm(forms.ModelForm):
    class Meta:
        model = Parent

        fields = ['name_reply', 'content_reply', 'comment']

        widgets = {
            'content_reply' : forms.TextInput(attrs={
                'class': 'form-control',
                }),
        }
