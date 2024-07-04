from django.db import models
from members.models import Member
from items.models import Item

# Create your models here.

class Orders(models.Model):
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, default="P")
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    
    items = models.ManyToManyField(Item, through='OrderItem')
    
    class Meta:
        db_table = 'orders'
        
class OrderItem(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'order_item'