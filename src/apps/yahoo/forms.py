from django import forms


class YahooSearchForm(forms.Form):
    # Get the search words entered in the form
    query = forms.CharField()

    # Get the exhibition division of the product entered in the form
    # store = forms.CharField()

    # Get the product state that is entered in the form
    # item_status = forms.CharField()

    # Get the upper limit of the range specification of commodity prices entered in the form
    # aucmaxprice = forms.IntegerField()