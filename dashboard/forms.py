from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import requests
import request

class SignUpForm(UserCreationForm):
	first_name = forms.CharField(max_length=50, required=False, help_text='Optional.')
	last_name = forms.CharField(max_length=50, required=False, help_text='Optional.')
	email = forms.EmailField(max_length=254, help_text='Required. You can re-set your password through this email.')

	class Meta: 
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


import pandas as pd

df = pd.read_csv("trends/data/confirmed_cases.csv")
df = df.groupby('Country')["Num_Confirmed"].agg("sum")
unique_countries = df.index
country_choices = list(zip(unique_countries, unique_countries))
country_choices = [('Global','Global')]+country_choices

class UpdateDashboardCountryForm(forms.Form):
	countries = forms.MultipleChoiceField(choices = country_choices, label = "Select Countries", widget=forms.CheckboxSelectMultiple)



