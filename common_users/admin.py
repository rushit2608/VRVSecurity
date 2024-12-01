from django.contrib import admin
from .models import Users,Role,Permission

admin.site.register(Users)
admin.site.register(Role)
admin.site.register(Permission)
