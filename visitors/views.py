from datetime import timedelta

from django.shortcuts import render
from django.utils import timezone

# Create your views here.
from visitors.models import Visitor


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
