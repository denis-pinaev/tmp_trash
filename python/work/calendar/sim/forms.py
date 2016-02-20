from django import forms

class VKontakteForm(forms.Form):
    viewer = forms.CharField(max_length=30, required=True)
    auth_key = forms.CharField( max_length=40, required=True)
    def clean_auth_key(self):
	from vsecure import check_auth
        if not check_auth( self.cleaned_data['viewer'], self.cleaned_data['auth_key']):
            raise forms.ValidationError("auth_key is not correct")
	return self.cleaned_data['auth_key']

class VisitForm(VKontakteForm):
    user = forms.CharField(max_length=30, required=True)
