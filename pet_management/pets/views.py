from django.shortcuts import render, redirect
from .models import User, Pet
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.hashers import make_password, check_password

# Quỹ thú cưng
PET_FUND_BALANCE = 0

def home(request):
    return render(request, 'pets/home.html')  # Đảm bảo rằng đường dẫn là 'pets/home.html'

def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            hashed_password = make_password(password)  # Mã hóa mật khẩu
            user = User.objects.create(username=username, password=hashed_password)
            messages.success(request, f"Đăng ký thành công cho {username}")
            return redirect('login_user')
    else:
        form = RegisterForm()
    return render(request, 'pets/register.html', {'form': form})  # Đảm bảo rằng đường dẫn là 'pets/register.html'

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.filter(username=username).first()
            if user and check_password(password, user.password):  # Kiểm tra mật khẩu đã mã hóa
                request.session['user_id'] = user.id
                messages.success(request, f"Chào mừng {username}")
                return redirect('home')
            else:
                messages.error(request, "Sai tên đăng nhập hoặc mật khẩu.")
    else:
        form = LoginForm()
    return render(request, 'pets/login.html', {'form': form})  # Đảm bảo rằng đường dẫn là 'pets/login.html'

def add_pet(request):
    if 'user_id' not in request.session:
        return redirect('login_user')
    
    if request.method == 'POST':
        name = request.POST['name']
        species = request.POST['species']
        user = User.objects.get(id=request.session['user_id'])
        pet = Pet.objects.create(name=name, species=species, owner=user)
        messages.success(request, f"Đã thêm thú cưng: {pet.name}")
        return redirect('view_pets')
    return render(request, 'pets/add_pet.html')  # Đảm bảo rằng đường dẫn là 'pets/add_pet.html'

def view_pets(request):
    if 'user_id' not in request.session:
        return redirect('login_user')
    
    user = User.objects.get(id=request.session['user_id'])
    pets = Pet.objects.filter(owner=user)
    return render(request, 'pets/view_pets.html', {'pets': pets})  # Đảm bảo rằng đường dẫn là 'pets/view_pets.html'

def adopt_pet(request):
    if 'user_id' not in request.session:
        return redirect('login_user')
    
    if request.method == 'POST':
        pet_id = request.POST['pet_id']
        pet = Pet.objects.get(id=pet_id)
        user = User.objects.get(id=request.session['user_id'])
        
        if pet.owner is not None:
            messages.error(request, f"Thú cưng {pet.name} đã có chủ.")
        else:
            pet.owner = user
            pet.save()
            messages.success(request, f"{user.username} đã nhận {pet.name}")
        return redirect('view_pets')

    # Lấy danh sách thú cưng chưa có chủ
    pets = Pet.objects.filter(owner=None)
    return render(request, 'pets/adopt_pet.html', {'pets': pets})


def donate_to_fund(request):
    global PET_FUND_BALANCE
    if request.method == 'POST':
        amount = float(request.POST['amount'])
        if amount > 0:
            PET_FUND_BALANCE += amount
            messages.success(request, f"Đã đóng góp {amount} vào quỹ thú cưng.")
        else:
            messages.error(request, "Số tiền đóng góp phải lớn hơn 0.")
    return render(request, 'pets/donate.html')  # Đảm bảo rằng đường dẫn là 'pets/donate.html'

def view_fund_balance(request):
    global PET_FUND_BALANCE
    return render(request, 'pets/view_balance.html', {'balance': PET_FUND_BALANCE})  # Đảm bảo rằng đường dẫn là 'pets/view_balance.html'

# Đăng xuất
def logout_user(request):
    try:
        del request.session['user_id']
        messages.success(request, "Đăng xuất thành công.")
    except KeyError:
        pass  # Nếu người dùng chưa đăng nhập thì không có gì xảy ra
    return redirect('home')
