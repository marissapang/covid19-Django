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
				if country_selections == ['None']:
					country_selections = []
				current_profile.dashboard_countries = str(country_selections)
				current_profile.save() # save changes to profie attribute
			else: 
				country_selections = ast.literal_eval(current_profile.dashboard_countries)
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
				if state_selections == ['None']:
					state_selections = []
				# add state selections to the username's dictionary
				current_profile.dashboard_states = str(state_selections)
				current_profile.save() # save changes to profie attribute
			else: 
				state_selections = ast.literal_eval(current_profile.dashboard_states)
				current_profile.dashboard_states = str(state_selections)
				current_profile.save() # save changes to profie attribute
		else: # if method is not post we just have to generate the form
			state_selections = ast.literal_eval(current_profile.dashboard_states)
			dashboard_state_filter_form = UpdateDashboardStateForm(initial={'states':state_selections})
		##### POP-UP STATE FORM ENDS #####


		##### COUNTRY DATA SERIES STARTS #####
		country_dict = {i : "country" for i in country_selections}
		state_dict = {i : "state" for i in state_selections}
		country_dict.update(state_dict)
		region_dict = country_dict #created dicitionary of region names and whether they're countries or states
		region_selections = country_selections + state_selections
		
		df = pd.read_csv("trends/data/confirmed_cases.csv")
		dates = list(df['Date'].unique())
		output_df = pd.DataFrame(dates, columns=["Date"])
		output_dict = {}
		output_region_list = []
		

		for region_name, region_type in region_dict.items(): 
			if region_name == "Global":
				region_data = df
			elif region_type == "country":
				region_data = df[df['Country']==region_name]
			elif region_type == "state":
				region_data = df[df['State']==region_name]
			else:
				region_data="ERROR"

			region_data = region_data.groupby(['Date'])["Num_Confirmed"].agg("sum").reset_index(name="Num_Confirmed")
			region_data = region_data.fillna(0)
			region_data = region_data.rename(columns={"Num_Confirmed" : region_name})
			output_df = output_df.merge(region_data, on="Date", how="left")


		for i in range(0, 12):
			if len(region_dict) > i:
				key = "region_"+str(i) 
				output_dict[key] = list(output_df[region_selections[i]])
				output_region_list += [[region_selections[i]]]
			else:
				key = "region_"+str(i) 
				output_dict[key] = []
				output_region_list += [[""]]
		# ##### COUNTRY DATA SERIES ENDS #####	

		context={
			'tab' : 'dashboard',
			'dashboard_country_filter_form' : dashboard_country_filter_form,
			'dashboard_state_filter_form' : dashboard_state_filter_form,
			"dates": dates,
			"region_1": output_dict['region_0'],
			"region_2": output_dict['region_1'],
			"region_3": output_dict['region_2'],
			"region_4": output_dict['region_3'],
			"region_5": output_dict['region_4'],
			"region_6": output_dict['region_5'],
			"region_7": output_dict['region_6'],
			"region_8": output_dict['region_7'],
			"region_9": output_dict['region_8'],
			"region_10": output_dict['region_9'],
			"region_11": output_dict['region_10'],
			"region_12": output_dict['region_11'],
			"region_1_name": output_region_list[0],
			"region_2_name": output_region_list[1],
			"region_3_name": output_region_list[2],
			"region_4_name": output_region_list[3],
			"region_5_name": output_region_list[4],
			"region_6_name": output_region_list[5],
			"region_7_name": output_region_list[6],
			"region_8_name": output_region_list[7],
			"region_9_name": output_region_list[8],
			"region_10_name": output_region_list[9],
			"region_11_name": output_region_list[10],
			"region_12_name": output_region_list[11],
		}


	else: # if user is not logged in we show nothing
		context = {}

	return render(request, 'dashboard-index.html', context)
	


