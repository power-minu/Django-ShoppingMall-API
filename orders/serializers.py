from rest_framework import serializers

class OrderItemSerializer(serializers.Serializer):
    item_id = serializers.IntegerField(source='item.id')
    item_name = serializers.CharField(source='item.item_name')
    item_price = serializers.IntegerField(source='item.item_price')
    count = serializers.IntegerField()

class OrdersSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    member_id = serializers.IntegerField(source='member.id')
    items = OrderItemSerializer(source='orderitem_set', many=True)
    order_date = serializers.DateTimeField()
    status = serializers.CharField()

class OrderItemRequestDTO(serializers.Serializer):
    item_id = serializers.IntegerField()
    count = serializers.IntegerField()

class OrderRequestDTO(serializers.Serializer):
    member_id = serializers.IntegerField()
    items = OrderItemRequestDTO(many=True)