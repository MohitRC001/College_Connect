from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import *


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'is_staff', 'is_active')


class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'uid', 'mobile', 'course')

class FollowRequestAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'status')


# @admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

admin.site.register(Skill, SkillAdmin)


# @admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

admin.site.register(Interest, InterestAdmin)

# @admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'years')
    search_fields = ('title',)

admin.site.register(Experience, ExperienceAdmin)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(FollowRequest, FollowRequestAdmin)