from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from .models import Player, DEPARTMENTS
from django.contrib.auth.models import User
from collections import defaultdict

def register(request):
		if not request.user.is_authenticated:
			return redirect('game-home')
		current_user_player = request.user.player
		if current_user_player.details_done:
			return redirect('play')
		# current_user_data = User.objects.get(id = current_user.id)
		# try:
		# 	current_user_data = Player.objects.get(id = current_user.id)
		# except Player.DoesNotExist:
		# 	current_user_data = None
		if request.method == 'POST':
			form = UserRegisterForm(request.POST, instance = current_user_player)
			if form.is_valid():
				user = form.save()
				user.refresh_from_db()
				current_user_player.roll = str(current_user_player.user.username).upper()
				current_user_player.save()
				# username = form.cleaned_data.get('username')
				referral = str(form.cleaned_data.get('referral')).upper()
				if Player.objects.filter(roll=referral).exists() and referral != current_user_player.roll:
					t = Player.objects.get(roll=referral)
					if t.referral_count < 3:
						t.referral_count = t.referral_count+1
						t.points += 2
					t.save()
				
				current_user_player.details_done = True
				current_user_player.save()
				messages.success(request, 'Account created for {}!'.format(current_user_player.user.first_name))
				return redirect('play')
			else:
				form = UserRegisterForm()
			return render(request, 'users/register.html', {'form': form})
		form = UserRegisterForm()
		return render(request, 'users/register.html', {'form': form})

def INT(object):
    if object is None:
        return 0
    else:
        return object

def DEN(object):
    if object is 0:
        return 1
    else:
        return object
def Group(department):
    if department in [u'Energy Science and Engineering', u'Humanities & Social Science', u'Aerospace Engineering']:
        return "Group 1: Energy, HSS, Aero"
    elif department in [u'Centre for Environmental Science and Engineering',u'Chemistry',u'Mathematics', u'Physics']:
        return "Group 2: Env, Chem, Math, Phy"
    else:
        return department
def leaderboard(request):
    """
    Returns the leadboard, sorted first with level (desc) then time (asc)
    """
    queryset = User.objects.order_by(
        '-player__points', 'player__current_level_time')
    dept_rank = {} 
    dept_rank = defaultdict(lambda:0, dept_rank)
    for user in queryset[:100]:
        dept_rank[Group(user.player.department)] += 1
    context = {
        'queryset': queryset,
        'department': sorted(dept_rank.items(), key = lambda kv:(kv[1] if kv[1] is not None else 0, kv[0]), reverse=True),
        # 'dept_score': dept_rank[request.user.player.department] if request.user.player.department in dept_rank.keys() else 0
    }
    return render(request, 'users/leaderboard.html', context)

def clean():
    dd = [u'Aerospace Engineering', 
            u'Biosciences and Bioengineering', 
            u'Centre for Environmental Science and Engineering',
            u'Chemical Engineering', 
            u'Chemistry',
            u'Civil Engineering', 
            u'Computer Science & Engineering',
            u'Earth Sciences',
            u'Electrical Engineering', 
            u'Energy Science and Engineering', 
            u'Humanities & Social Science',
            u'Industrial Engineering and Operations Research', 
            u'Material Science',
            u'Materials, Manufacturing and Modelling',
            u'Mathematics', 
            u'Mechanical Engineering',
            u'Metallurgical Engineering & Materials Science', 
            u'National Centre for Mathematics',
            u'Physics', 
            u'Systems and Control Engineering']
    for user in User.objects.all():
        if user.player is None:
            user.delete()
    for player in Player.objects.all():
        if player.department not in dd:
            player.user.delete()
            player.delete()

        else:
            if player.department in [u'Material Science', u'Materials, Manufacturing and Modelling']:
                player.department = u'Metallurgical Engineering & Materials Science'
                player.save()
            elif player.department == u'National Centre for Mathematics':
                player.department = u'Mathematics'
                player.save()
            elif player.department in [u'Biosciences and Bioengineering',u'Earth Sciences',u'Systems and Control Engineering',u'Industrial Engineering and Operations Research']:
                player.department = u'Humanities & Social Science'
                player.save()