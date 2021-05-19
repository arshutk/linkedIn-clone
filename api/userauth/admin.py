from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from userauth.forms import UserAdminCreationForm, UserAdminChangeForm
from userauth.models import User, UserProfile, OTPModel


admin.site.register(OTPModel)



class UserProfileInline(admin.StackedInline):
    model       = UserProfile
    can_delete  = False
    

class UserAdmin(BaseUserAdmin):

    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ('email', 'admin',) # columns to show for each models object
    list_filter = ('admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('active','admin','staff',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'active','admin','staff')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
    inlines = (UserProfileInline,)


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)


