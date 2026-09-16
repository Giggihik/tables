from django import forms
from .models import Category, Quote


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['text', 'category']
