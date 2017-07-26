# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
	def registerVal(self, postData):
		results = {
			'status': True,
			'errors': [],
		}
		user = []
		if not postData['name'] or len(postData['name']) < 4:
			results['status'] = False
			results['errors'].append('Name must be at least 3 characters!')
		if not postData['username'] or len(postData['username']) < 4:
			results['status'] = False
			results['errors'].append('Username must be at least 3 characters!')
		if not postData['email'] or not re.match(r"[^@]+@[^@]+\.[^@]+",postData['email']):
			results['status'] = False
			results['errors'].append('Email is not valid!')
		if not postData['password'] or len(postData['password']) < 8 or postData['password'] != postData['c_password']:
			results['status'] = False
			results['errors'].append('Password is not valid!')
		# if true so far, try to get the user from the db by email
		if results['status'] == True:
			user = User.objects.filter(email=postData['email'])
		# if something came back, that email is already in use - throw an error
		if len(user) != 0:
			results['status'] = False
			results['errors'].append('User already exists!')
		return results
	def loginVal(self, postData):
		results = {
			'status':True,
			'errors':[],
			'user':None,
		}
		if len(postData['username']) < 3:
			results['errors'].append('Uh-oh! Please check your credentials and try again!')
		else:
			user = User.objects.filter(username=postData['username'])
			if len(user) <= 0:
				results['status'] = False
				results['errors'].append('Uh-oh! Please check your credentials and try again!')
				return results
			hashed = bcrypt.hashpw(postData['password'].encode(), user[0].password.encode())
			if hashed != user[0].password:
				results['status'] = False
				results['errors'].append('Uh-oh! Please check your credentials and try again!')
			else:
				results['user'] = user[0]
			return results
	# def getLatest(self):
	# 	users = User.objects.all().order_by('-created_at')
	# 	latest = []
	# 	for i in range(0,3):
	# 		try:
	# 			latest.append(users[i])
	# 		except:
	# 			pass
	# 	return latest

class User(models.Model):
	# f_name = models.CharField(max_length = 40)
	# l_name = models.CharField(max_length = 40)
	name = models.CharField(max_length = 40)
	username = models.CharField(max_length = 40)
	email = models.CharField(max_length = 40)
	password = models.CharField(max_length = 40)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = UserManager()