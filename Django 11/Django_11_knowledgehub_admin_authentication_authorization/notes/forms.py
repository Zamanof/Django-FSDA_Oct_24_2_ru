from django import forms

from notes.models import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'category', 'tags']
        labels = {
            'title': 'Title',
            'content': 'Content',
            'category': 'Category',
            'tags': 'Tags',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }


    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        if title.lower().startswith("test"):
            raise forms.ValidationError("Title should not start with test")
        return title

