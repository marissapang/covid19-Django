from django.shortcuts import render
from django import forms
import pandas as pd
from .forms import UpdateDashboardCountryForm, UpdateDashboardStateForm, UpdateDashboardCountryFormMobile, UpdateDashboardStateFormMobile, UpdateDashboardDateRangeForm
from django.contrib.auth.models import User
from .models import Profile
import ast
from datetime import datetime, timedelta

def index(request):
	user = request.user.pk
	current_profile = Profile.objects.get(user=user) if request.user.is_authenticated else None

	default_country_selections = ['Global', 'United States']
	default_state_selections = ['New York']

	##### POP-UP COUNTRY FORM STARTS #####
	if request.method == "POST":
		dashboard_country_filter_form = UpdateDashboardCountryForm(request.POST)
		if dashboard_country_filter_form.is_valid():
			country_selections = dashboard_country_filter_form.cleaned_data.get('countries') # this is a list object
			if request.user.is_authenticated: # add selection to user's profile
				current_profile.dashboard_countries = str(country_selections)
				current_profile.save() # save changes to profie attribute
			else: # if not logged in just save to session
				request.session['countries'] = country_selections
		else: 
			if request.user.is_authenticated:
				country_selections = ast.literal_eval(current_profile.dashboard_countries)
				current_profile.dashboard_countries = str(country_selections)
				current_profile.save() # save changes to profie attribute
			else: 
				country_selections = request.session.get('countries') 
				country_selections = default_country_selections if country_selections is None else country_selections
			if request.user_agent.is_mobile:
				dashboard_country_filter_form = UpdateDashboardCountryFormMobile(initial={'countries': country_selections})
			else: 
				dashboard_country_filter_form = UpdateDashboardCountryForm(initial={'countries': country_selections})		
	
	else: # if method is not post we just have to generate the form
		if request.user.is_authenticated:
			country_selections = ast.literal_eval(current_profile.dashboard_countries)
		else: 
			country_selections = request.session.get('countries') 
			country_selections = default_country_selections if country_selections is None else country_selections
		if request.user_agent.is_mobile:
			dashboard_country_filter_form = UpdateDashboardCountryFormMobile(initial={'countries': country_selections})
		else: 
			dashboard_country_filter_form = UpdateDashboardCountryForm(initial={'countries': country_selections})		
	

	##### POP-UP COUNTRY FORM ENDS #####

	##### POP-UP STATE FORM STARTS #####
	if request.method == "POST":
		dashboard_state_filter_form = UpdateDashboardStateForm(request.POST)
		if dashboard_state_filter_form.is_valid():
			state_selections = dashboard_state_filter_form.cleaned_data.get('states') # this is a list object
			if request.user.is_authenticated: # add selection to user's profile
				current_profile.dashboard_states = str(state_selections)
				current_profile.save() # save changes to profie attribute
			else: 
				request.session['states'] = state_selections
		else: 
			if request.user.is_authenticated:
				state_selections = ast.literal_eval(current_profile.dashboard_states)
				current_profile.dashboard_states = str(state_selections)
				current_profile.save() # save changes to profie attribute
			else:
				state_selections = request.session.get('states')
				state_selections = default_state_selections if state_selections is None else state_selections

			if request.user_agent.is_mobile:
				dashboard_state_filter_form = UpdateDashboardStateFormMobile(initial={'states':state_selections})
			else:
				dashboard_state_filter_form = UpdateDashboardStateForm(initial={'states':state_selections})

	else: # if method is not post we just have to generate the form
		if request.user.is_authenticated:
			state_selections = ast.literal_eval(current_profile.dashboard_states)
		else: 
			state_selections = request.session.get('states') 
			state_selections = default_state_selections if state_selections is None else state_selections

		if request.user_agent.is_mobile:
			dashboard_state_filter_form = UpdateDashboardStateFormMobile(initial={'states':state_selections})
		else:
			dashboard_state_filter_form = UpdateDashboardStateForm(initial={'states':state_selections})

	##### POP-UP STATE FORM ENDS #####

	

	if request.method == "POST":
		dashboard_date_range_form = UpdateDashboardDateRangeForm(request.POST)
		if dashboard_date_range_form.is_valid():
			date_range = dashboard_date_range_form.cleaned_data.get('date_range')
			request.session['date_range'] = date_range
		else: 
			date_range = request.session.get('date_range')
			date_range = "All time" if date_range is None else date_range
			dashboard_date_range_form = UpdateDashboardDateRangeForm(initial={'date_range': date_range})
	else: 
		date_range = request.session.get('date_range')
		date_range = "All time" if date_range is None else date_range
		dashboard_date_range_form = UpdateDashboardDateRangeForm(initial={'date_range': date_range})

	date_range = request.session.get('date_range')

	##### DATA SERIES STARTS #####
	df_confirmed = pd.read_csv("trends/data/confirmed_cases.csv")
	df_deaths = pd.read_csv("trends/data/num_deaths.csv")

	latest_date = datetime.strptime(max(df_confirmed['Date']), '%Y-%m-%d')

	days = timedelta(1000) # set high number of days to subtract if it's all time
	if date_range == "Past 2 months":
		days = timedelta(61)
	elif date_range == "Past month":
		days = timedelta(31)
	elif date_range == "Past 2 weeks":
		days = timedelta(15)

	start_date = latest_date - days

	latest_date = latest_date.strftime("%Y-%m-%d")
	start_date = start_date.strftime("%Y-%m-%d")

	print("Before filtering")
	#print("Num rows:", df_confirmed.count())
	print("Max date:", max(df_confirmed['Date']))
	print("Min date:", min(df_confirmed['Date']))

	df_confirmed = df_confirmed[df_confirmed['Date']>start_date]

	print("After filtering")
	#print("Num rows:", df_confirmed.count())
	print("Max date:", max(df_confirmed['Date']))
	print("Min date:", min(df_confirmed['Date']))


	country_selections = [i for i in country_selections if i != "None"]
	state_selections = [i for i in state_selections if i != "None"]

	region_dict = {i : "country" for i in country_selections}
	state_dict = {i : "state" for i in state_selections}
	region_dict.update(state_dict) #created dicitionary of region names and whether they're countries or states
	region_selections = country_selections + state_selections
	
	dates = list(df_confirmed['Date'].unique())
	output_confirmed_df = pd.DataFrame(dates, columns=["Date"])
	output_deaths_df = pd.DataFrame(dates, columns=["Date"])
	
	for region_name, region_type in region_dict.items(): 
		if region_name == "Global":
			region_confirmed_data = df_confirmed
			region_deaths_data = df_deaths
		elif region_type == "country":
			region_confirmed_data = df_confirmed[df_confirmed['Country']==region_name]
			region_deaths_data = df_deaths[df_deaths['Country']==region_name]
		elif region_type == "state":
			region_confirmed_data = df_confirmed[df_confirmed['State']==region_name]
			region_deaths_data = df_deaths[df_deaths['State']==region_name]

		region_confirmed_data = region_confirmed_data.groupby(['Date'])["Num_Confirmed"].agg("sum").reset_index(name="Num_Confirmed")
		region_confirmed_data = region_confirmed_data.fillna(0)
		region_confirmed_data = region_confirmed_data.rename(columns={"Num_Confirmed" : region_name})
		output_confirmed_df = output_confirmed_df.merge(region_confirmed_data, on="Date", how="left")

		region_deaths_data = region_deaths_data.groupby(['Date'])["Num_Deaths"].agg("sum").reset_index(name="Num_Deaths")
		region_deaths_data = region_deaths_data.fillna(0)
		region_deaths_data = region_deaths_data.rename(columns={"Num_Deaths" : region_name})
		output_deaths_df = output_deaths_df.merge(region_deaths_data, on="Date", how="left")

	output_region_names = []
	output_data_list_confirmed = []
	output_data_list_deaths = []

	for i in range(0, 12):
		if len(region_dict) > i:
			output_region_names += [list(region_dict.keys())[i]]
			output_data_list_confirmed += [list(output_confirmed_df[list(region_dict.keys())[i]])]
			output_data_list_deaths += [list(output_deaths_df[list(region_dict.keys())[i]])]
		else:
			output_region_names += [['']]
			output_data_list_confirmed += [[]]
			output_data_list_deaths += [[]]
	##### DATA SERIES ENDS #####	

	context={
		'tab' : 'dashboard',
		'dashboard_country_filter_form' : dashboard_country_filter_form,
		'dashboard_state_filter_form' : dashboard_state_filter_form,
		'dashboard_date_range_form' :  dashboard_date_range_form,
		"dates": dates,
		"output_data_list_confirmed": output_data_list_confirmed,
		"output_data_list_deaths" : output_data_list_deaths,
		"output_region_names": output_region_names
	}

	return render(request, 'dashboard-index.html', context)
	


