from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.request import Request
from django.http import Http404

from items.models import Item
from members.models import Member
from .models import Orders, OrderItem
from orders.serializers import OrderRequestDTO, OrdersSerializer

class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer
    
    def list(self, request: Request):
        if member_id := request.query_params.get('memberId', None):
            try:
                getMember = Orders.objects.get(id=member_id)
            except Orders.DoesNotExist:
                raise Http404('존재하지 않는 회원입니다.')
            orders = Orders.objects.filter(member_id=member_id)
        else:
            orders = Orders.objects.none()

        serializer = OrdersSerializer(orders, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = OrderRequestDTO(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        
        try:
            member = Member.objects.get(id=data['member_id'])
        except Member.DoesNotExist:
            raise ValidationError('존재하지 않는 회원입니다.')
        
        order = Orders(member=member)
        order_items = []
        items = []
        for order_item_data in data['items']:
            try:
                item = Item.objects.get(id=order_item_data['item_id'])
            except:
                raise ValidationError('존재하지 않는 상품입니다.')
            
            item.sub_stock(order_item_data['count'], save=False)
            items.append(item)
            order_items.append(OrderItem(
                    order=order,
                    item=item,
                    count=order_item_data['count']))
        
        order.save()
        for order_item in order_items:
            order_item.save()
        for item in items:
            item.save()
        
        serializer = OrdersSerializer(order)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except:
            raise Http404("존재하지 않는 주문입니다.")
        
        print(instance)
        instance.status = "C"
        instance.save()
        
        serializer = OrdersSerializer(instance)
        return Response(serializer.data)