# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from models import User
import bcrypt

# Create your views here.
def index(request):
	request.session.flush()
	request.session['userID'] = None
	request.session['isLogged'] = False
	return render(request, 'users/index.html')

def register(request):
	results = User.objects.registerVal(request.POST)
	if results['status'] == False:
		for error in results['errors']:
			messages.error(request, error)
	else:
		p_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
		userDict = {
			'name':request.POST['name'], 
			'username':request.POST['username'], 
			'email':request.POST['email'], 
			'password':p_hash,
		}
		user = User.objects.create(**userDict)
		messages.success(request, 'User has been created! Please log in.')
	return redirect('/')

def login(request):
	results = User.objects.loginVal(request.POST)
	if results['status'] == False:
		for error in results['errors']:
			messages.error(request, error)
		return redirect('/')
	else:
		request.session['userID'] = results['user'].id
		request.session['isLogged'] = True
		return redirect('/travels') 