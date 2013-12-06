from django import forms


class YahooSearchForm(forms.Form):

    TYPE_CHOICES = (
        ('all', 'All'),  # search results containing all query string
        ('any', 'Any')   # search results that contain any of the query string
    )

    SORT_CHOICES = (
        ('end', 'End time'),
        ('img', 'Presence or absence of image'),
        ('bids', 'Number of bids'),
        ('cbids', 'Current price'),
        ('Bidorbuy', 'Prompt decision price'),
        ('Affiliate', 'Affiliate')
    )

    # Get the search words entered in the form
    query = forms.CharField()

    type = forms.CharField(widget=forms.Select(choices=TYPE_CHOICES))

    sort = forms.CharField(widget=forms.Select(choices=SORT_CHOICES))
    # Get the product state that is entered in the form
    # item_status = forms.CharField()

    # Get the upper limit of the range specification of commodity prices entered in the form
    # aucmaxprice = forms.IntegerField()