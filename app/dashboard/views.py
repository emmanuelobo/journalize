from django.shortcuts import render


def analytics(request):
	data = {}
	return render(request, 'dashboard/analytics.html', data)


def data(request):
	data = {}
	return render(request, 'dashboard/data.html', data)


def summary(request):
	data = {}
	return render(request, 'dashboard/summary.html', data)


def security(request):
	data = {}
	return render(request, 'dashboard/security.html', data)