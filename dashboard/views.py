from django.shortcuts import render
import pandas as pd
from .forms import UpdateDashboardCountryForm

df = pd.read_csv("trends/data/confirmed_cases.csv")
df = df.groupby('Country').agg("sum")
unique_countries = df.index
country_choices = list(zip(unique_countries, unique_countries))
country_choices = [('Global','Global')]+country_choices

def index(request):
	if request.user.is_authenticated == True: # we only show content if the user is logged in
		print("first if for authentication")
		username = request.user.username

		##### POP UP FORM #####
		#dashboard_country_filter_form = UpdateDashboardCountryForm()
		if request.method == "POST":
			print("request method is post")
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
			print("request method is not post")
			country_selections = request.session.get(username)['country_selections']
			print("non post country selections")
			print(country_selections)
			dashboard_country_filter_form = UpdateDashboardCountryForm(initial={'countries': country_selections})		
		
		context={'dashboard_country_filter_form' : dashboard_country_filter_form, 'test_list' : ["Global", "Burma"]}
	


	else: # if user is not logged in we show nothing
		context = {}

	return render(request, 'dashboard-index.html', context)
	


