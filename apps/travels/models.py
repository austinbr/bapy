# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from ..users.models import User
import datetime

# Create your models here.
class DestinationManager(models.Manager):
	def destinationVal(self, postData, seshID):
		results = {
			'status': True,
			'errors': [],
		}
		destDict = {
			'destination':None,
			'description':None,
			'datefrom':None,
			'dateto':None,
			'created_by':None,
		}
		datenow = datetime.datetime.today()
		if not postData['destination']:
			results['status'] = False
			results['errors'].append('Empty Field Error!')
		if not postData['description']:
			results['status'] = False
			results['errors'].append('Empty Field Error!')
		if not postData['datefrom']:
			results['status'] = False
			results['errors'].append('Empty Field Error!')
		if not postData['dateto']:
			results['status'] = False
			results['errors'].append('Empty Field Error!')
		# empty checks passed, now check date values
		dateto = datetime.datetime.strptime(postData['dateto'], '%Y-%m-%d')
		datefrom = datetime.datetime.strptime(postData['datefrom'], '%Y-%m-%d')
		if dateto <= datenow:
			results['status'] = False
			results['errors'].append('Error! to <= now')
		if datefrom <= datenow:
			results['status'] = False
			results['errors'].append('Error! from <= now')
		if dateto <= datefrom:
			results['status'] = False
			results['errors'].append('Error! from <= to')
		if results['status'] == True:
			results['errors'].append('Trip added!')
			destDict['destination'] = postData['destination']
			destDict['description'] = postData['description']
			destDict['datefrom'] = datefrom
			destDict['dateto'] = dateto
			destDict['created_by'] = User.objects.get(id=seshID)
			newDest = Destination.objects.create(**destDict)
		return results

class FellowManager(models.Manager):
	def addFellow(self):
		return True
	def getFellows(self):
		return True

class Destination(models.Model):
	destination = models.CharField(max_length = 100)
	description = models.CharField(max_length = 255)
	datefrom = models.DateTimeField()
	dateto = models.DateTimeField()
	created_by = models.ForeignKey(User, related_name='created_by')
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = DestinationManager()

class FellowTraveller(models.Model):
	fellowdestination = models.ForeignKey(Destination, related_name='fellowdestination')
	fellowtraveller = models.ForeignKey(User, related_name='fellowtraveller')
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = FellowManager()