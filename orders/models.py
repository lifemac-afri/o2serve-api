import uuid
from django.db import models
from customers.models import Customer
from tables.models import Table
from menu.models import MenuItem
from django.db.models.signals import post_delete
from django.dispatch import receiver

class Order(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'), ('completed', 'Completed'), ('canceled', 'Canceled')]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_number = models.IntegerField(unique=True, blank=True, null=True)  # IntegerField for auto-increment logic
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.order_number is None:
         
            last_order = Order.objects.all().order_by('order_number').last()
            if last_order:
                self.order_number = last_order.order_number + 1
            else:
                self.order_number = 1

        # Compute total amount from order items
        self.update_total_amount()
        super().save(*args, **kwargs)

    def update_total_amount(self):
        self.total_amount = sum(item.menu_item.price * item.quantity for item in self.items.all())
        print(f"Total amount updated to: {self.total_amount}")

    def __str__(self) -> str:
        return f"Order {self.order_number} for table {self.table}"


class  OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def save(self, *args, **kwargs):       
        super().save(*args, **kwargs)       
        self.order.update_total_amount()
        self.order.save()

    def __str__(self) -> str:
        return f"Order Item in {self.order}"



@receiver(post_delete, sender=OrderItem)
def update_order_total_on_delete(sender, instance, **kwargs):
    instance.order.update_total_amount()
    instance.order.save()
