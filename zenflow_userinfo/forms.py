from django import forms 
from zenflow_userinfo.models import Team

class CreateTeamForm(forms.Form):
    name = forms.CharField(label='Name')

    def save(self):
        name = self.cleaned_data['name']
        team = Team.objects.create(name=name)
        team.save()
        return team
    
class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name']

class EditProfile(forms.Form):
    profile_picture = forms.CharField(label='profile_picture', required=False)
    first_name = forms.CharField(label='first_name')
    last_name = forms.CharField(label='last_name')
    birth_date = forms.CharField(label='birth_date')
    phone_number = forms.CharField(label='phone_number')
    password = forms.CharField(label='password', required=False)
    confirm_password = forms.CharField(label='confirm_password', required=False)
    team_id = forms.CharField(label='team_id', required=False)
