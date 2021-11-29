from django import forms
from .models import Category, Auction, Watchlist, Bid, Comment
# Create a form in Django - this time I figured out how to at least add some classes to the inputs.
# I pulled this out of the main file because it's getting wayyyy too long

class NewListingForm(forms.Form):
    title = forms.CharField(label="Listing Title", max_length=100,
                            widget=forms.TextInput(attrs={'class': "form-control mb-2", 'required': True, 'placeholder': "Enter a title for your listing here"}))
    description = forms.CharField(label="Description", max_length=100,
                                  widget=forms.Textarea(attrs={'class': "form-control mb-2", 'required': True}))
    url = forms.CharField(label="Image URL", max_length=100, required=False,
                          widget=forms.TextInput(attrs={'class': "form-control mb-2", "placeholder": "Enter a url to an image"}))
    starting_bid = forms.CharField(label="Starting Bid in US Dollars",
                                   widget=forms.TextInput(attrs={'class': "form-control mb-2",  'placeholder': "Enter the starting bid here in US Dollars (i.e. 10.50)"}))
    categories = forms.ModelChoiceField(
        queryset=Category.objects.all(), empty_label="Select one...", widget=forms.Select(attrs={'class': 'form-select mb-2', 'required': True}))


class bidForm(forms.Form):
    bid_amount = forms.CharField(label="", widget=forms.TextInput(attrs={'class': "form-control mb-2",  'placeholder': "Enter your bid here", "placeholder":'Enter an amount in US Dollars' }))


class simpleListForm(forms.Form):
    listing = forms.CharField(label="listing", widget=forms.TextInput(
        attrs={'class': "form-control mb-2", 'required': True}))


class commentForm(forms.Form):
    comment = forms.CharField(label="Add a comment:", max_length=500,
                              widget=forms.Textarea(attrs={'class': "form-control mb-2 mt-1", 'required': True}))

