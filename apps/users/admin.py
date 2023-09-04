from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.contrib.auth.models import Group

from apps.users.models import User, Basket, Mycard, Bankcard, Subscr, Coment, Favorites, Partners, Like, BasicUser


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        if bool(self.cleaned_data['email']):
            user.email = self.cleaned_data['email'];
        else:
            user.email = None;
        if 'password' in self.changed_data:
            user.set_password(self.cleaned_data["password"]);
        if commit:
            user.save()
        return user


fieldsets = (
        (None, {'fields': (
            'uniqueId',
            'logo',
            'email',
            'name',
            'user_type',
            'is_superuser',
            'is_staff',
            'is_active',
            'password',
            'resetPasswordUUID',
            'resetPasswordDate',
        )}),
        )


class CustomUserAdmin(UserAdmin):
    search_fields = ['email', 'name']
    add_form = UserCreationForm
    form = UserCreationForm
    list_display = ['name', 'uniqueId', 'email', 'user_type']
    list_display_links = ['name', 'email', 'uniqueId']
    ordering = ("-id",)
    list_filter = ('is_superuser', 'is_staff', 'is_active', 'created_date', 'user_type', )

    fieldsets = fieldsets

    add_fieldsets = fieldsets


class BasicUserAdmin(admin.ModelAdmin):
    list_display = ['name', 'last_name', 'email', 'uniqueId', 'created_date']
    search_fields = ['email', 'name', 'last_name']
    list_display_links = ['name', 'last_name', 'email', 'uniqueId']

    fieldsets = (
        (None, {'fields': (
            'uniqueId',
            'logo',
            'email',
            'name',
            'user_type',
            'phone_number',
            'dob',
            'password',
            'resetPasswordUUID',
            'resetPasswordDate',
        )}),
    )


class PartnersAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'activity_type', 'uniqueId', 'created_date')
    list_display_links = list_display
    search_fields = ('email', 'name', 'activity_type', 'address')


admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)
admin .site.register(Basket)
admin.site.register(Mycard)
admin.site.register(Bankcard)
admin.site.register(Subscr)
admin.site.register(Coment)
# admin.site.register(Like);
admin.site.register(Favorites)
admin.site.register(Partners, PartnersAdmin)
admin.site.register(BasicUser, BasicUserAdmin)


@admin.register(Like)
class Favorites(admin.ModelAdmin):
    list_display = ('title', 'name')
