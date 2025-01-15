from django.contrib import admin
from .models import User, Pet  # Nhập các model cần quản lý

# Đăng ký User model vào admin
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'password')  # Hiển thị tên người dùng và mật khẩu (chú ý: không khuyến khích hiển thị mật khẩu trực tiếp)
    search_fields = ('username',)  # Thêm chức năng tìm kiếm theo tên người dùng
    list_filter = ('username',)  # Thêm bộ lọc theo tên người dùng

# Đăng ký Pet model vào admin
@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'owner')  # Hiển thị tên thú cưng, loài, và chủ sở hữu
    search_fields = ('name', 'species')  # Thêm chức năng tìm kiếm theo tên và loài thú cưng
    list_filter = ('species', 'owner')  # Thêm bộ lọc theo loài thú cưng và chủ sở hữu

# Hoặc có thể đăng ký thủ công nếu không dùng decorator
# admin.site.register(User, UserAdmin)
# admin.site.register(Pet, PetAdmin)
