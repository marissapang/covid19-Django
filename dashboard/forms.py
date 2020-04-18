from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django_toggle_switch_widget.widgets import DjangoToggleSwitchWidget

class SignUpForm(UserCreationForm):
	first_name = forms.CharField(max_length=50, required=False, help_text='Optional.')
	last_name = forms.CharField(max_length=50, required=False, help_text='Optional.')
	email = forms.EmailField(max_length=254, help_text='Required. You can re-set your password through this email.')

	class Meta: 
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


import pandas as pd

# get country choices
df = pd.read_csv("trends/data/confirmed_cases.csv")
df = df.groupby('Country')["Num_Confirmed"].agg("sum")
unique_countries = df.index
country_choices = list(zip(unique_countries, unique_countries))
country_choices = [('None', 'None')]+[('Global','Global')]+country_choices

# get state choices
df = pd.read_csv("trends/data/confirmed_cases.csv")
df = df[df['Country'].isin(['Australia', 'Canada', 'United States', 'China'])]
countries_w_state_level_data = ['Australia', 'Canada', 'China', 'United States']
country_state_list = []
for country in countries_w_state_level_data:
	country_data = df[df['Country'] == country]
	country_data = country_data.groupby('State')["Num_Confirmed"].agg("sum")
	unique_states = country_data.index
	unique_states = [(country, tuple(zip(unique_states, unique_states)))]
	country_state_list += unique_states
none_list = [("", (("None", "None"),))]
state_choices = tuple(none_list + country_state_list)

# get date choices
date_range_options = ["All time", "Past 2 months", "Past month", "Past 2 weeks"]
date_range_options = list(zip(date_range_options, date_range_options))

data_choices = ["Cumulative", "Incremental"]
data_choices = list(zip(data_choices, data_choices))

class UpdateDashboardForm(forms.Form):
	countries = forms.MultipleChoiceField(choices = country_choices, label = "Select Countries", widget=forms.CheckboxSelectMultiple, required=False)
	states = forms.MultipleChoiceField(choices = state_choices, label = "Select States", widget=forms.CheckboxSelectMultiple, required=False)
	date_range = forms.ChoiceField(choices = date_range_options, required=False)

class UpdateDashboardFormMobile(forms.Form):
	countries = forms.MultipleChoiceField(choices = country_choices, label = "Select Countries",  widget=forms.SelectMultiple(attrs={'style':'width:90px;'}), required=False)
	states = forms.MultipleChoiceField(choices = state_choices, label = "Select States", widget=forms.SelectMultiple(attrs={'style':'width:90px;'}), required=False)
	date_range = forms.ChoiceField(choices = date_range_options, widget=forms.Select(attrs={'style':'width:90px;'}), required=False)
	cum_vs_incr = forms.ChoiceField(choices=data_choices, widget=forms.Select(attrs={'style':'width:90px;'}), required=False)

class SummStatFilterForm(forms.Form):
	country = forms.ChoiceField(choices = country_choices, widget=forms.Select(attrs={'class':'btn btn-outline-secondary','style':'height:30px;width:85px;margin-bottom:10px;'}), initial="Global")

class SummStatFilterFormMobile(forms.Form):
	country = forms.ChoiceField(choices = country_choices, widget=forms.Select(attrs={'class':'btn','style':'font-size:14px;height:22px;width:85px;padding:1px; margin-bottom:2px'}), initial="Global")

class DataTypeForm(forms.Form):
	data_type = forms.ChoiceField(choices=data_choices, initial="Cumulative")


