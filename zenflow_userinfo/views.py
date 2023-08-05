from django.shortcuts import render, redirect, get_object_or_404
import hashlib, re
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Max
from zenflow_userinfo.models import Employee, Team
from zenflow_workflow.models import Workflow
from zenflow_userinfo.forms import CreateTeamForm, TeamForm, EditProfile
from zenflow_authentication import views
from django.core.files.images import ImageFile

def profile(request):
        user_objects = Employee.objects.filter(employee_id=1) #employee_id needs to equal the signed in user
        user = {'user': user_objects}
        return render(request, '../templates/userinfo/profile.html', context=user)

def teamlist(request):
        team_list = Team.objects.filter(team_id = request.session['team_id']).prefetch_related('workflows', 'employees')
        team_dict = {'team':team_list}
        return render(request, '../templates/userinfo/teamlist.html', context=team_dict)

def editTeam(request, pk):
        if request.session['is_manager']:
                team = get_object_or_404(Team, pk=pk)

                if request.method == 'POST':
                        form = TeamForm(request.POST, instance=team)
                        if form.is_valid():
                                form.save()
                                return teamlist(request)
                else:
                        form = TeamForm(instance=team)
                return render(request, '../templates/userinfo/editteam.html', {'form': form, 'team': team})
        else:
                return redirect('teamlist')

def emplist(request):
        emp_list = Employee.objects.filter(team_id = request.session['team_id']).order_by('employee_id')
        emp_dict = {'emp':emp_list}
        return render(request, '../templates/userinfo/emplist.html', context=emp_dict)

def createteam(request):
        if request.method == 'POST':
                form = CreateTeamForm(request.POST)
                if form.is_valid():
                        form.save()
                        emp = get_object_or_404(Employee, pk=request.session['employee_id'])
                        emp.is_manager = True
                        teamid = Team.objects.aggregate(Max('team_id'))['team_id__max']
                        request.session['team_id'] = teamid
                        emp.team_id = get_object_or_404(Team, pk=request.session['team_id'])
                        emp.save()
                        request.session['is_manager']=True
                        return teamlist(request)
        else:
                form = CreateTeamForm()
                return render(request, '../templates/userinfo/teamcreate.html', {'form': form})
        return redirect('teamlist')  
                
def deleteTeam(request, team_id):
        if request.session['is_manager']:
                try: 
                        team = get_object_or_404(Team, pk=team_id)
                        team.delete()
                except Team.DoesNotExist:
                        messages.error(request, 'Team not found!')

                return redirect('teamlist')
        else:
                return redirect('teamlist')

def deleteaccount(request):
        try: 
                user_for_delete = Employee.objects.get(employee_id=request.session['employee_id'])
                user_for_delete.delete()
        except:
                messages.error(request, 'Unable to Delete Account!')    
        request.session.flush()
        request.session.clear()
        del request.session
        return redirect(views.landing)

def editaccount(request):
        request.session['edit_account'] = 'active'
        return redirect(profile)

def canceledit(request):
        request.session['edit_account'] = ''
        return redirect(profile)

def editprofile(request):
        if request.method == 'POST':
                form = EditProfile(request.POST)
                if form.is_valid():
                        request.session['edit_errors'] = ''
                        #password validation
                        if(form.cleaned_data['password'] != ''):
                                if(form.cleaned_data['password'] != form.cleaned_data['confirm_password']):
                                        request.session['edit_errors'] += 'Passwords Do Not Match'
                                        return redirect(profile)
                                regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&_()])[A-Za-z\d@$!#%*?&_()]{8,20}$'
                                if(not re.fullmatch(regex, form.cleaned_data['password'])):
                                        request.session['edit_errors'] += 'Your Password Must Have At Least One Uppercase Letter, One Lowercase Letter, One Digit, One Special Character (@$!#%*?&()_), And Be Between 8-20 Characters'
                                        return redirect(profile)
                        #team_id validation
                        if(form.cleaned_data['team_id'] != ''):
                                try:
                                        Team.objects.get(team_id=form.cleaned_data['team_id'])
                                except:
                                        request.session['edit_errors'] += 'Team Code Does Not Exist'
                                        return redirect(profile)
                        if(form.cleaned_data['password'] != ''):
                                password_hash = hashlib.sha256(str(form.cleaned_data['password']).encode('utf-8')).hexdigest()
                        # try:
                        Employee.objects.filter(employee_id=request.session['employee_id']).update(
                                first_name=form.cleaned_data['first_name'],
                                last_name=form.cleaned_data['last_name'],
                                birth_date=str(form.cleaned_data['birth_date']),
                                phone_number=form.cleaned_data['phone_number']
                        )
                        request.session['first_name'] = form.cleaned_data['first_name']
                        request.session['last_name'] = form.cleaned_data['last_name']
                        request.session['birth_date'] = str(form.cleaned_data['birth_date'])
                        request.session['phone_number'] = str(form.cleaned_data['phone_number'])
                        if(form.cleaned_data['profile_picture'] != ''):
                                Employee.objects.filter(employee_id=request.session['employee_id']).update(
                                        profile_picture=form.cleaned_data['profile_picture']
                                )
                                request.session['profile_picture'] = form.cleaned_data['profile_picture']    
                        if(form.cleaned_data['team_id'] != ''):
                                Employee.objects.filter(employee_id=request.session['employee_id']).update(
                                        team_id=Team.objects.get(team_id=form.cleaned_data['team_id']),
                                        is_manager=False
                                )
                                request.session['team_id'] = form.cleaned_data['team_id']  
                        if(form.cleaned_data['password'] != ''):
                                Employee.objects.filter(employee_id=request.session['employee_id']).update(
                                        password=password_hash,
                                )
                        request.session['edit_account'] = ''
                        request.session['edit_errors'] = ''
                        return redirect(profile)
                        # except:
                        #         request.session['edit_errors'] += 'Something Went Wrong... Please Contact A System Administrator'
                        #         return redirect(profile)
                return redirect(profile)
        return redirect(profile)