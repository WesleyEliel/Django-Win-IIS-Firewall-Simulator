# Register your models here.

from django.contrib import admin
from django.contrib import messages

from .models import Visitor
from .services import block_ip_in_firewall, unblock_ip_in_firewall


@admin.action(description="Block selected IPs via Windows Firewall")
def block_ips(modeladmin, request, queryset):
    for visitor in queryset:
        if not visitor.is_blocked:

            success, message = block_ip_in_firewall(visitor.ip_address)
            if success:
                visitor.is_blocked = True
                visitor.save(update_fields=["is_blocked"])
                modeladmin.message_user(request, f"Successfully blocked {visitor.ip_address}", messages.SUCCESS)
            else:
                modeladmin.message_user(request, f"Failed to block {visitor.ip_address} {message}", messages.ERROR)
    block_ips.short_description = "Block selected visitors (via Windows Firewall)"


@admin.action(description="Unblock selected IPs from Windows Firewall")
def unblock_ips(modeladmin, request, queryset):
    for visitor in queryset:
        if visitor.is_blocked:
            success, message = unblock_ip_in_firewall(visitor.ip_address)
            if success:
                visitor.is_blocked = False
                visitor.save(update_fields=["is_blocked"])
                modeladmin.message_user(request, f"Successfully unblocked {visitor.ip_address}", messages.SUCCESS)
            else:
                modeladmin.message_user(request, f"Failed to unblock {visitor.ip_address} | {message}", messages.ERROR)
    unblock_ips.short_description = "Unblock selected visitors (from Windows Firewall)"


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'first_visit', 'user_agent', 'is_blocked')
    actions = [block_ips, unblock_ips]
