from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Survey, Question, Choice, Response
from django.contrib.auth import authenticate,login,logout

# Create your views here.

# AUTHENTICATION ROUTES
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



# MAIN ROUTES
@login_required(login_url='auth/register')
def home(request):
    
    surveys = Survey.objects.filter(user = request.user)
    print(surveys)
    
    data = {
        'surveys': surveys
    }
    
    return render(request, './survey/home.html', data)

@login_required(login_url='auth/register')
def create_survey(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        survey = Survey.objects.create(
            title= title,
            user= request.user
        )
        return redirect(f'/survey/{survey.id}/add-question/')

    return render(request, './survey/create.html')

@login_required(login_url='auth/register')
def add_question(request, survey_id):
    survey = Survey.objects.filter(id = survey_id)[0]
    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        choices = []
        for i in range(1,5):
            choices.append(request.POST.get(f'choice_{i}'))
        
        new_question = Question.objects.create(
            survey = survey,
            text = question_text
        )

        for choice in choices:
            if choice != '':
                Choice.objects.create(
                    question = new_question,
                    text = choice
                )
        
        if request.POST.get('action') == 'add_another':
            return render(request, './survey/add-question.html')
        else:
            return redirect('home')


    return render(request, './survey/add-question.html')

@login_required(login_url='auth/register')
def delete_survey_by_id(request, survey_id):
    if survey_id is not None:
        Survey.objects.filter(id = survey_id).delete()
        print("Survey deleted!!")
    
    return redirect('home')

def get_survey_by_id(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    survey_url = request.build_absolute_uri()

    if request.method == 'POST':
        for question in survey.questions.all():
            # Get the submitted choices for this question
            submitted_choices = request.POST.getlist(f"choice_{question.id}[]")
            print(f"Submitted choices for question {question.id}: {submitted_choices}")

            for choice_id in submitted_choices:
                choice = get_object_or_404(Choice, id=choice_id)
                print("choice", choice)
                print("question", question)

                # Create a response for each selected choice
                response = Response.objects.create(
                    survey=survey,
                    question=question,
                    choice=choice
                )

                # Associate the response with the authenticated user if available
                if request.user.is_authenticated:
                    response.user = request.user
                response.save()

        return render(request, './survey/thank-you.html')

    return render(request, './survey/survey-by-id.html', {'survey': survey, 'survey_url': survey_url})