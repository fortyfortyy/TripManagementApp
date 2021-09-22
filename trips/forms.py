from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from .models import TripPlan, Trip


class TripPlanCreateEditForm(forms.ModelForm):
    class Meta:
        model = TripPlan
        # TODO w jaki sposób dodać też tagi do tego formularza jeśli ma ManyToMany field?
        fields = ('name', 'tags', 'is_private')

    tags = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'name': 'tags'}))


class TripCreateForm(forms.Form):
    country = forms.CharField(label='Country', max_length=50)
    city = forms.CharField(label='City', max_length=50)
    day_from = forms.DateField(label='Date From', widget=forms.DateInput(attrs={'type': 'date'}))
    day_to = forms.DateField(label='Date To', widget=forms.DateInput(attrs={'type': 'date'}))
    short_description = forms.CharField(widget=forms.TextInput(attrs={'size': '40'}))

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

#
# class TripEditForm(ModelForm):
#     class Meta:
#         model = Trip
#         # fields = ('countries', 'cities', 'descriptions', 'date_range', 'trip_images')
#         fields = '__all__'

    # def __init__(self, *args, **kwargs):
    #     super(TripEditForm, self).__init__(*args, **kwargs)
    #
    #     self.fields['countries'].widget.attrs.update(
    #         {'type': 'text', 'placeholder': 'country'})
    #
    #     self.fields['cities'].widget.attrs.update(
    #         {'type': 'date'})
    #
    #     self.fields['descriptions'].widget.attrs.update(
    #         {'type': 'date', 'placeholder': 'description'})
    #
    #     self.fields['date_range'].widget.attrs.update(
    #         {'type': 'date', 'name': 'day_to', 'class': 'form-control'})
