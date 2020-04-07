from django.shortcuts import render
import pandas as pd
from .forms import UpdateDashboardCountryForm

def index(request):
	if request.user.is_authenticated == True: # we only show content if the user is logged in
		username = request.user.username

		##### POP-UP FORM STARTS #####
		if request.method == "POST":
			dashboard_country_filter_form = UpdateDashboardCountryForm(request.POST)
			if dashboard_country_filter_form.is_valid():
				country_selections = dashboard_country_filter_form.cleaned_data.get('countries') # this is a list object
				# add country selections to the username's dictionary
				if request.session.has_key(username): 
					request.session[username]['country_selections'] = country_selections
				else: # if user do not already exists, we can just asign a dictionary object
					request.session[username] = {"country_selections": country_selections}
				request.session.modified = True # save session change
		else: # if method is not post we just have to generate the form
			if request.session.has_key(username):
				print("there is a key for the username")
				print(username)
				country_selections = request.session.get(username)['country_selections']
				if country_selections is None:
					country_selections = ['Global', "United States"]
			else: 
				print("there isnt a key for the username")
				country_selections = ['Global', "United States"]
			dashboard_country_filter_form = UpdateDashboardCountryForm(initial={'countries': country_selections})		
		
		##### POP-UP FORM ENDS #####

		##### DATA SERIES STARTS #####
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


		##### DATA SERIES ENDS #####

		context={
			'tab' : 'dashboard',
			'dashboard_country_filter_form' : dashboard_country_filter_form,
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
            "country_6_name": output_country_list[5]
		}

	else: # if user is not logged in we show nothing
		context = {}

	return render(request, 'dashboard-index.html', context)
	


