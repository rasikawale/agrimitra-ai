from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Farmer, Farm, Crop
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
def crop_update(request, id):

    farmer = get_object_or_404(
        Farmer,
        user=request.user
    )

    crop = get_object_or_404(
        Crop,
        id=id,
        farm__farmer=farmer
    )

    if request.method == 'POST':

        crop_name = request.POST.get('crop_name', '').strip()
        variety = request.POST.get('variety', '').strip()
        area = request.POST.get('area', '').strip()
        sowing_date = request.POST.get('sowing_date', '').strip()
        expected_harvest_date = request.POST.get(
            'expected_harvest_date',
            ''
        ).strip()
        irrigation_type = request.POST.get(
            'irrigation_type',
            ''
        ).strip()
        crop_stage = request.POST.get(
            'crop_stage',
            ''
        ).strip()

        if not crop_name:
            messages.error(
                request,
                'Crop name is required.'
            )

            return render(
                request,
                'farmers/crop_form.html',
                {
                    'farmer': farmer,
                    'crop': crop,
                    'title': 'Edit Crop'
                }
            )

        crop.crop_name = crop_name
        crop.variety = variety
        crop.area = area
        crop.sowing_date = sowing_date
        crop.expected_harvest_date = (
            expected_harvest_date
            if expected_harvest_date
            else None
        )
        crop.irrigation_type = irrigation_type
        crop.crop_stage = crop_stage

        crop.save()

        messages.success(
            request,
            'Crop updated successfully!'
        )

        return redirect('my_crops')

    return render(
        request,
        'farmers/crop_form.html',
        {
            'farmer': farmer,
            'crop': crop,
            'title': 'Edit Crop'
        }
    )
@login_required
def ai_prediction(request):
    farmer = get_object_or_404(Farmer, user=request.user)

    farms = Farm.objects.filter(
        farmer=farmer
    ).order_by('-created_at')

    crops = Crop.objects.filter(
        farm__farmer=farmer
    ).order_by('-created_at')

    prediction = None
    selected_crop = None
    selected_farm = None

    if request.method == 'POST':

        farm_id = request.POST.get('farm')
        crop_id = request.POST.get('crop')

        selected_farm = get_object_or_404(
            Farm,
            id=farm_id,
            farmer=farmer
        )

        selected_crop = get_object_or_404(
            Crop,
            id=crop_id,
            farm=selected_farm
        )

        # Temporary result only for testing the page.
        # We will replace this with the real ML model later.
        prediction = {
            'health': 'Healthy',
            'risk': 'Low',
            'confidence': '85%',
            'recommendation': (
                'Continue monitoring the crop regularly '
                'and maintain proper farm management.'
            )
        }

    return render(
        request,
        'farmers/ai_prediction.html',
        {
            'farmer': farmer,
            'farms': farms,
            'crops': crops,
            'prediction': prediction,
            'selected_crop': selected_crop,
            'selected_farm': selected_farm,
        }
    )
@login_required
def my_crops(request):

    farmer = get_object_or_404(
        Farmer,
        user=request.user
    )

    crops = Crop.objects.filter(
        farm__farmer=farmer
    ).select_related(
        'farm'
    ).order_by('-created_at')

    return render(
        request,
        'farmers/my_crops.html',
        {
            'farmer': farmer,
            'crops': crops
        }
    )


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

    farmer = get_object_or_404(
        Farmer,
        id=id
    )

    if request.method == 'POST':

        form = FarmerForm(
            request.POST,
            instance=farmer
        )

        if form.is_valid():
            form.save()
            return redirect('farmer_list')

    else:
        form = FarmerForm(
            instance=farmer
        )

    return render(
        request,
        'farmers/farmer_form.html',
        {
            'form': form,
            'title': 'Edit Farmer'
        }
    )


def farmer_delete(request, id):

    farmer = get_object_or_404(
        Farmer,
        id=id
    )

    if request.method == 'POST':

        farmer.delete()

        return redirect('farmer_list')

    return render(
        request,
        'farmers/farmer_confirm_delete.html',
        {'farmer': farmer}
    )

