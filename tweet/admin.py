from django.contrib import admin
from .models import Tweet,Profile

admin.site.register(Tweet)

class ProfileAdmin(admin.ModelAdmin):
    fields = (
        'user',
        'get_username',
        'get_first_name',
        'get_email',
        'p_img',
        'dob',
        'country'
    )

    readonly_fields = (
        'get_username',
        'get_first_name',
        'get_email'
    )

    def get_username(self, obj):
        return obj.user.username

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_email(self, obj):
        return obj.user.email

    get_username.short_description = 'Username'
    get_first_name.short_description = 'First Name'
    get_email.short_description = 'Email'


admin.site.register(Profile, ProfileAdmin)