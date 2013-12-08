from django import forms


class YahooSearchForm(forms.Form):

    # TYPE_CHOICES = (
    #     ('all', 'All'),  # search results containing all query string
    #     ('any', 'Any')   # search results that contain any of the query string
    # )

    SORT_CHOICES = (
        ('end', 'End time'),
        ('img', 'Presence or absence of image'),
        ('bids', 'Number of bids'),
        ('cbids', 'Current price'),
        ('Bidorbuy', 'Prompt decision price'),
        ('Affiliate', 'Affiliate')
    )

    ORDER_CHOICES = (
        ('a', 'Ascending'),
        ('d', 'Descending')
    )

    ITEM_STATUS_CHOICES = (
        (0, 'Not specified'),
        (1, 'New'),
        (2, 'Used')
    )

    F_CHOICES = (
        ('0x2', 'Search for "Title + store for Search"'),
        ('0x4', 'Search for "Title + body"'),
        ('0x8', 'Search for "title only"')
    )

    # Get the search words entered in the form
    query = forms.CharField()

    # type = forms.CharField(widget=forms.Select(choices=TYPE_CHOICES))

    sort = forms.CharField(widget=forms.Select(choices=SORT_CHOICES))
    order = forms.CharField(widget=forms.Select(choices=ORDER_CHOICES))
    category = forms.IntegerField(required=False)

    # Get the product state that is entered in the form
    item_status = forms.CharField(widget=forms.Select(choices=ITEM_STATUS_CHOICES))

    f = forms.CharField(widget=forms.Select(choices=F_CHOICES))

    # Get the upper limit of the range specification of commodity prices entered in the form
    aucminprice = forms.IntegerField(required=False)
    aucmaxprice = forms.IntegerField(required=False)