@login_required
def my_crops(request):

    farmer = get_object_or_404(
        Farmer,
        user=request.user
    )

    crops = Crop.objects.filter(
        farm__farmer=farmer
    ).select_related(
        'farm'
    ).order_by('-created_at')

    return render(
        request,
        'farmers/my_crops.html',
        {
            'farmer': farmer,
            'crops': crops
        }
    )
# =========================
# CROP MANAGEMENT
# =========================

@login_required
def crop_update(request, id):

    farmer = get_object_or_404(
        Farmer,
        user=request.user
    )

    crop = get_object_or_404(
        Crop,
        id=id,
        farm__farmer=farmer
    )

    farms = Farm.objects.filter(
        farmer=farmer
    ).order_by('-created_at')

    if request.method == 'POST':

        farm_id = request.POST.get('farm')

        crop_name = request.POST.get(
            'crop_name',
            ''
        ).strip()

        variety = request.POST.get(
            'variety',
            ''
        ).strip()

        area = request.POST.get(
            'area',
            ''
        ).strip()

        sowing_date = request.POST.get(
            'sowing_date'
        )

        expected_harvest_date = request.POST.get(
            'expected_harvest_date'
        )

        irrigation_type = request.POST.get(
            'irrigation_type'
        )

        crop_stage = request.POST.get(
            'crop_stage'
        )

        farm = get_object_or_404(
            Farm,
            id=farm_id,
            farmer=farmer
        )

        if not crop_name or not area or not sowing_date:

            messages.error(
                request,
                'Please fill all required fields.'
            )

            return render(
                request,
                'farmers/crop_form.html',
                {
                    'farmer': farmer,
                    'farms': farms,
                    'crop': crop,
                    'title': 'Edit Crop'
                }
            )

        crop.farm = farm
        crop.crop_name = crop_name
        crop.variety = variety
        crop.area = area
        crop.sowing_date = sowing_date

        crop.expected_harvest_date = (
            expected_harvest_date
            if expected_harvest_date
            else None
        )

        crop.irrigation_type = irrigation_type
        crop.crop_stage = crop_stage

        crop.save()

        messages.success(
            request,
            'Crop updated successfully!'
        )

        return redirect('my_crops')

    return render(
        request,
        'farmers/crop_form.html',
        {
            'farmer': farmer,
            'farms': farms,
            'crop': crop,
            'title': 'Edit Crop'
        }
    )


@login_required
def crop_delete(request, id):

    farmer = get_object_or_404(
        Farmer,
        user=request.user
    )

    crop = get_object_or_404(
        Crop,
        id=id,
        farm__farmer=farmer
    )

    if request.method == 'POST':

        crop.delete()

        messages.success(
            request,
            'Crop deleted successfully!'
        )

        return redirect('my_crops')

    return render(
        request,
        'farmers/crop_confirm_delete.html',
        {
            'crop': crop,
            'farmer': farmer
        }
    )


# =========================
# FARM MANAGEMENT
# =========================

@login_required
def my_farms(request):

    farmer = get_object_or_404(
        Farmer,
        user=request.user
    )

    farms = Farm.objects.filter(
        farmer=farmer
    ).order_by('-created_at')

    return render(
        request,
        'farmers/my_farms.html',
        {
            'farmer': farmer,
            'farms': farms
        }
    )


@login_required
def farm_create(request):

    farmer = get_object_or_404(
        Farmer,
        user=request.user
    )

    if request.method == 'POST':

        farm_name = request.POST.get('farm_name')
        location = request.POST.get('location')
        area = request.POST.get('area')
        soil_type = request.POST.get('soil_type')

        Farm.objects.create(
            farmer=farmer,
            farm_name=farm_name,
            location=location,
            area=area,
            soil_type=soil_type
        )

        messages.success(
            request,
            'Farm added successfully!'
        )

        return redirect('my_farms')

    return render(
        request,
        'farmers/farm_form.html',
        {
            'farmer': farmer,
            'title': 'Add Farm'
        }
    )


