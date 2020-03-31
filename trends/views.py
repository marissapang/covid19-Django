from django.shortcuts import render
import pandas as pd
from .forms import CountryFilterForm

def index(request):
    df = pd.read_csv("trends/data/confirmed_cases.csv")

    country = request.GET.get('country_filter')
    if country is None: 
        country = "Global"
     
    if country == "Global":
        top_regions = df.groupby('Country')["Num_Confirmed"].agg("max").reset_index(name="Num_Confirmed") 
        top_regions = top_regions.sort_values(by=['Num_Confirmed'], ascending=False)
        top_regions = list(top_regions.head(5)['Country'])

        df = df.groupby(['Date', 'Country'])["Num_Confirmed"].agg("sum").reset_index(name="Num_Confirmed")
        df['Agg_Country'] =  df.apply(lambda row: row['Country'] if row['Country'] in top_regions else 'Other Countries', axis=1)
        df = df.groupby(['Date', 'Agg_Country'])["Num_Confirmed"].agg("sum").reset_index(name="Num_Confirmed")
        
        df = df.pivot(index='Date', columns='Agg_Country', values='Num_Confirmed')
        df = df.fillna(0)
        df = df[top_regions + ['Other Countries']] 
        dates = list(df.index)
        breakdown_names = top_regions + ['Other Countries']

    else:
        df = df[df['Country']==country]
        top_regions = df.groupby('State')["Num_Confirmed"].agg("max").reset_index(name="Num_Confirmed") 
        top_regions = top_regions.sort_values(by=['Num_Confirmed'], ascending=False)
        top_regions = list(top_regions.head(5)['State'])

        df = df.groupby(['Date', 'State'])["Num_Confirmed"].agg("sum").reset_index(name="Num_Confirmed")
        df['Agg_State'] =  df.apply(lambda row: row['State'] if row['State'] in top_regions else 'Other States', axis=1)
        df = df.groupby(['Date', 'Agg_State'])["Num_Confirmed"].agg("sum").reset_index(name="Num_Confirmed")
        
        df = df.pivot(index='Date', columns='Agg_State', values='Num_Confirmed')
        df = df.fillna(0)
        df = df[top_regions + ['Other States']] 
        dates = list(df.index)
        breakdown_names = top_regions + ['Other States']

        #df = df.groupby('Date')["Num_Confirmed"].agg("sum").reset_index(name="Num_Confirmed")
    
        #num_confirmed = list(df['Num_Confirmed'])
        #dates = list(df['Date'])
    
    country_filter_form = CountryFilterForm()
    if country != "Global":
        country_filter_form.fields['country_filter'].initial = country

    
    context = {
        'breakdown_1': list(df[top_regions[0]]),
        'breakdown_2': list(df[top_regions[1]]),
        'breakdown_3': list(df[top_regions[2]]),
        'breakdown_4': list(df[top_regions[3]]),
        'breakdown_5': list(df[top_regions[4]]),
        'breakdown_6': list(df[breakdown_names[5]]),
        'breakdown_1_name':[breakdown_names[0]],
        'breakdown_2_name':[breakdown_names[1]],
        'breakdown_3_name':[breakdown_names[2]],
        'breakdown_4_name':[breakdown_names[3]],
        'breakdown_5_name':[breakdown_names[4]],
        'breakdown_6_name':[breakdown_names[5]],
        'dates' : dates,
        'country' : country,
        'country_filter_form' : country_filter_form
     } 
    return render(request, 'index.html', context)

