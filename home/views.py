from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth import login as do_login
from django.contrib.auth import logout


def error_404_view(request, exception):
    return render(request, 'home/404.html', status=404)

@login_required
def index(request):
    return render(request, "home/index.html")

def configuracion(request):
    return render(request, "home/configuracion.html")

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            do_login(request, user)
            return redirect('home:index')
   
    return render(request, "home/login.html")

def logout_view(request):
    logout(request)
    return redirect('home:login')
    # Redirect to a success page.