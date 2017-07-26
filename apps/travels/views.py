# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
from models import Destination, FellowTraveller
from ..users.models import User

# Create your views here.
def dashboard(request):
	if request.session['isLogged'] == True:
		context = {
			'destinations':[],
			'otherdestinations':[],
			'curruser':None,
		}
		context['curruser'] = User.objects.get(id=request.session['userID']).name
		theD = Destination.objects.filter(created_by=request.session['userID'])
		for d in theD:
			context['destinations'].append(d)
		theF = FellowTraveller.objects.filter(fellowtraveller=request.session['userID'])
		for f in theF:
			place = Destination.objects.get(id=int(f.fellowdestination.id))
			context['destinations'].append(place)
		theOD = Destination.objects.exclude(created_by=request.session['userID'])
		for od in theOD:
			if od in context['destinations']:
				pass
			else:
				context['otherdestinations'].append(od)
		return render(request, 'travels/dashboard.html', context)
	else:
		messages.error(request, 'Please login!')
		return redirect('/')

def travelAdd(request):
	if request.session['isLogged'] == True:
		return render(request, 'travels/add.html')
	else:
		messages.error(request, 'Please login!')
		return redirect('/')

def travelProcess(request):
	if request.session['isLogged'] == True:
		Destination.objects.destinationVal(request.POST, request.session['userID'])
		return redirect('/travels')
	else:
		messages.error(request, 'Please login!')
		return redirect('/')

def joinProcess(request, id):
	if request.session['isLogged'] == True:
		joinDict = {
			'fellowdestination':None,
			'fellowtraveller':None,
		}
		joinDict['fellowdestination'] = Destination.objects.get(id=id) 
		joinDict['fellowtraveller'] = User.objects.get(id=request.session['userID'])
		try:
			FellowTraveller.objects.get(**joinDict)
			return redirect('/travels')
		except:
			FellowTraveller.objects.create(**joinDict)
			return redirect('/travels')
	else:
		messages.error(request, 'Please login!')
		return redirect('/')

def showDest(request, id):
	if request.session['isLogged'] == True:
		context = {
			'destination':None,
			'description':None,
			'datefrom':None,
			'dateto':None,
			'created_by':None,
			'fellows':[],
		}
		dest = Destination.objects.get(id=id)
		context['destination'] = dest.destination
		context['description'] = dest.description
		context['datefrom'] = dest.datefrom
		context['dateto'] = dest.dateto
		context['created_by'] = dest.created_by.name
		fellows = FellowTraveller.objects.filter(fellowdestination=dest)
		for fellow in fellows:
			context['fellows'].append(fellow)
		return render(request, 'travels/destination.html', context)
	else:
		messages.error(request, 'Please login!')
		return redirect('/')