from django.contrib import admin
from .models import Pet, User

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'owner', 'date_of_birth', 'is_available_for_adoption')
    list_filter = ('species', 'owner', 'is_available_for_adoption')
    search_fields = ('name', 'species', 'owner__username')
    actions = ['delete_selected']

    def delete_model(self, request, obj):
        # Ghi đè phương thức xóa nếu cần
        obj.delete()

    def delete_queryset(self, request, queryset):
        # Ghi đè phương thức xóa nhiều nếu cần
        queryset.delete()

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
