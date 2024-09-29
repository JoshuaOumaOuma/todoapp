from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .models import todo
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(request):
    if request.method == "POST":
        tasks = request.POST.get('task')
        new_todo = todo(user=request.user,name=tasks)
        new_todo.save()

    all_todos = todo.objects.filter(user = request.user)

    context = {
        'todo' : all_todos
    }
        
    return render(request,'baseapp/todo.html',context)


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        
        # Check for minimum password length
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return redirect('register')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        # Check if email is already in use
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('register')
        
        new_user = User.objects.create_user(username=username,email=email,password=password)
        new_user.save()

        messages.success(request,"Registration Successful")
        return redirect('loginpage')
    return render(request,'baseapp/register.html')

def loginpage(request):
    if request.method == "POST":
        # Get username and password from POST request
        username = request.POST.get('uname')
        password = request.POST.get('pass')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Login the user and redirect to the home page
            login(request, user)
            return redirect('home')
        else:
            # Show error message if credentials are invalid and redirect to login page
            messages.error(request, "Invalid credentials. Please try again or register.")
            return redirect('loginpage')  # Redirect back to the login page to try again

    # Render the login page if method is GET
    return render(request, 'baseapp/login.html')

def logout_view(request):
    logout(request)
    return redirect('loginpage')

@login_required
def Delete(request,name):
    to_delete = todo.objects.get(user=request.user,name=name)
    to_delete.delete()
    return redirect('home')

@login_required
def update(request,name):
    to_update = todo.objects.get(user=request.user,name=name)
    to_update.status = True
    to_update.save()
    return redirect('home')

    