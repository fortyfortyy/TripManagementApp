from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import Trip


class TripCreateForm(forms.Form):
    name = forms.CharField(max_length=200,
                           label='Trip Name',
                           widget=forms.TextInput(attrs={'placeholder': 'dream holidays...'}),
                           )
    day_from = forms.DateField(label='Day From', widget=forms.DateInput(attrs={'type': 'date'}))
    day_to = forms.DateField(label='Date To', widget=forms.DateInput(attrs={'type': 'date'}))

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 3:
            raise ValidationError(_('Minimum 4 characters are required.'), code='trip_name_error')
        if Trip.objects.filter(name=name).exists():
            raise ValidationError(_("Sorry, this trip name already exists. Please try to write another trip name."),
                                  code='trip_exists_error')
        return name
