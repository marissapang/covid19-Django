from django.shortcuts import render

def index(request):
	test = 1234
	context = {'test_variable': test}
	return render(request, 'dashboard-index.html', context)


