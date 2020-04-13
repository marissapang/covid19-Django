from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.urls import reverse

from dashboard.forms import SignUpForm
from dashboard import views as dashboard_views

def signup(request): 
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('/dashboard/')
	else: 
		form = SignUpForm()
	return render(request, 'override_signup.html', {'form': form})


def privacy(request):
	return render(request, 'privacy_policy.html', {})