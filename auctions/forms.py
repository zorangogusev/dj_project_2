from django.forms import ModelForm
from django import forms

from .models import List, ListComment, Bid


class ListForm(ModelForm):
    class Meta:
        model = List
        fields = ['title', 'description', 'start_bid', 'category', 'photo']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'start_bid': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }


class ListCommentForm(ModelForm):
    class Meta:
        model = ListComment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter comment...',
            })
        }


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['price']
