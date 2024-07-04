from rest_framework import serializers, status
from rest_framework.exceptions import APIException

from .models import Address, Member

class AdressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['city', 'street', 'zipcode']

class MemberSerializer(serializers.ModelSerializer):
    address = AdressSerializer()

    class Meta:
        model = Member
        fields = ['id', 'name', 'address']
        
    def validate_name(self, value):
        if Member.objects.filter(name=value).exists():
            raise DuplicateMemberNameException()
        return value

    def create(self, validated_data):
        address_validated_data = validated_data.pop('address')
        member = Member.objects.create(**validated_data)
        Address.objects.create(member=member, **address_validated_data)
        return member
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)

        address_data = validated_data.get('address', None)
        
        if not validated_data:
            raise UpdateBadRequestException()
        if address_data:
            address_serializer = self.fields['address']
            address_instance = instance.address
            address_serializer.update(address_instance, address_data)
            
        instance.save()
        return instance
    
class DuplicateMemberNameException(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = '동일한 이름의 회원이 존재합니다.'
    default_code = 'conflict'

class UpdateBadRequestException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '잘못된 요청입니다.'
    default_code = 'bad request'