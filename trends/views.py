from django.shortcuts import render
import pandas as pd
from .forms import CountryFilterForm

def index(request):
    df = pd.read_csv("trends/data/confirmed_cases.csv")
    df_deaths = pd.read_csv("trends/data/num_deaths.csv")


    ###################################
    ###### COUNTRY CHARTS BEGINS ######
    country_confirmed = request.GET.get('confirmed_country_filter')
    country_deaths= request.GET.get('deaths_country_filter')

    if country_confirmed is not None:
        request.session['country_confirmed'] = country_confirmed

    if country_deaths is not None:
        request.session['country_deaths'] = country_deaths

    country_confirmed = request.session.get('country_confirmed', 'Global')
    country_deaths = request.session.get('country_deaths', 'Global')
     
    if country_confirmed == "Global":
        df = df.groupby(['Country','Date'])["Num_Confirmed"].agg("sum").reset_index(name="Num_Confirmed") 
        top_regions = df.groupby('Country')["Num_Confirmed"].agg("max").reset_index(name="Num_Confirmed") 
        top_regions = top_regions.sort_values(by=['Num_Confirmed'], ascending=False)
        top_regions = list(top_regions.head(5)['Country'])

        df['Agg_Country'] =  df.apply(lambda row: row['Country'] if row['Country'] in top_regions else 'Other Countries', axis=1)
        df = df.groupby(['Date', 'Agg_Country'])["Num_Confirmed"].agg("sum").reset_index(name="Num_Confirmed")
        
        df = df.pivot(index='Date', columns='Agg_Country', values='Num_Confirmed')
        df = df.fillna(0)
        df = df[top_regions + ['Other Countries']] 
        dates = list(df.index)

        breakdown_names = top_regions + ['Other Countries']
        breakdown_data = []
        for region in breakdown_names:
            breakdown_data += [list(df[region])]
    else:
        df = df[df['Country']==country_confirmed]
        unique_states = list(df['State'].unique())

        if len(unique_states) > 1:
            df = df.groupby(['Date', 'State'])["Num_Confirmed"].agg("sum").reset_index(name="Num_Confirmed")
            top_regions = df.groupby('State')["Num_Confirmed"].agg("max").reset_index(name="Num_Confirmed") 
            top_regions = top_regions.sort_values(by=['Num_Confirmed'], ascending=False)
            top_regions = list(top_regions.head(5)['State'])

            df['Agg_State'] =  df.apply(lambda row: row['State'] if row['State'] in top_regions else 'Other States', axis=1)
            df = df.groupby(['Date', 'Agg_State'])["Num_Confirmed"].agg("sum").reset_index(name="Num_Confirmed")
            
            df = df.pivot(index='Date', columns='Agg_State', values='Num_Confirmed')
            df = df.fillna(0)
            df = df[top_regions + ['Other States']] 
            dates = list(df.index)

            breakdown_names = top_regions + ['Other States']
            breakdown_data = []

            for region in breakdown_names:
                breakdown_data += [list(df[region])]

        else: 
            dates = list(df['Date'].unique())
            df = df.groupby(['Date'])["Num_Confirmed"].agg("sum").reset_index(name="Num_Confirmed")
            breakdown_names = [[country_confirmed]]
            breakdown_data = [list(df['Num_Confirmed'])]

    if country_deaths == "Global":

        df_deaths = df_deaths.groupby(['Country','Date'])["Num_Deaths"].agg("sum").reset_index(name="Num_Deaths") 
        top_regions_deaths = df_deaths.groupby('Country')["Num_Deaths"].agg("max").reset_index(name="Num_Deaths") 
        top_regions_deaths = top_regions_deaths.sort_values(by=['Num_Deaths'], ascending=False)
        top_regions_deaths = list(top_regions_deaths.head(5)['Country'])

        df_deaths['Agg_Country'] =  df_deaths.apply(lambda row: row['Country'] if row['Country'] in top_regions_deaths else 'Other Countries', axis=1)
        df_deaths = df_deaths.groupby(['Date', 'Agg_Country'])["Num_Deaths"].agg("sum").reset_index(name="Num_Deaths")
        
        df_deaths = df_deaths.pivot(index='Date', columns='Agg_Country', values='Num_Deaths')
        df_deaths = df_deaths.fillna(0)
        df_deaths = df_deaths[top_regions_deaths + ['Other Countries']] 

        breakdown_deaths_names = top_regions_deaths + ['Other Countries']
        breakdown_deaths_data = []
        for region in breakdown_deaths_names:
            breakdown_deaths_data += [list(df_deaths[region])]
    else: 
        df_deaths = df_deaths[df_deaths['Country']==country_deaths]
        unique_states_deaths = list(df_deaths['State'].unique())

        if len(unique_states_deaths) > 1:
            df_deaths = df_deaths.groupby(['Date', 'State'])["Num_Deaths"].agg("sum").reset_index(name="Num_Deaths")
            top_regions_deaths = df_deaths.groupby('State')["Num_Deaths"].agg("max").reset_index(name="Num_Deaths") 
            top_regions_deaths = top_regions_deaths.sort_values(by=['Num_Deaths'], ascending=False)
            top_regions_deaths = list(top_regions_deaths.head(5)['State'])

            df_deaths['Agg_State'] =  df_deaths.apply(lambda row: row['State'] if row['State'] in top_regions_deaths else 'Other States', axis=1)
            df_deaths = df_deaths.groupby(['Date', 'Agg_State'])["Num_Deaths"].agg("sum").reset_index(name="Num_Deaths")
            
            df_deaths = df_deaths.pivot(index='Date', columns='Agg_State', values='Num_Deaths')
            df_deaths = df_deaths.fillna(0)
            df_deaths = df_deaths[top_regions_deaths + ['Other States']] 

            breakdown_deaths_names = top_regions_deaths + ['Other States']
            breakdown_deaths_data = []

            for region in breakdown_deaths_names:
                breakdown_deaths_data += [list(df_deaths[region])]
        else: 
            df_deaths = df_deaths.groupby(['Date'])["Num_Deaths"].agg("sum").reset_index(name="Num_Deaths")
            breakdown_deaths_names = [[country_deaths]]
            breakdown_deaths_data = [list(df_deaths['Num_Deaths'])]


    country_filter_form = CountryFilterForm()
    country_filter_form.fields['confirmed_country_filter'].initial = country_confirmed
    country_filter_form.fields['deaths_country_filter'].initial = country_deaths

    ####### COUNTRY CHARTS ENDS #######
    ###################################

    ###################################
    ##### DEATH RATE CHART BEGINS #####
    death_rates = pd.read_csv("trends/data/death_rate.csv")
    death_rate_dict = {}

    continents = ["Europe", "Asia Pacific", "Americas", "Middle East"]

    for c in continents:
        cont_death_rates = death_rates[death_rates['Continent']==c].reset_index()
        # cont_death_rates = death_rates
        cont_data = []
        for row in range(len(cont_death_rates.index)):
            row_dict = {}
            row_dict['x'] = cont_death_rates['GDP_Per_Capita'][row]
            row_dict['y'] = cont_death_rates['Death_Rate'][row]
            row_dict['z'] = cont_death_rates['Num_Confirmed'][row]
            row_dict['num_deaths'] = cont_death_rates['Num_Deaths'][row]
            row_dict['name'] = cont_death_rates['Country_Abbr'][row]
            row_dict['country'] = cont_death_rates['Country'][row]
            cont_data += [row_dict]
        death_rate_dict[c] = cont_data


    ###### DEATH RATE CHART ENDS ######
    ###################################

    context = {
        'tab': 'insights',
        'breakdown_data': breakdown_data,
        'breakdown_names':breakdown_names,
        'breakdown_deaths_data':breakdown_deaths_data,
        'breakdown_deaths_names':breakdown_deaths_names,
        'dates' : dates,
        'country_confirmed' : country_confirmed,
        'country_deaths': country_deaths,
        'country_filter_form' : country_filter_form,
        'death_rate_dict' : death_rate_dict
     } 

    if request.user_agent.is_mobile:
        return render(request, 'trends-index-mobile.html', context)
    else:
        return render(request, 'trends-index.html', context)

def localGovUpdate(request):
    context = {}
    return render(request, 'local-gov-update.html', context)