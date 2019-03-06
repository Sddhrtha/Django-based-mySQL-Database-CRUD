from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .forms import *
from .models import dbNames

from connection import mysqlConnector

# Create your views here.

@login_required
def CreatedbNames (request):

	if request.method == 'POST':
		form = dbForm(request.POST)
		if form.is_valid():
			Details = {
				'Name' : form.cleaned_data['dbName'],
				'Username' : form.cleaned_data['dbUsername'],
				'Password' : form.cleaned_data['dbPassword'],
				'Host' : form.cleaned_data['dbHost'],
				'Port' : form.cleaned_data['dbPort'],
			}

			cnnct = mysqlConnector.Connection(Details)
			if cnnct is False:
				return render(request, 'error.html')
			else:
				form.save()
			return redirect('userCRUD:ReaddbNames')
	else:
		form = dbForm()

	return render(request, 'dbForm.html', {'form' : form}) 

@login_required
def ReaddbNames(request):

	DbNames = dbNames.objects.all()
	return render(request, 'home.html', { 'DbNames' : DbNames })

@login_required
def EditdbNames(request, pk):
	DbName = get_object_or_404(dbNames, pk = pk)
	form = dbForm(instance = DbName)
	return render(request, 'UpdatedbForm.html', { 'form' : form , 'id' : pk })

@login_required
def UpdatedbNames(request, pk):
	DbNames = dbNames.objects.get(id = pk)
	form = dbForm(request.POST, instance = DbNames)

	if form.is_valid():
		Details = {
			'Name' : form.cleaned_data['dbName'],
			'Username' : form.cleaned_data['dbUsername'],
			'Password' : form.cleaned_data['dbPassword'],
			'Host' : form.cleaned_data['dbHost'],
			'Port' : form.cleaned_data['dbPort'],
		}

		cnnct = mysqlConnector.Connection(Details)
		if cnnct is False:
			return render(request, 'error.html')
		else:
			form.save()
			return redirect('userCRUD:ReaddbNames')
	return render(request, 'UpdatedbForm.html', { 'form' : form , 'id' : pk })

@login_required	
def DeletedbNames(request, pk):
	db = get_object_or_404(dbNames, pk = pk)
	db.delete()
	return redirect('userCRUD:ReaddbNames')










