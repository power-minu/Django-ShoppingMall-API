from rest_framework import serializers, status
from rest_framework.exceptions import APIException

from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'item_name', 'stock_quantity', 'item_price']
        
    def validate_item_name(self, value):
        if Item.objects.filter(item_name=value).exists():
            raise DuplicateItemNameException()
        return value
    
    def update(self, instance, validated_data):
        print(validated_data)
        
        instance.item_name = validated_data.get('item_name', instance.item_name)
        instance.stock_quantity = validated_data.get('stock_quantity', instance.stock_quantity)
        instance.item_price = validated_data.get('item_price', instance.item_price)

        if not validated_data:
            raise UpdateBadRequestException()
        
        instance.save()
        return instance

class DuplicateItemNameException(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = '동일한 이름의 상품이 존재합니다.'
    default_code = 'conflict'
    
class UpdateBadRequestException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '잘못된 요청입니다.'
    default_code = 'bad request'