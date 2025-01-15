from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from pets import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout'),
    path('add-pet/', views.add_pet, name='add_pet'),
    path('view-pets/', views.view_pets, name='view_pets'),
    path('adopt-pet/', views.adopt_pet, name='adopt_pet'),
    path('donate/', views.donate_to_fund, name='donate_to_fund'),
    path('view-balance/', views.view_fund_balance, name='view_fund_balance'),
    path('edit-pet/<int:pet_id>/', views.edit_pet, name='edit_pet'),  # Route chỉnh sửa
    path('delete-pet/<int:pet_id>/', views.delete_pet, name='delete_pet'),  # Route xóa
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
