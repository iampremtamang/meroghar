from django.contrib import admin

from django.contrib import admin
from .models import Address, Home, Owner

class AddressAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Address instances.
    """
    list_display = ('street_address', 'city', 'state', 'postal_code', 'country')
    search_fields = ('street_address', 'city', 'state', 'postal_code', 'country')
    ordering = ('city', 'street_address')
    list_filter = ('state', 'type')


class HomeAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Home instances.
    """
    list_display = ('owner', 'address', 'date_of_purchase', 'ownership_percentage')
    search_fields = ('owner__user__first_name', 'owner__user__last_name', 'address__street_address', 'address__city')
    list_filter = ('date_of_purchase', 'ownership_percentage')
    ordering = ('address__city', 'address__street_address')


class OwnerAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Owner instances.
    """
    list_display = ('user', 'occupation', 'marital_status', 'spouse_name', 'address')
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'occupation', 'spouse_name', 'address__street_address')
    list_filter = ('marital_status', 'occupation')
    ordering = ('user__last_name', 'user__first_name')

# Registering models with the admin site
admin.site.register(Address, AddressAdmin)
admin.site.register(Home, HomeAdmin)
admin.site.register(Owner, OwnerAdmin)
