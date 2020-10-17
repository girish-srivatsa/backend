from django.contrib import admin
from .models import UserMy,Courses,Course,Messages,Token

admin.site.register(UserMy)
admin.site.register(Courses)
admin.site.register(Course)
admin.site.register(Messages)
admin.site.register(Token)