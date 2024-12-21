from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Survey
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

def logout_user(request):
    logout(request)
    return redirect('login')

def create_survey(request):
    return render(request, './survey/create.html')