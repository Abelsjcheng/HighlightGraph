from django.shortcuts import render
from django.http import HttpResponse
import json
import time

from backend import models

# Create your views here.


def register(request):
	if request.method == 'POST':
		params = json.loads(request.body)
		print(params)
		if not request.COOKIES.get('current_user'):
			try:
				models.Username.objects.create(username=params['name'], education=params['education'], age=params['age'], sex=params['sex'], research=params['research'], background=params['background'])
				response = HttpResponse("OK")
				response.set_cookie('current_user', params['name'].encode('utf-8').decode('latin-1'))
				print(response)
				return response
			except :
				return HttpResponse("fail")
		return HttpResponse('signin')


def saveRect(request):
	if request.method == 'POST':
		params = json.loads(request.body)
		# print(params)
		try:
			username = models.Username.objects.get(username=request.COOKIES.get('current_user').encode('latin-1').decode('utf-8'))
			models.Rectangle.objects.create(time=params['time'], name=params['name'], x1=params['x1'], y1=params['y1'], x2=params['x2'], y2=params['y2'], username=username)
			return HttpResponse(json.dumps({'state': 'success'}), content_type='application/json')
		except:
			return HttpResponse(json.dumps({'state': 'fail'}), content_type='application/json')


def saveDuration(request):
	if request.method == 'POST':
		params = json.loads(request.body)

		try:
			# now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())) 
			username = models.Username.objects.get(username=request.COOKIES.get('current_user').encode('latin-1').decode('utf-8'))
			print(params)
			models.Duration.objects.create(time=params['time'], name=params['name'], consumingtime=params['consumingtime'], username=username, qid=params['qid'], TestType=params['TestType'])
			return HttpResponse(json.dumps({'state': 'success'}), content_type='application/json')
		except:
			return HttpResponse(json.dumps({'state': 'fail'}), content_type='application/json')

def readRect(request):
	if request.method == 'POST':
		params = json.loads(request.body)
		print(params)
		username = models.Username.objects.get(username=request.COOKIES.get('current_user').encode('latin-1').decode('utf-8'))
		filter_data = models.Rectangle.objects.filter(name=params['name'], username_id=username).values()
		print(username)
		print(filter_data)
		#filter_data = models.Rectangle.objects.filter(name=params['name']).values()
		return HttpResponse(json.dumps({'datum': list(filter_data)}), content_type='application/json')

def signout(request):
	response = HttpResponse('OK')
	response.delete_cookie('current_user')
	return response

def isLogged(request):
	current_user = request.COOKIES.get('current_user')
	if current_user:
		return HttpResponse('log_in')
	else:
		return HttpResponse('not_log_in')


def getQuestions(request):
	if request.method == 'POST':
		params = json.loads(request.body)
		print(params)
		background = params['background']
		filter_data = models.Questions.objects.filter(name=params['name'], background=background, TestType=params['TestType']).values().order_by("qid")
		if background == '1':
			graphbackground = models.Background.objects.filter(name=params['name']).values()
			print(graphbackground)
		else:
			graphbackground = [{'background': '无背景信息'}]
		return HttpResponse(json.dumps({'datum': list(filter_data), 'graphbackground': list(graphbackground)}), content_type='application/json')


def saveanswer(request):
	if request.method == 'POST':
		params = json.loads(request.body)
		try:
			qid = models.Questions.objects.get(qid=params['qid'])
			username = models.Username.objects.get(username=request.COOKIES.get('current_user').encode('latin-1').decode('utf-8'))
			print(params)
			models.Answers.objects.create(time=params['time'], name=params['name'], answer=params['answer'], x1=params['x1'], y1=params['y1'], x2=params['x2'], y2=params['y2'], qid=qid, consumingtime=params['consumingtime'], username=username, TestType=params['TestType'])
			return HttpResponse(json.dumps({'state': 'success'}), content_type='application/json')
		except:
			return HttpResponse(json.dumps({'state': 'fail'}), content_type='application/json')


def getBackground(request):
	if request.method == 'POST':
		params = json.loads(request.body)
		print(params)
		graphbackground = models.Background.objects.filter(name=params['name']).values()
		return HttpResponse(json.dumps({'datum':  list(graphbackground)}), content_type='application/json')
