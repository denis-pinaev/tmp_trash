from django import forms

class TestAddCommunicatorForm(forms.Form):                                                                                                                                                                                       
    host = forms.CharField(max_length=128, required=True)                                                                                                                                                            
    port = forms.IntegerField(required=True)
    
class TestDeleteCommunicatorForm(forms.Form):                                                                                                                                                                                       
    ids = forms.RegexField(max_length=1024, regex=r'^[\d+,]+$',
        help_text = "Required. Digits and ',' only.", error_messages = {'invalid': "This value may contain only numbers and ',' characters."})      

class TestAddArchiveForm(forms.Form):                                                                                                                                                                                       
    ip = forms.CharField(max_length=128, required=True)                                                                                                                                                            
    #port = forms.IntegerField(required=True)
    url = forms.CharField(max_length=150, required=True)
    #save_dir = forms.CharField(max_length=150, required=True)
    id = forms.IntegerField(required=False)
    
class TestDeleteArchiveForm(forms.Form):                                                                                                                                                                                       
    id = forms.RegexField(max_length=1024, regex=r'^\d+$',
        help_text = "Required. Digits and ',' only.", error_messages = {'invalid': "This value may contain only numbers and ',' characters."})                                                                                                                                                           