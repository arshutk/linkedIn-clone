from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User, UserProfile, UserExperience

class UserProfileInline(admin.StackedInline):
    model       = UserProfile
    can_delete  = False
    
class UserExperienceInline(admin.StackedInline):
    model       = UserExperience
    can_delete  = False

class UserAdmin(BaseUserAdmin):

    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ('email', 'admin',)
    list_filter = ('admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('active','admin','staff',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
    inlines = (UserProfileInline, UserExperienceInline)


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
