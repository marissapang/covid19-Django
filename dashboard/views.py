from django.shortcuts import render
from django import forms
import pandas as pd
from .forms import UpdateDashboardForm, UpdateDashboardFormMobile, SummStatFilterForm, SummStatFilterFormMobile, DataTypeForm
from django.contrib.auth.models import User
from .models import Profile
import ast
from datetime import datetime, timedelta


def index(request):
	user = request.user.pk
	current_profile = Profile.objects.get(user=user) if request.user.is_authenticated else None

	default_country_selections = ['Global', 'United States']
	default_state_selections = ['New York']
	default_date_range = 'All time'

	if request.method == "POST":
		dashboard_form = UpdateDashboardForm(request.POST)
		if dashboard_form.is_valid():
			country_selections = dashboard_form.cleaned_data.get('countries') # this is a list object
			state_selections = dashboard_form.cleaned_data.get('states') # this is a list object
			date_range = dashboard_form.cleaned_data.get('date_range') # this is a string object

			if not request.user_agent.is_mobile:
				if 'country_select_save' in request.POST:
					country_selections = dashboard_form.cleaned_data.get('countries')
					if request.user.is_authenticated: # if user is signed in then we save changes to profile
						current_profile.dashboard_countries = str(country_selections)
						current_profile.save()
					else: 
						request.session['countries'] = country_selections
				elif 'state_select_save' in request.POST:
					state_selections = dashboard_form.cleaned_data.get('states')
					if request.user.is_authenticated: # if user is signed in then we save changes to profile
						current_profile.dashboard_states = str(state_selections)
						current_profile.save()
					else: 
						request.session['states'] = state_selections
			else: # if using mobile interface we only have one submit button for country and state
				if 'region_select_save' in request.POST:
					country_selections = dashboard_form.cleaned_data.get('countries')
					state_selections = dashboard_form.cleaned_data.get('states')

					if request.user.is_authenticated:
						current_profile.dashboard_countries = str(country_selections)
						current_profile.dashboard_states = str(state_selections)
						current_profile.save()
					else: 
						request.session['countries'] = country_selections
						request.session['states'] = state_selections
			
			date_range = dashboard_form.cleaned_data.get('date_range')
			if date_range != "":
				if request.user.is_authenticated: # if user is signed in then we save changes to profile
					current_profile.dashboard_date_range = str(date_range)
					current_profile.save()
				else: 
					request.session['date_range'] = date_range

			if request.user.is_authenticated:
				country_selections = ast.literal_eval(current_profile.dashboard_countries)
				state_selections = ast.literal_eval(current_profile.dashboard_states)
				date_range = current_profile.dashboard_date_range
			else: 
				country_selections = request.session.get('countries')
				state_selections = request.session.get('states')
				date_range = request.session.get('date_range')
			country_selections = default_country_selections if country_selections is None else country_selections
			state_selections = default_state_selections if state_selections is None else state_selections
			date_range = default_date_range if date_range is None else date_range
	else: # if request method is not post, just generate the form
		if request.user.is_authenticated: # use saved DB settings in profile
			country_selections = ast.literal_eval(current_profile.dashboard_countries)
			state_selections = ast.literal_eval(current_profile.dashboard_states)
			date_range = current_profile.dashboard_date_range
		else: # if no profile use session data
			country_selections = request.session.get('countries')
			country_selections = default_country_selections if country_selections is None else country_selections
			state_selections = request.session.get('states')
			state_selections = default_state_selections if state_selections is None else state_selections
			date_range = request.session.get('date_range')
			date_range = default_date_range if date_range is None else date_range
	initial_form_values = {'countries':country_selections, 'states':state_selections, 'date_range':date_range}
	dashboard_form = UpdateDashboardFormMobile(initial = initial_form_values) if request.user_agent.is_mobile else UpdateDashboardForm(initial = initial_form_values)


	##### SUMM STATS STARTS #####
	df_confirmed = pd.read_csv("trends/data/confirmed_cases.csv")
	df_deaths = pd.read_csv("trends/data/num_deaths.csv")

	if request.user_agent.is_mobile: 
		summ_filter_form = SummStatFilterFormMobile(request.POST)
	else: 
		summ_filter_form = SummStatFilterForm(request.POST)


	if summ_filter_form.is_valid():
		country = summ_filter_form.cleaned_data.get('country')
		country = "Global" if country=="" or country=="None" else country
		request.session['country'] = country	
	else: 
		country = request.session.get('country')
		country = "Global" if country is None else country

	if request.user_agent.is_mobile: 
		summ_stat_filter_form = SummStatFilterFormMobile(initial = {'country': country})
	else: 
		summ_stat_filter_form = SummStatFilterForm(initial = {'country': country})

	summ_filter_country = country

	if country != "Global":
		df_confirmed = df_confirmed[df_confirmed['Country']==country]
		df_deaths = df_deaths[df_deaths['Country']==country]




	# find yesterday's date
	yesterday_confirmed = datetime.strptime(max(df_confirmed['Date']), '%Y-%m-%d') - timedelta(1)
	yesterday_confirmed = yesterday_confirmed.strftime("%Y-%m-%d")
	yesterday_deaths = datetime.strptime(max(df_deaths['Date']), '%Y-%m-%d') - timedelta(1)
	yesterday_deaths = yesterday_deaths.strftime("%Y-%m-%d")

	# find latest + T-1 day numbers
	confirmed_summ_stat = df_confirmed[df_confirmed['Date'] == max(df_confirmed['Date'])].Num_Confirmed.sum()
	deaths_summ_stat = df_deaths[df_deaths['Date'] == max(df_deaths['Date'])].Num_Deaths.sum()
	yesterday_confirmed_summ_stat = df_confirmed[df_confirmed['Date'] == yesterday_confirmed].Num_Confirmed.sum()
	yesterday_deaths_summ_stat = df_deaths[df_deaths['Date'] == yesterday_deaths].Num_Deaths.sum()

	# calculate increment numbers
	incr_confirmed = confirmed_summ_stat - yesterday_confirmed_summ_stat
	incr_deaths = deaths_summ_stat - yesterday_deaths_summ_stat
	incr_pct_confirmed = round(incr_confirmed/yesterday_confirmed_summ_stat*100,1)
	incr_pct_deaths = round(incr_deaths/yesterday_deaths_summ_stat*100,1)

	confirmed_summ_stat = f"{confirmed_summ_stat:,d}"
	deaths_summ_stat = f"{deaths_summ_stat:,d}"
	incr_confirmed = f"{incr_confirmed:,d}"
	incr_deaths = f"{incr_deaths:,d}"

	summ_stats = {
		"confirmed_summ_stat":confirmed_summ_stat, "deaths_summ_stat":deaths_summ_stat,
		"incr_confirmed":incr_confirmed, "incr_deaths":incr_deaths, 
		"incr_pct_confirmed":incr_pct_confirmed, "incr_pct_deaths":incr_pct_deaths
		}
	###### SUMM STATS ENDS ######


	##### DATA SERIES STARTS #####
	df_confirmed = pd.read_csv("trends/data/confirmed_cases.csv")
	df_deaths = pd.read_csv("trends/data/num_deaths.csv")

	latest_date = datetime.strptime(max(df_confirmed['Date']), '%Y-%m-%d')

	days = timedelta(1000) # set high number of days to subtract if it's all time
	if date_range == "Past 2 months":
		days = timedelta(62)
	elif date_range == "Past month":
		days = timedelta(32)
	elif date_range == "Past 2 weeks":
		days = timedelta(16)

	start_date = latest_date - days

	latest_date = latest_date.strftime("%Y-%m-%d")
	start_date = start_date.strftime("%Y-%m-%d")

	df_confirmed = df_confirmed[df_confirmed['Date']>start_date]

	country_selections = [i for i in country_selections if i != "None"]
	state_selections = [i for i in state_selections if i != "None"]

	region_dict = {i : "country" for i in country_selections}
	state_dict = {i : "state" for i in state_selections}
	region_dict.update(state_dict) #created dicitionary of region names and whether they're countries or states
	region_selections = country_selections + state_selections
	
	dates = list(df_confirmed['Date'].unique())
	dates.pop(0)
	output_confirmed_df = pd.DataFrame(dates, columns=["Date"])
	output_deaths_df = pd.DataFrame(dates, columns=["Date"])

	first_data_type = request.session.get('data_type')

	if request.method=="POST":
		data_type_form = DataTypeForm(request.POST)
		if data_type_form.is_valid():
			data_type = data_type_form.cleaned_data.get('data_type')
			request.session['data_type'] = data_type
		else:
			data_type = first_data_type if first_data_type is not None else "Cumulative"
	else:
		data_type = first_data_type if first_data_type is not None else "Cumulative"

	data_type_form = DataTypeForm(initial={"data_type":data_type})

	
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

		region_deaths_data = region_deaths_data.groupby(['Date'])["Num_Deaths"].agg("sum").reset_index(name="Num_Deaths")
		region_deaths_data = region_deaths_data.fillna(0)

		# create incremental data and decide whether or not to use cumulative or incremental data

		if data_type == "Incremental":
				region_confirmed_data['Lag_Num'] = region_confirmed_data['Num_Confirmed'].shift(1)
				region_confirmed_data['Incr_Num'] = region_confirmed_data['Num_Confirmed'] - region_confirmed_data['Lag_Num']
				region_confirmed_data = region_confirmed_data.drop(['Num_Confirmed', 'Lag_Num'], axis=1)
				region_confirmed_data = region_confirmed_data.rename(columns={"Incr_Num" : "Num_Confirmed"})
				
				region_deaths_data['Lag_Num'] = region_deaths_data['Num_Deaths'].shift(1)
				region_deaths_data['Incr_Num'] = region_deaths_data['Num_Deaths'] - region_deaths_data['Lag_Num']
				region_deaths_data = region_deaths_data.drop(['Num_Deaths', 'Lag_Num'], axis=1)
				region_deaths_data = region_deaths_data.rename(columns={"Incr_Num" : "Num_Deaths"})


		region_confirmed_data = region_confirmed_data.drop(region_confirmed_data.index[0])
		region_deaths_data = region_deaths_data.drop(region_deaths_data.index[0])

		region_confirmed_data = region_confirmed_data.fillna(0)
		region_deaths_data = region_deaths_data.fillna(0)

		region_confirmed_data = region_confirmed_data.rename(columns={"Num_Confirmed" : region_name})
		region_deaths_data = region_deaths_data.rename(columns={"Num_Deaths" : region_name})

		output_confirmed_df = output_confirmed_df.merge(region_confirmed_data, on="Date", how="left")
		output_deaths_df = output_deaths_df.merge(region_deaths_data, on="Date", how="left")

	output_region_names = []
	output_data_list_confirmed = []
	output_data_list_deaths = []

	for i in range(0, len(region_dict)):
		output_region_names += [list(region_dict.keys())[i]]
		output_data_list_confirmed += [list(output_confirmed_df[list(region_dict.keys())[i]])]
		output_data_list_deaths += [list(output_deaths_df[list(region_dict.keys())[i]])]

	##### DATA SERIES ENDS #####	


	alert_popup = request.session.get('alert_popup') 
	alert_popup = True if alert_popup is None else alert_popup

	if request.GET.get('close_alert'):
		alert_popup = False
		request.session['alert_popup'] = alert_popup

	context={
		'tab' : 'dashboard',
		"dashboard_form" : dashboard_form,
		"dates": dates,
		"output_data_list_confirmed" : output_data_list_confirmed,
		"output_data_list_deaths" : output_data_list_deaths,
		"output_region_names" : output_region_names,
		"summ_stats" : summ_stats,
		"alert_popup" : alert_popup,
		"summ_stat_filter_form" : summ_stat_filter_form,
		"summ_filter_country" : summ_filter_country,
		"data_type_form" : data_type_form,
		"data_type" : [data_type],
	}

	if request.user_agent.is_mobile:
		return render(request, 'dashboard-index-mobile.html', context)
	else: 
		return render(request, 'dashboard-index.html', context)
	


