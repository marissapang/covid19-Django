from django import forms
import pandas as pd

df = pd.read_csv("trends/data/confirmed_cases.csv")
df = df.groupby(['Country', 'Date'])["Num_Confirmed"].agg("sum").reset_index(name="Num_Confirmed")
df = df.groupby('Country')["Num_Confirmed"].agg("max").reset_index(name="Num_Confirmed")
df = df.sort_values(by=['Num_Confirmed'], ascending=False)

country_choices = df['Country']
country_choices = list(zip(country_choices, country_choices))
country_choices = [('Global','Global')]+country_choices

class CountryFilterForm(forms.Form):
   confirmed_country_filter = forms.ChoiceField(choices = country_choices, label = "Country", initial="Global", required=False)
   deaths_country_filter = forms.ChoiceField(choices = country_choices, label = "Country", initial="Global", required=False)
