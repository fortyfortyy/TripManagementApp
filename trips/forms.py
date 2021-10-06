from django import forms
from django.core.exceptions import ValidationError
from django.forms import modelformset_factory
from django.utils.translation import ugettext_lazy as _

from .models import TripPlan, Trip, Description, City, Country, Tag


class TripPlanCreateEditForm(forms.ModelForm):
    class Meta:
        model = TripPlan
        fields = ('name', 'is_private')


class TagForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TagForm, self).__init__(*args, **kwargs)
        self.fields['tag'].initial = '#'

    class Meta:
        model = Tag
        fields = ('tag',)
        widgets = {
            'tag': forms.TextInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': '#holidays',
            }),
        }


TagFormSet = modelformset_factory(Tag, form=TagForm, extra=1, can_delete=True)


class TripCreateForm(forms.Form):
    country = forms.CharField(label='Country', max_length=50)
    city = forms.CharField(label='City', max_length=50)
    day_from = forms.DateField(label='Date From', widget=forms.DateInput(attrs={'type': 'date'}))
    day_to = forms.DateField(label='Date To', widget=forms.DateInput(attrs={'type': 'date'}))
    short_description = forms.CharField(widget=forms.TextInput(attrs={'size': '40'}))

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 3:
            raise ValidationError(_('Minimum 4 characters are required.'), code='trip_name_error')
        if Trip.objects.filter(name=name).exists():
            raise ValidationError(_("Sorry, this trip name already exists. "
                                    "Please try to write another trip name."),
                                  code='trip_exists_error')
        return name


class TripDescriptionForm(forms.ModelForm):
    class Meta:
        model = Description
        fields = ('trip', 'content',)
        widgets = {
            'trip': forms.HiddenInput(),
            'content': forms.TextInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'visit a museum...',
            }),
        }


DescriptionFormSet = modelformset_factory(Description, form=TripDescriptionForm, extra=1, can_delete=True)


class CityForm(forms.ModelForm):

    class Meta:
        model = City
        fields = ('city',)
        widgets = {
            'city': forms.TextInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Barcelona...',
            }),
        }


CityFormSet = modelformset_factory(City, form=CityForm, extra=1, can_delete=True)


class CountryForm(forms.ModelForm):

    class Meta:
        model = Country
        fields = ('country',)
        widgets = {
            'country': forms.TextInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Spain...',
            }),
        }


CountryFormSet = modelformset_factory(Country, form=CountryForm, extra=1, can_delete=True)
