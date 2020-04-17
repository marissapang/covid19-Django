from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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

class UpdateDashboardForm(forms.Form):
	countries = forms.MultipleChoiceField(choices = country_choices, label = "Select Countries", widget=forms.CheckboxSelectMultiple, blank=True)
	states = forms.MultipleChoiceField(choices = state_choices, label = "Select States", widget=forms.CheckboxSelectMultiple, blank=True)
	date_range = forms.ChoiceField(choices = date_range_options, blank=True)

class UpdateDashboardFormMobile(forms.Form):
	countries = forms.MultipleChoiceField(choices = country_choices, label = "Select Countries", blank=True)
	states = forms.MultipleChoiceField(choices = state_choices, label = "Select States", blank=True)
	date_range = forms.ChoiceField(choices = date_range_options, blank=True)

# class UpdateDashboardCountryForm(forms.Form):
# 	countries = forms.MultipleChoiceField(choices = country_choices, label = "Select Countries", widget=forms.CheckboxSelectMultiple)

# class UpdateDashboardStateForm(forms.Form):
# 	states = forms.MultipleChoiceField(choices = state_choices, label = "Select States", widget=forms.CheckboxSelectMultiple)

# class UpdateDashboardCountryFormMobile(forms.Form):
# 	countries = forms.MultipleChoiceField(choices = country_choices, label = "Select Countries")

# class UpdateDashboardStateFormMobile(forms.Form):
# 	states = forms.MultipleChoiceField(choices = state_choices, label = "Select States")

# class UpdateDashboardDateRangeForm(forms.Form):
# 	date_range = forms.ChoiceField(choices = date_range_options)


