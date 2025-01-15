from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Pet
from .forms import RegisterForm, LoginForm, PetForm
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from functools import wraps

PET_FUND_BALANCE = 0

def login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect('login_user')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def home(request):
    return render(request, 'pets/home.html')

def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Đăng ký thành công.")
            return redirect('login_user')
    else:
        form = RegisterForm()
    return render(request, 'pets/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = User.objects.filter(username=form.cleaned_data['username']).first()
            if user and user.check_password(form.cleaned_data['password']):
                request.session['user_id'] = user.id
                messages.success(request, "Đăng nhập thành công.")
                return redirect('home')
            messages.error(request, "Tên đăng nhập hoặc mật khẩu không chính xác.")
    else:
        form = LoginForm()
    return render(request, 'pets/login.html', {'form': form})

@login_required
def add_pet(request):
    if request.method == 'POST':
        form = PetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thêm thú cưng thành công.")
            return redirect('view_pets')
    else:
        form = PetForm()
    return render(request, 'pets/add_pet.html', {'form': form})

@login_required
def view_pets(request):
    pets = Pet.objects.all()
    return render(request, 'pets/view_pets.html', {'pets': pets})

@login_required
def adopt_pet(request):
    if request.method == 'POST':
        pet_id = request.POST['pet_id']
        pet = Pet.objects.get(id=pet_id)
        user = User.objects.get(id=request.session['user_id'])
        if not pet.owner:
            pet.owner = user
            pet.is_available_for_adoption = False
            pet.save()
            messages.success(request, "Nhận nuôi thú cưng thành công.")
        else:
            messages.error(request, "Thú cưng đã có chủ.")
        return redirect('view_pets')
    pets = Pet.objects.filter(owner=None, is_available_for_adoption=True)
    return render(request, 'pets/adopt_pet.html', {'pets': pets})

@login_required
def donate_to_fund(request):
    global PET_FUND_BALANCE
    if request.method == 'POST':
        amount = float(request.POST['amount'])
        if amount > 0:
            PET_FUND_BALANCE += amount
            messages.success(request, "Đóng góp thành công.")
        else:
            messages.error(request, "Số tiền phải lớn hơn 0.")
    return render(request, 'pets/donate.html')

@login_required
def view_fund_balance(request):
    global PET_FUND_BALANCE
    return render(request, 'pets/view_balance.html', {'balance': PET_FUND_BALANCE})

@login_required
def edit_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if request.method == 'POST':
        form = PetForm(request.POST, instance=pet)
        if form.is_valid():
            form.save()
            messages.success(request, "Cập nhật thông tin thú cưng thành công.")
            return redirect('view_pets')
    else:
        form = PetForm(instance=pet)
    return render(request, 'pets/edit_pet.html', {'form': form, 'pet': pet})

@login_required
def delete_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if request.method == 'POST':
        pet.delete()
        messages.success(request, "Xóa thú cưng thành công.")
        return redirect('view_pets')
    return render(request, 'pets/delete_pet.html', {'pet': pet})

def logout_user(request):
    request.session.flush()
    messages.success(request, "Đăng xuất thành công.")
    return redirect('home')
