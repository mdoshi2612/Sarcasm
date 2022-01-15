from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Player, Team

class TeamForm(forms.ModelForm):
    class Meta:
        model=Team
        fields='__all__'


class UserRegisterForm(forms.ModelForm):
	email=forms.EmailField(label="Personal Email Address")
	referral = forms.CharField(max_length=9)
	def __init__(self, *args, **kwargs):
		super(UserRegisterForm, self).__init__(*args, **kwargs)
		# Making name required
		self.fields['email'].required = True
		self.fields['referral'].required = False
		# self.fields['first_name'].required = True

	class Meta:
		model=Player
		fields=['username','department']