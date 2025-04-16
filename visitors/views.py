from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

# Create your views here.
from visitors.models import Visitor
from visitors.services import block_ip_in_firewall, is_super_admin, unblock_ip_in_firewall


def visitor_list(request):
    visitors = Visitor.objects.all().order_by('-first_visit')

    # Calcul des statistiques
    active_visitors = Visitor.objects.filter(is_blocked=False).count()
    blocked_visitors = Visitor.objects.filter(is_blocked=True).count()
    today = timezone.now() - timedelta(days=1)
    today_visitors = Visitor.objects.filter(first_visit__gte=today).count()

    return render(request, 'visitors/list.html', {
        'visitors': visitors,
        'active_visitors': active_visitors,
        'blocked_visitors': blocked_visitors,
        'today_visitors': today_visitors
    })


@user_passes_test(is_super_admin)
def block_visitor(request, visitor_id):
    visitor = get_object_or_404(Visitor, id=visitor_id)
    if not visitor.is_blocked:
        success, message = block_ip_in_firewall(visitor.ip_address)
        if success:
            visitor.is_blocked = True
            visitor.save(update_fields=["is_blocked"])
            messages.success(request, f"Utilisateur  {visitor.__str__()} bloqué avec succès")
        else:
            messages.error(request, f"Une erreur s'est produite lors du blocage de l' utilisateur | Trace:  {message}")
    return redirect('visitor_list')


@user_passes_test(is_super_admin)
def unblock_visitor(request, visitor_id):
    visitor_to_unblock = get_object_or_404(Visitor, id=visitor_id)
    if visitor_to_unblock.is_blocked:
        success, message = unblock_ip_in_firewall(visitor_to_unblock.ip_address)
        if success:
            visitor_to_unblock.is_blocked = False
            visitor_to_unblock.save(update_fields=["is_blocked"])
            messages.success(request, f"Utilisateur  {visitor_to_unblock.__str__()} bloqué avec succès")
        else:
            messages.error(request,
                           f"Une erreur s'est produite lors du déblocage de l' utilisateur | Trace:  {message}")

    return redirect('visitor_list')


@user_passes_test(is_super_admin)
def delete_visitor(request, visitor_id):
    visitor_to_delete = get_object_or_404(Visitor, id=visitor_id)
    if visitor_to_delete.is_blocked:
        success, message = unblock_ip_in_firewall(visitor_to_delete.ip_address)
        if not success:
            messages.error(request,
                           f"Une erreur s'est produite lors de la suppression de l' utilisateur | Trace:  {message}")
            return redirect('visitor_list')
        # Delete user
    visitor_name = visitor_to_delete.__str__()
    visitor_to_delete.delete()
    messages.success(request, f"Utilisateur  {visitor_name} supprimé avec succès")

    return redirect('visitor_list')
