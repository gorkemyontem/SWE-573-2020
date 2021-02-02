from django import forms


class DashboardSearchForm(forms.Form):
    searchText = forms.CharField(label='searchText', max_length=100)
