from django.shortcuts import render
import pandas as pd
from .forms import UpdateDashboardCountryForm

df = pd.read_csv("trends/data/confirmed_cases.csv")
df = df.groupby('Country').agg("sum")
unique_countries = df.index
country_choices = list(zip(unique_countries, unique_countries))
country_choices = [('Global','Global')]+country_choices

def index(request):
	if request.user.is_authenticated == True:
		username = request.user.username
		# if request.session.has_key(username):
		# 	user_session = requestion.session['username']
		# else: 
		# 	user_session = {}
		# 	countries = request.GET.get('dashboard_country_filter')

		dashboard_country_filter_form = UpdateDashboardCountryForm()

		
		new_list = []
		print(request.session.has_key(username))
		request.session['username'] = new_list
		context={'dashboard_country_filter_form' : dashboard_country_filter_form}
	else:
		context = {}
	return render(request, 'dashboard-index.html', context)
	


