from django.db import models

from rest_framework.exceptions import ValidationError

class Item(models.Model):
    item_name = models.CharField(max_length=50, null=False)
    stock_quantity = models.IntegerField(default=0)
    item_price = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'item'
        
    def sub_stock(self, quantity, save=True):
        if self.stock_quantity - quantity < 0:
            raise ValidationError('재고가 부족합니다.')
        self.stock_quantity -= quantity
        if save:
            self.save()