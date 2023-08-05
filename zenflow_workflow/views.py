from django.shortcuts import render, redirect
from datetime import date
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from zenflow_workflow.forms import CreateWorkflowForm, WorkflowForm, CreateComment, CreateLink, CreateTask, EditTask
from zenflow_workflow.models import Workflow, Task, TaskAssignment, Comment, Link
from zenflow_userinfo.models import Employee, Team


def editworkflow(request, pk):
    if request.session['is_manager']:
        workflow = get_object_or_404(Workflow, pk=pk)

        if request.method == 'POST':
            form = WorkflowForm(request.POST, instance=workflow)
            if form.is_valid():
                form.save()
                return work_list(request)
        else:
            form = WorkflowForm(instance=workflow)

        return render(request, '../templates/workflow/workflow_edit.html', {'form': form, 'workflow': workflow})
    else:
        return redirect(work_list)
    
def edittask(request):
    task = get_object_or_404(Task, pk=request.session['task_id'])

    if request.method == 'POST':
        form = EditTask(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return workflow_view(request)
    else:
        form = EditTask(instance=task)

    return render(request, '../templates/workflow/workflow_edit.html', {'form': form, 'task': task})


def createworkflow(request):
    if request.session['is_manager']:
        if request.method == 'POST':
            form = CreateWorkflowForm(request.POST)
            if form.is_valid():
                current_date = date.today()
                name = form.cleaned_data['name']
                description = form.cleaned_data['description']
                team = get_object_or_404(Team, pk=request.session['team_id'])
                workflow = Workflow.objects.create(
                    name=name,
                    description=description,
                    date_started=current_date,
                    team_id=team
                )
                workflow.save()
                return redirect(work_list)
        else:
            form = CreateWorkflowForm()
            return render(request, '../templates/workflow/createworkflow.html', {'form': form})
    else:
        return redirect(work_list)

    
def backlog(request):
    flow_list = Workflow.objects.filter(team_id = request.session['team_id']).order_by('workflow_id')
    flow_dict = {'workflow': flow_list}
    return render(request, '../templates/workflow/workflow_backlog.html', context=flow_dict)

def deleteWorkflow(request, pk):
    if request.session['is_manager']:
        try: 
            work = get_object_or_404(Workflow, pk=pk)
            work.delete()
        except Workflow.DoesNotExist:
            messages.error(request, 'Team not found!')
            
        return redirect('worklist')
    else:
        return redirect(work_list)


def work_list(request):
    flow_list = Workflow.objects.filter(team_id=request.session['team_id']).order_by('workflow_id')
    flow_dict = {'work': flow_list}


    return render(request, '../templates/workflow/workflow_list.html', context=flow_dict)

def workflow_save(request, pk):
    # Maybe check if user is apart of workflow
    request.session['workflow_id'] = pk
    request.session['task_id'] = ''
    return redirect('workflowview')

def complete_workflow(request):
    workflow = get_object_or_404(Workflow, pk=request.session['workflow_id'])
    workflow.date_completed = date.today()
    workflow.save()
    # currentdate = date.today
    # work = Workflow.objects.filter(pk=request.session['workflow_id']).update(date_completed = currentdate)
    # work.save()
    return redirect(work_list)


def task_save(request, pk):
    # Maybe check if user is apart of workflow
    request.session['task_id'] = pk
    return redirect('workflowview')

def addcomment(request):
    if request.method == 'POST':
        form = CreateComment(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            emp = get_object_or_404(Employee, pk=request.session['employee_id'])
            task = get_object_or_404(Task, pk=request.session['task_id'])
            profpic = emp.profile_picture
            comment = Comment.objects.create(text=text, employee_id = emp, task_id = task, profile_picture = profpic)
            comment.save()
            return redirect(workflow_view)
    else:
            form = CreateComment()
            return render(request, '../templates/workflow/addcomment.html', {'form': form})

def addlink(request):
    if request.method == 'POST':
        form = CreateLink(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            task = get_object_or_404(Task, pk=request.session['task_id'])
            link = Link.objects.create(url=url,task_id=task)
            link.save()
            return redirect(workflow_view)
    else:
        form = CreateLink()
    return render(request, '../templates/workflow/addlink.html', {'form': form})

def addtask(request):
    if request.method == 'POST':
        form = CreateTask(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            desc = form.cleaned_data['description']
            deadline = form.cleaned_data['deadline']
            status = form.cleaned_data['status']
            workid = get_object_or_404(Workflow, pk=request.session['workflow_id'])
            task = Task.objects.create(name=name, description=desc, deadline=deadline, workflow_id=workid, status=status)
            print(task.status)
            task.save()
            return redirect('workflowsave', request.session['workflow_id'])
    else:
        form = CreateTask()
    return render(request, '../templates/workflow/addtask.html', {'form':form})

def workflow_view(request):
    workflow = Workflow.objects.get(workflow_id=request.session['workflow_id'])

    todo_task_list = Task.objects.filter(workflow_id=request.session['workflow_id'], status='to do')
    inprogress_task_list = Task.objects.filter(workflow_id=request.session['workflow_id'], status='in progress')
    inreview_task_list = Task.objects.filter(workflow_id=request.session['workflow_id'], status='in review')
    completed_task_list = Task.objects.filter(workflow_id=request.session['workflow_id'], status='completed')
    task = None 
    dict = {}
    taskassignment_list = []
    employee_list = []
    task_employee_list = []
    comments_list = []
    links_list = []


    if(request.session['task_id'] != ''):
        task = Task.objects.get(workflow_id=request.session['workflow_id'], task_id = request.session['task_id'])

        taskassignment_list = TaskAssignment.objects.filter(task_id=task.task_id)
        employee_list = Employee.objects.order_by('employee_id')

        for ta in taskassignment_list:
            for e in employee_list:
                if ta.employee_id.employee_id == e.employee_id:
                    task_employee_list.append(e)
        
        comments_list = Comment.objects.filter(task_id=request.session['task_id'])
        links_list = Link.objects.filter(task_id=request.session['task_id'])
        
        dict={'workflow': workflow, 'todo_task_list': todo_task_list, 'inprogress_task_list': inprogress_task_list, 'inreview_task_list': inreview_task_list, 'completed_task_list': completed_task_list, 'task': task, 'task_employee_list': task_employee_list, 'comments_list': comments_list, 'links_list': links_list}      
    else:
        dict={'workflow': workflow, 'todo_task_list': todo_task_list, 'inprogress_task_list': inprogress_task_list, 'inreview_task_list': inreview_task_list, 'completed_task_list': completed_task_list, 'task_employee_list': task_employee_list}      

    return render(request, '../templates/workflow/workflow_view.html', context=dict)