from django import forms

class NoteForm(forms.Form):
    CATEGORY_CHOICES = [
        ("study", "Study"),
        ("work", "Work"),
        ('personal', 'Personal')
    ]
    title = forms.CharField(
        label='Title',
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Enter note title"}),
    )
    content = forms.CharField(
        label='Text',
    widget=forms.Textarea(attrs={"placeholder": "Write your note", "rows": "6"}),
    min_length=20)
    tags = forms.CharField(
        label='Tags',
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Example: django python"}),
    )
    category = forms.ChoiceField(
        label='Category',
        choices=CATEGORY_CHOICES)


    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        if title.lower().startswith("test"):
            raise forms.ValidationError("Title should not start with test")
        return title

