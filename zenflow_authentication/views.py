from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
import re
import hashlib

from zenflow_authentication.forms import SignupForm, LoginForm
from zenflow_userinfo import views
from zenflow_userinfo import urls
from zenflow_userinfo.models import Employee, Team

def landing(request):
        return render(request, '../templates/authentication/landing.html', context=None)

def login(request):
        if request.method == 'POST':
                form = LoginForm(request.POST)
                if form.is_valid():
                        try:
                                try:
                                        employee_object = Employee.objects.get(email=form.cleaned_data['email'])
                                        request.session['invalid_email_error'] = ''
                                        if(employee_object.password == hashlib.sha256(str(form.cleaned_data['password']).encode('utf-8')).hexdigest()):
                                                request.session['invalid_password_error'] = ''
                                                request.session['employee_id'] = employee_object.employee_id
                                                request.session['email'] = employee_object.email
                                                request.session['first_name'] = employee_object.first_name
                                                request.session['last_name'] = employee_object.last_name
                                                request.session['phone_number'] = employee_object.phone_number
                                                request.session['birth_date'] = str(employee_object.birth_date)
                                                request.session['is_manager'] = employee_object.is_manager
                                                request.session['profile_picture'] = employee_object.profile_picture
                                                if(employee_object.team_id != None):
                                                        request.session['team_id'] = employee_object.team_id.team_id
                                                request.session['edit_account'] = ''
                                                request.session['task_id'] = ''
                                                return redirect(views.profile)
                                        else: 
                                                request.session['invalid_password_error'] = 'Incorrect Password' #incorrect password error
                                                return redirect(landing)
                                except:
                                        request.session['invalid_password_error'] = ''
                                        request.session['invalid_email_error'] = 'Incorrect Email/Username' #email/username invalid error
                                        return redirect(landing)
                        except:
                                request.session['invalid_password_error'] = ''
                                request.session['invalid_email_error'] = ''
                                request.session['database_retrieval_error'] = 'Please Contact the System Administrator' #employee properties cannot be stored to the session error
                                return redirect(landing)
                return redirect(landing)
        return redirect(landing)

def logout(request):
        request.session.flush()
        request.session.clear()
        del request.session
        return redirect(landing)

def signup(request):
        return render(request, '../templates/authentication/signup.html', context=None)

def register(request):
        if request.method == 'POST':
                form = SignupForm(request.POST)
                if form.is_valid():
                        request.session['signup_errors'] = ''
                        #email validation
                        try:
                                employee_object = Employee.objects.get(email=form.cleaned_data['email'])
                                request.session['signup_errors'] += 'Email Already In Use'
                                return redirect(signup)
                        except:
                                regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
                                if(not re.fullmatch(regex, form.cleaned_data['email'])):
                                        request.session['signup_errors'] += 'Invalid Email Address'
                                        return redirect(signup)
                        #password validation
                        if(form.cleaned_data['password'] != form.cleaned_data['confirm_password']):
                                request.session['signup_errors'] += 'Passwords Do Not Match'
                                return redirect(signup)
                        regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&_()])[A-Za-z\d@$!#%*?&_()]{8,20}$'
                        if(not re.fullmatch(regex, form.cleaned_data['password'])):
                                request.session['signup_errors'] += 'Your Password Must Have At Least One Uppercase Letter, One Lowercase Letter, One Digit, One Special Character (@$!#%*?&()_), And Be Between 8-20 Characters'
                                return redirect(signup)
                        #team_id validation
                        if(form.cleaned_data['team_id'] != ''):
                                try:
                                        employee_object = Team.objects.get(team_id=form.cleaned_data['team_id'])
                                        request.session['no_team_at_signup'] = ''
                                except:
                                        request.session['signup_errors'] += 'Team Code Does Not Exist'
                                        return redirect(signup)
                        else:
                                request.session['no_team_at_signup'] = 'true'
                        password_hash = hashlib.sha256(str(form.cleaned_data['password']).encode('utf-8')).hexdigest()
                        try:
                                if(request.session['no_team_at_signup']):
                                        #create team without team_id
                                        new_employee = Employee.objects.create(
                                                first_name=form.cleaned_data['first_name'],
                                                last_name=form.cleaned_data['last_name'],
                                                birth_date=str(form.cleaned_data['birth_date']),
                                                email=form.cleaned_data['email'],
                                                password=password_hash,
                                                phone_number=str(form.cleaned_data['phone_number']),
                                                is_manager=False,
                                                team_id=None
                                        )
                                else:
                                        #create team with team_id
                                        new_employee = Employee.objects.create(
                                                first_name=form.cleaned_data['first_name'],
                                                last_name=form.cleaned_data['last_name'],
                                                birth_date=str(form.cleaned_data['birth_date']),
                                                email=form.cleaned_data['email'],
                                                password=password_hash,
                                                phone_number=str(form.cleaned_data['phone_number']),
                                                is_manager=False,
                                                team_id=Team.objects.get(team_id=form.cleaned_data['team_id'])
                                        )
                                new_employee.save()
                                return redirect(landing)
                        except:
                                request.session['signup_errors'] += 'Something Went Wrong... Please Contact A System Administrator'
                                return redirect(signup)
                return redirect(signup)
        return redirect(signup)

def helpme(request):
        return render(request, '../templates/authentication/help.html', context=None)
