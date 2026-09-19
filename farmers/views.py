from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Farmer
from .forms import FarmerForm
def home(request):
    return render(request, 'farmers/home.html')

def register_farmer(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        mobile = request.POST.get('mobile')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register_farmer')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        Farmer.objects.create(
            user=user,
            name=name,
            mobile=mobile
        )

        messages.success(request, 'Registration successful!')
        return redirect('login_farmer')

    return render(request, 'farmers/register.html')


def login_farmer(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('farmer_dashboard')

        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'farmers/login.html')


@login_required
def farmer_dashboard(request):

    farmer = Farmer.objects.get(user=request.user)

    return render(
        request,
        'farmers/dashboard.html',
        {'farmer': farmer}
    )


def logout_farmer(request):

    logout(request)

    return redirect('home')
def farmer_list(request):
    farmers = Farmer.objects.all().order_by('-created_at')

    return render(
        request,
        'farmers/farmer_list.html',
        {'farmers': farmers}
    )


def farmer_create(request):
    if request.method == 'POST':
        form = FarmerForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('farmer_list')
    else:
        form = FarmerForm()

    return render(
        request,
        'farmers/farmer_form.html',
        {
            'form': form,
            'title': 'Add Farmer'
        }
    )


def farmer_update(request, id):
    farmer = get_object_or_404(Farmer, id=id)

    if request.method == 'POST':
        form = FarmerForm(request.POST, instance=farmer)

        if form.is_valid():
            form.save()
            return redirect('farmer_list')
    else:
        form = FarmerForm(instance=farmer)

    return render(
        request,
        'farmers/farmer_form.html',
        {
            'form': form,
            'title': 'Edit Farmer'
        }
    )


def farmer_delete(request, id):
    farmer = get_object_or_404(Farmer, id=id)

    if request.method == 'POST':
        farmer.delete()
        return redirect('farmer_list')

    return render(
        request,
        'farmers/farmer_confirm_delete.html',
        {'farmer': farmer}
    )