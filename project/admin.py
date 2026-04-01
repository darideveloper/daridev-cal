from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect
from django.urls import reverse
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.admin import ModelAdmin
from unfold.sites import UnfoldAdminSite
from unfold.decorators import action

class PublicAdminSite(UnfoldAdminSite):
    pass

class TenantAdminSite(UnfoldAdminSite):
    pass

public_admin_site = PublicAdminSite(name="admin")
tenant_admin_site = TenantAdminSite(name="admin")

try:
    admin.site.unregister(User)
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass

class ModelAdminUnfoldBase(ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True
    list_filter_sheet = False
    change_form_show_cancel_button = True
    
    actions_row = ["edit"]

    @action(description="Edit", permissions=["change"])
    def edit(self, request, object_id):
        return redirect(reverse(f"admin:{self.model._meta.app_label}_{self.model._meta.model_name}_change", args=[object_id]))

class UserAdmin(BaseUserAdmin, ModelAdminUnfoldBase):
    # Forms loaded from `unfold.forms`
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

class GroupAdmin(BaseGroupAdmin, ModelAdminUnfoldBase):
    pass

public_admin_site.register(User, UserAdmin)
public_admin_site.register(Group, GroupAdmin)
