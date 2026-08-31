from django import forms
from django.template.defaultfilters import first


class ContactForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    email = forms.EmailField(label='Email')


class NoteForm(forms.Form):
    title = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={"placeholder": "Title here", "class": "form-control"}))
    content = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Content here", "class": "form-control"}))
    secret_word = forms.CharField()
    confirm_secret_word = forms.CharField()

    def clean_title(self):
        title = self.cleaned_data['title'].strip()
        if len(title) < 5:
            raise forms.ValidationError('Title must be at least 5 characters')
        return title

    def clean(self):
        cleaned_data = super().clean()
        first = cleaned_data.get('secret_word')
        second = cleaned_data.get('confirm_secret_word')

        if first and second and first != second:
            raise forms.ValidationError('Secret word must be the same')
        return cleaned_data