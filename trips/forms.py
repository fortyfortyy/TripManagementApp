from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import TripPlan, Trip


class TripPlanCreateForm(forms.ModelForm):
    class Meta:
        model = TripPlan
        fields = ('name', 'is_private')
    # day_from = forms.DateField(label='Trip From', widget=forms.DateInput(attrs={'type': 'date'}))
    # day_to = forms.DateField(label='Trip To', widget=forms.DateInput(attrs={'type': 'date'}))
    # country = forms.CharField(label='Country', max_length=50)
    # city = forms.CharField(label='City', max_length=50)
    # tag = forms.CharField(label='Tag', max_length=50, initial='#')


class TripCreateForm(forms.Form):
    country = forms.CharField(label='Country', max_length=50)
    city = forms.CharField(label='City', max_length=50)
    day_from = forms.DateField(label='Date From', widget=forms.DateInput(attrs={'type': 'date'}))
    day_to = forms.DateField(label='Date To', widget=forms.DateInput(attrs={'type': 'date'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'size': '40'}))

    # class Meta:
    #     model = Trip
    #     fields = ('name', 'day_from', 'day_to', 'countries', 'cities', 'tags', 'is_private')
    #
    # def __init__(self, *args, **kwargs):
    #     super(TripCreateForm, self).__init__(*args, **kwargs)

    #     self.fields['name'].widget.attrs.update(
    #         {'type': 'text', 'name': 'name', 'class': 'form-control', 'placeholder': 'Trip name'})
    #
    # self.fields['day_from'].widget.attrs.update(
    #     {'type': 'date', 'name': 'day_from', 'class': 'form-control'})
    #
    # self.fields['day_to'].widget.attrs.update(
    #     {'type': 'date', 'name': 'day_to', 'class': 'form-control'})
    #
    #     self.fields['countries'].widget.attrs.update(
    #         {'type': 'text', 'name': 'countries', 'class': 'form-control', 'placeholder': 'Country'})
    #
    #     self.fields['cities'].widget.attrs.update(
    #         {'type': 'text', 'name': 'cities', 'class': 'form-control', 'placeholder': 'Tags'})
    #
    #     self.fields['tags'].widget.attrs.update(
    #         {'type': 'text', 'name': 'tags', 'class': 'form-control', 'placeholder': 'Tags'})
    #
    #     self.fields['is_private'].widget.attrs.update(
    #         {'type': 'boolean', 'name': 'is_private', 'class': 'form-control', 'placeholder': 'Email address'})

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 3:
            raise ValidationError(_('Minimum 4 characters are required.'), code='trip_name_error')
        if Trip.objects.filter(name=name).exists():
            raise ValidationError(_("Sorry, this trip name already exists. Please try to write another trip name."),
                                  code='trip_exists_error')
        return name
