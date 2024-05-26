from django.shortcuts import render, redirect  
from user.forms import SignUpForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            user = authenticate(request, username=username, password=password, email=email)
            login(request, user)
            messages.success(request, ("Registered Successfully"))
            return redirect('user_profile')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Successfully Logged In"))
            return redirect('user_profile')
        else:
            messages.success(request, ("There Was An Error Logging In, Try Again..."))
            return redirect('login')
    else:
        return render(request, 'login.html')
    

def logout_user(request):
    logout(request)
    messages.success(request, ("You Were Logged Out"))
    return redirect('home_page')