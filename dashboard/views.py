from django.shortcuts import render
import pandas as pd
from .forms import UpdateDashboardCountryForm, UpdateDashboardStateForm
from django.contrib.auth.models import User
from .models import Profile
import ast

def index(request):
	if request.user.is_authenticated == True: # we only show content if the user is logged in
		username = request.user.username
		user = request.user.pk

		current_profile = Profile.objects.get(user=user)

		#country_selections = current_profile.dashboard_countries
		

		##### POP-UP COUNTRY FORM STARTS #####
		if request.method == "POST":
			dashboard_country_filter_form = UpdateDashboardCountryForm(request.POST)
			if dashboard_country_filter_form.is_valid():
				country_selections = dashboard_country_filter_form.cleaned_data.get('countries') # this is a list object
				# add country selections to the username's dictionary
				current_profile.dashboard_countries = str(country_selections)
				current_profile.save() # save changes to profie attribute
			else: 
				country_selections = []
				current_profile.dashboard_countries = str(country_selections)
				current_profile.save() # save changes to profie attribute
		else: # if method is not post we just have to generate the form
			country_selections = ast.literal_eval(current_profile.dashboard_countries)
			dashboard_country_filter_form = UpdateDashboardCountryForm(initial={'countries': country_selections})		
		##### POP-UP COUNTRY FORM ENDS #####


		##### POP-UP STATE FORM STARTS #####
		if request.method == "POST":
			dashboard_state_filter_form = UpdateDashboardStateForm(request.POST)
			if dashboard_state_filter_form.is_valid():
				state_selections = dashboard_state_filter_form.cleaned_data.get('states') # this is a list object
				print(state_selections)
				# add state selections to the username's dictionary
				current_profile.dashboard_states = str(state_selections)
				current_profile.save() # save changes to profie attribute
			else: 
				state_selections = []
				current_profile.dashboard_states = str(state_selections)
				current_profile.save() # save changes to profie attribute
		else: # if method is not post we just have to generate the form
			state_selections = ast.literal_eval(current_profile.dashboard_states)
			dashboard_state_filter_form = UpdateDashboardStateForm(initial={'states':state_selections})
		##### POP-UP STATE FORM ENDS #####


		##### COUNTRY DATA SERIES STARTS #####
		df = pd.read_csv("trends/data/confirmed_cases.csv")
		dates = list(df['Date'].unique())
		output_df = pd.DataFrame(dates, columns=["Date"])

		for country in country_selections: 

			if country != "Global": # filter to get country-level data
				country_data = df[df['Country']==country]
			else: 
				country_data = df

			country_data = country_data.groupby(['Date'])["Num_Confirmed"].agg("sum").reset_index(name="Num_Confirmed")
			country_data = country_data.fillna(0)
			country_data = country_data.rename(columns={"Num_Confirmed" : country})
			output_df = output_df.merge(country_data, on="Date", how="left")

		output_dict = {}
		output_country_list = []


		for i in range(0, 6):
			if len(country_selections) > i:
				key = "country_"+str(i) 
				output_dict[key] = list(output_df[country_selections[i]])
				output_country_list += [[country_selections[i]]]
			else:
				key = "country_"+str(i) 
				output_dict[key] = []
				output_country_list += [[""]]
		##### COUNTRY DATA SERIES ENDS #####


		##### STATE DATA SERIES STARTS #####
		df = pd.read_csv("trends/data/confirmed_cases.csv")
		dates = list(df['Date'].unique())
		output_df = pd.DataFrame(dates, columns=["Date"])

		for state in state_selections: 
			state_data = df[df['State']==state]

			state_data = state_data.groupby(['Date'])["Num_Confirmed"].agg("sum").reset_index(name="Num_Confirmed")
			state_data = state_data.fillna(0)
			state_data = state_data.rename(columns={"Num_Confirmed" : state})
			output_df = output_df.merge(state_data, on="Date", how="left")

		output_state_list = []

		for i in range(0, 6):
			if len(state_selections) > i:
				key = "state_"+str(i) 
				output_dict[key] = list(output_df[state_selections[i]])
				output_state_list += [[state_selections[i]]]
			else:
				key = "state_"+str(i) 
				output_dict[key] = []
				output_state_list += [[""]]

		print(output_state_list)


		##### STATE DATA SERIES ENDS #####

		context={
			'tab' : 'dashboard',
			'dashboard_country_filter_form' : dashboard_country_filter_form,
			'dashboard_state_filter_form' : dashboard_state_filter_form,
			"dates": dates,
			"country_1": output_dict['country_0'],
			"country_2": output_dict['country_1'],
			"country_3": output_dict['country_2'],
			"country_4": output_dict['country_3'],
			"country_5": output_dict['country_4'],
			"country_6": output_dict['country_5'],
            "country_1_name": output_country_list[0],
            "country_2_name": output_country_list[1],
            "country_3_name": output_country_list[2],
            "country_4_name": output_country_list[3],
            "country_5_name": output_country_list[4],
            "country_6_name": output_country_list[5],
            "state_1": output_dict['state_0'],
            "state_2": output_dict['state_1'],
            "state_3": output_dict['state_2'],
            "state_4": output_dict['state_3'],
            "state_5": output_dict['state_4'],
            "state_6": output_dict['state_5'],
            "state_1_name": output_state_list[0],
            "state_2_name": output_state_list[1],
            "state_3_name": output_state_list[2],
            "state_4_name": output_state_list[3],
            "state_5_name": output_state_list[4],
            "state_6_name": output_state_list[5],
		}

		#print(context)

	else: # if user is not logged in we show nothing
		context = {}

	return render(request, 'dashboard-index.html', context)
	


