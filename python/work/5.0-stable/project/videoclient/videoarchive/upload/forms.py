from django import forms
import models

class FileUploadForm(forms.ModelForm):
    def clean_file(self):
        max_size = 8 * 2**20 #8Mb
        file = self.cleaned_data.get('file')
        self.size = len(file)
        return file
        if len(file) > max_size:
            raise forms.ValidationError('too large image')
        else:
            return file
        
    class Meta:
        model = models.Files