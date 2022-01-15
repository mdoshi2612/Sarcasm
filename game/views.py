from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.models import User
from .models import Level, BonusQuestion
from users.models import Team
from users.forms import TeamForm
from .forms import LevelForm
from django.shortcuts import redirect
from django.utils import timezone
from django.urls import reverse
# from django.contrib.sites.models import Site	# To get location of current domain
# Create your views here.
def home(request):
	return render(request, 'game/home.html',{})

def error(request):
	return render(request, 'game/error.html',{})

def prize(request):
	return render(request, 'game/prizes.html',{})

def forum(request):
	return render(request, 'game/forum.html',{})

def instructions(request):
	return render(request, 'game/instructions.html',{})


def contacts(request):
	return render(request, 'game/contacts.html',{})

class Play(View) :
	# login_url = '/login/'
	# redirect_field_name = '/register/'
	# redierct_url = '/accounts/facebook/login/callback/'
	# Form field for the level
	form_class = LevelForm


	def get(self, request, *args, **kwargs):
		""" 
		GET Request 
		1. get the current user by the request.user
		2. find their current level and return the question accordingly
		"""

		if not request.user.is_authenticated:
			return redirect('game-home')
		cur_user = User.objects.get(id=request.user.id)
		if not cur_user.player.details_done:
			return redirect('register')
		if not cur_user.player.roll.startswith("2") and cur_user.player.roll not in ['18B080006','180110046','170020010']:
			return redirect('game-home')
		return redirect('game-home') # if cur_user.profile.is_banned:
		# return render(request,'home.html')
		cur_level = cur_user.player.current_level	
		# cur_level = Level.objects.get(level_id=5)
		form = self.form_class()
		context = {
			'level' : cur_level,
			'form': form,
		}
		if cur_level.level_id is 24:
			context['special'] = "code"
		elif cur_level.level_id in [6,10,27,35]:
			context['special'] = "dark"
		elif cur_level.level_id is 7:
			context['special'] = "math"
		else:
			context['special'] = "none"
		print(context)
		return render(request,'game/play.html',context)   #{{form|crispy}} crispy form was removed try to add it back


	def post(self,request, *args, **kwargs):
		"""
		POST request
		1. Get the current user and their answer
		2. If the answer is correct, update the level
		"""
		if request.user is None:
			return redirect('game-home')
		cur_user = User.objects.get(id=request.user.id)
		cur_level = cur_user.player.current_level
		level_number = cur_user.player.current_level.level_id

		form = self.form_class(request.POST)    #What if request != 'POST' ????
		if form.is_valid():
			ans = form.cleaned_data.get('answer')
			if ans == cur_level.answer:
				level_number = cur_user.player.current_level.level_id
				try:
					cur_user.player.current_level = Level.objects.get(level_id = level_number + 1)
					cur_user.player.points=cur_user.player.points+3
					cur_user.player.current_level_time = timezone.now()	 					
					cur_user.player.save()
				except:
					pass

		return redirect(reverse('play'))


class Bonus(View) :
	login_url = '/login/'
	redirect_field_name = '/register/'
	redierct_url = '/accounts/facebook/login/callback/'
	# Form field for the level
	form_class = LevelForm

	def get(self, request, *args, **kwargs):
		cur_user = User.objects.get(id=request.user.id)
		try:
			bonus_level = BonusQuestion.objects.get(level_id=cur_user.player.bonus_level_id)
			livedatetime=bonus_level.live_date
			# print("live date ", livedatetime)
			current_time=timezone.now()
			# print("current time ",current_time)
			expdatetime = bonus_level.expiration_date
			# print("expiry date ",expdatetime)
			expired = bonus_level.expiration_date < current_time
			if expired:
				# print("The question has expired")
				bonus_array = BonusQuestion.objects.filter(level_id__gt=cur_user.player.bonus_level_id)
				# print(bonus_array)
				for q in bonus_array:
					if q.live_date < current_time and current_time<q.expiration_date:
						cur_user.player.bonus_level_id = q.level_id
						# print("The bonus id is ",cur_user.player.bonus_level_id)
						bonus_level = BonusQuestion.objects.get(level_id=cur_user.player.bonus_level_id)
						cur_user.player.save()

			if bonus_level.expiration_date<timezone.now() or bonus_level.live_date>timezone.now():
				print("Question {0} not live".format(bonus_level.level_id))
				raise
		except:
			print("Error")
			return redirect(reverse('error'))
		form = self.form_class

		question = bonus_level.question
		livedatetime = bonus_level.live_date
		expdatetime = bonus_level.expiration_date
	
		current_time = timezone.now()
		year = expdatetime.strftime('%Y')
		month = expdatetime.strftime('%m')
		day = expdatetime.strftime('%d')
		hour = expdatetime.strftime('%H')
		minute = expdatetime.strftime('%M')
		second = expdatetime.strftime('%S')

		context = {'question': question,'year': year,'month': month,'day': day,'hour': hour,'minute': minute,
			'second':second,'expdate': expdatetime,'livedate': livedatetime,'now': current_time,'form':form,}
		return render(request, 'game/bonus.html', context)
	

	def post(self,request, *args, **kwargs):
		"""
		POST request
		1. Get the current user and their answer
		2. If the answer is correct, update the level
		"""
		cur_user = User.objects.get(id=request.user.id)
		bonus_level = BonusQuestion.objects.get(level_id=cur_user.player.bonus_level_id)
		form = self.form_class(request.POST)    #What if request != 'POST' ????
		if form.is_valid():
			ans = form.cleaned_data.get('answer')
			if ans == bonus_level.answer:
				
				level_number = bonus_level.level_id
				if cur_user.player.bonus_level_id == level_number:
					try:
						cur_user.player.bonus_level_id += 1
						cur_user.player.bonus_attempted=cur_user.player.bonus_attempted+1
						cur_user.player.points += 5	 					
						cur_user.player.save()
						return redirect(reverse('play'))
					except:
						pass
				else:
					print("Cant play Bonus Twice")
					return redirect(reverse('play'))
			else:
				print("Wrong Answer! Try Again")
				return redirect(reverse('bonus'))
		return redirect(reverse('play'))

def home(request):
	if request.method=="POST":
		form=TeamForm(request.POST)
		if (form.is_valid):
			#Check for Redundant Roll Numbers
			form.save()
			return HttpResponseRedirect('/')

	else:
		form=TeamForm()

	
	return render(request,'game/sarcasmbase.html')