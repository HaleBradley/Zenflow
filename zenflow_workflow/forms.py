from django import forms
from django.forms import ModelForm, TextInput, DateInput, NumberInput, Select, URLInput
from zenflow_workflow.models import Workflow, Comment, Link, Task

class CreateWorkflowForm(forms.Form):
    name = forms.CharField(label='Name')
    description = forms.CharField(label='Description')

class CreateTask(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'deadline', 'status']
        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'style': 'max_width: 300px',
                'placeholder': 'Name',
            }),
            'description': TextInput(attrs={
                'class': 'form-control',
                'style': 'max_width: 300px',
                'placeholder': 'Description',
            }),
            'deadline': TextInput(attrs={
                'class': 'form-control',
                'style': 'max_width: 300px',
                'type': 'date',
                'placeholder': 'Deadline',
            }),
            'status': Select(attrs={
                'class': 'form-control',
                'style': 'max_width: 300px',
            }, choices=Task.STATUS_CHOICES),
            
        }

class EditTask(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'deadline', 'status']
        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'style': 'max_width: 300px',
                'placeholder': 'Name',
            }),
            'description': TextInput(attrs={
                'class': 'form-control',
                'style': 'max_width: 300px',
                'placeholder': 'Description',
            }),
            'deadline': TextInput(attrs={
                'class': 'form-control',
                'style': 'max_width: 300px',
                'type': 'date',
                'placeholder': 'Deadline',
            }),
            'status': Select(attrs={
                'class': 'form-control',
                'style': 'max_width: 300px',
            }, choices=Task.STATUS_CHOICES),
        }

class CreateComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 800px;',
                })
        }
        

class CreateLink(forms.ModelForm):
    class Meta:
        model = Link
        fields = ['url']
        widgets = {
            'url': URLInput(attrs={
                'class': "form-control",
                'style': 'max-width: 800px;',
                })
        }

class WorkflowForm(forms.ModelForm):
    class Meta:
        model = Workflow
        fields = ['name', 'description']
        widgets = {
            'name': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Name'
                }),
                'description': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'description'
                }),
        }

