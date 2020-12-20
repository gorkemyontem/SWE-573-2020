from django import forms


class DashboardSearchForm(forms.Form):
    searchText = forms.CharField(label='searchText', max_length=100)

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass
