from django.shortcuts import render
import pandas as pd
from .forms import CountryFilterForm

def index(request):
    df = pd.read_csv("trends/data/confirmed_cases.csv")

    country = request.GET.get('country_filter')
    if country is None: 
        country = "Global"
     
    if country != "Global":
        df = df[df['Country']==country]

    df = df.groupby('Date')["Num_Confirmed"].agg("sum").reset_index(name="Num_Confirmed")
    
    num_confirmed = list(df['Num_Confirmed'])
    dates = list(df['Date'])
 
    country_filter_form = CountryFilterForm()
    if country != "Global":
        country_filter_form.fields['country_filter'].initial = country

    context = {
        'num_confirmed' : num_confirmed,
        'dates' : dates,
        'country' : country,
        'country_filter_form' : country_filter_form
     } 
    return render(request, 'index.html', context)

