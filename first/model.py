from django import forms
from .models import UploadedImage

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ('image',)


class ModelSelectionForm(forms.Form):
    model_choices = (
        ('model1', 'Model 1'),
        ('model2', 'Model 2'),
    )
    model = forms.ChoiceField(choices=model_choices, widget=forms.RadioSelect)
