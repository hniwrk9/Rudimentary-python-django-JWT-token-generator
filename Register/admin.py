from django.contrib import admin

# Register your models here.
from .models.staff import Staff
from .models.users import User
from .models.role import Role

# Add fields to display on admin panel over here:
class AdminStaff(admin.ModelAdmin):
    list_display = ['id','csid','fname','lname','email','active', 'role']

class AdminUser(admin.ModelAdmin):
    list_display = ['id','email','ran','staff']

class AdminRole(admin.ModelAdmin):
    list_display = ['id','name']


# Send the models and display parameter classes to the admin panel
admin.site.register(Staff, AdminStaff)
admin.site.register(User, AdminUser)
admin.site.register(Role, AdminRole)


