from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Survey, Question
from django.contrib.auth import authenticate,login,logout

# Create your views here.

@login_required(login_url='auth/register')
def home(request):
    
    surveys = Survey.objects.filter(user = request.user)
    print(surveys)
    
    data = {
        'surveys': surveys
    }
    
    return render(request, './survey/home.html', data)

def register(request):
    if request.method == 'POST':
        data = {
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'email': request.POST.get('email'),
            'username': request.POST.get('username'),
            'password': request.POST.get('password'),
        }
    
        new_user = User.objects.create(
            first_name = data['first_name'],
            last_name = data['last_name'],
            email = data['email'],
            username = data['username']
        )
        
        new_user.set_password(data['password'])
        new_user.save()
        
        print('New user created')
        return redirect('login')

    return render(request, './auth/register.html')

def login_user(request):
    if request.method == 'POST':
        data = {
            'username': request.POST.get('username'),
            'password': request.POST.get('password'),
        }
        print('data', data)
        
        user = authenticate(request, username=data['username'], password=data['password'])
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('register')
        
    return render(request, './auth/login.html')

@login_required(login_url='auth/register')
def logout_user(request):
    logout(request)
    return redirect('login')

@login_required(login_url='auth/register')
def create_survey(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        survey = Survey.objects.create(
            title= title,
            user= request.user
        )
        print(survey)
        redirect('create_question')

    return render(request, './survey/create.html')

@login_required(login_url='auth/register')
def create_question(request):
    return render(request, './survey/create-question.html')

def get_survey_by_id(request, survey_id):
    return render(request, './survey/survey-by-id.html', {'survey_id': survey_id})

@login_required(login_url='auth/register')
def delete_survey_by_id(request, survey_id):
    if survey_id is not None:
        Survey.objects.filter(id = survey_id).delete()
        print("Survey deleted!!")
    
    return redirect('home')

def edit_survey_by_id(request, survey_id):
    if survey_id is not None:
        survey_info = Survey.objects.filter(id = survey_id)[0]
        questions = Question.objects.filter(survey = survey_info)
        print("survey_info", survey_info)
        return render(request, './survey/edit-survey.html', {'survey_info': survey_info, 'questions': questions})