@login_required
def farm_update(request, id):

    farmer = get_object_or_404(
        Farmer,
        user=request.user
    )

    farm = get_object_or_404(
        Farm,
        id=id,
        farmer=farmer
    )

    if request.method == 'POST':

        farm_name = request.POST.get(
            'farm_name',
            ''
        ).strip()

        location = request.POST.get(
            'location',
            ''
        ).strip()

        area = request.POST.get(
            'area',
            ''
        ).strip()

        soil_type = request.POST.get(
            'soil_type',
            ''
        ).strip()

        # Validate required fields

        if not farm_name:

            messages.error(
                request,
                'Farm name is required.'
            )

            return render(
                request,
                'farmers/farm_form.html',
                {
                    'farmer': farmer,
                    'farm': farm,
                    'title': 'Edit Farm'
                }
            )

        if not location:

            messages.error(
                request,
                'Farm location is required.'
            )

            return render(
                request,
                'farmers/farm_form.html',
                {
                    'farmer': farmer,
                    'farm': farm,
                    'title': 'Edit Farm'
                }
            )

        if not area:

            messages.error(
                request,
                'Farm area is required.'
            )

            return render(
                request,
                'farmers/farm_form.html',
                {
                    'farmer': farmer,
                    'farm': farm,
                    'title': 'Edit Farm'
                }
            )

        if not soil_type:

            messages.error(
                request,
                'Soil type is required.'
            )

            return render(
                request,
                'farmers/farm_form.html',
                {
                    'farmer': farmer,
                    'farm': farm,
                    'title': 'Edit Farm'
                }
            )

        # Update farm

        farm.farm_name = farm_name
        farm.location = location
        farm.area = area
        farm.soil_type = soil_type

        farm.save()

        messages.success(
            request,
            'Farm updated successfully!'
        )

        return redirect('my_farms')

    return render(
        request,
        'farmers/farm_form.html',
        {
            'farmer': farmer,
            'farm': farm,
            'title': 'Edit Farm'
        }
    )


@login_required
def farm_delete(request, id):

    farmer = get_object_or_404(
        Farmer,
        user=request.user
    )

    farm = get_object_or_404(
        Farm,
        id=id,
        farmer=farmer
    )

    if request.method == 'POST':

        farm.delete()

        messages.success(
            request,
            'Farm deleted successfully!'
        )

        return redirect('my_farms')

    return render(
        request,
        'farmers/farm_confirm_delete.html',
        {
            'farmer': farmer,
            'farm': farm
        }
    )


@login_required
def crop_create(request):

    farmer = get_object_or_404(
        Farmer,
        user=request.user
    )

    farms = Farm.objects.filter(
        farmer=farmer
    ).order_by('-created_at')

    if request.method == 'POST':

        farm_id = request.POST.get('farm')

        crop_name = request.POST.get(
            'crop_name',
            ''
        ).strip()

        variety = request.POST.get(
            'variety',
            ''
        ).strip()

        area = request.POST.get(
            'area',
            ''
        ).strip()

        sowing_date = request.POST.get(
            'sowing_date'
        )

        expected_harvest_date = request.POST.get(
            'expected_harvest_date'
        )

        irrigation_type = request.POST.get(
            'irrigation_type'
        )

        crop_stage = request.POST.get(
            'crop_stage'
        )

        farm = get_object_or_404(
            Farm,
            id=farm_id,
            farmer=farmer
        )

        if not crop_name:

            messages.error(
                request,
                'Crop name is required.'
            )

            return render(
                request,
                'farmers/crop_form.html',
                {
                    'farmer': farmer,
                    'farms': farms,
                    'title': 'Add Crop'
                }
            )

        if not area:

            messages.error(
                request,
                'Crop area is required.'
            )

            return render(
                request,
                'farmers/crop_form.html',
                {
                    'farmer': farmer,
                    'farms': farms,
                    'title': 'Add Crop'
                }
            )

        Crop.objects.create(
            farm=farm,
            crop_name=crop_name,
            variety=variety,
            area=area,
            sowing_date=sowing_date,
            expected_harvest_date=(
                expected_harvest_date
                if expected_harvest_date
                else None
            ),
            irrigation_type=irrigation_type,
            crop_stage=crop_stage
        )

        messages.success(
            request,
            'Crop added successfully!'
        )

        return redirect('my_crops')

    return render(
        request,
        'farmers/crop_form.html',
        {
            'farmer': farmer,
            'farms': farms,
            'title': 'Add Crop'
        }
    )