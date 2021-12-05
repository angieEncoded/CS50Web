from django import forms


class NewPostForm(forms.Form):
    content = forms.CharField(label="", max_length=75,
                                  widget=forms.Textarea(attrs={'class': "form-control mb-2", 'required': True, "cols": 10, "rows": 5}))
