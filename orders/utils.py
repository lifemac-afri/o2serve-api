from authentication.models import Worker
from django.db.models import Count
from django.utils import timezone
from django.db import models

def assign_waiter_to_order(order):
    available_workers = Worker.objects.filter(user__is_logged_in=True, user__role='waiter')
    
    if not available_workers:
        return None

    # Get the count of active orders for each worker
    worker_order_counts = available_workers.annotate(
        active_orders=Count('user__assigned_orders', filter=models.Q(user__assigned_orders__status='pending'))
    ).order_by('active_orders', 'last_order_assigned')

    assigned_worker = worker_order_counts.first()
    assigned_worker.last_order_assigned = timezone.now()
    assigned_worker.save()

    order.assigned_waiter = assigned_worker.user
    order.save()

    return assigned_worker.user
