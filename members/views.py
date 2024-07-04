from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.http import Http404

from members.models import Member
from members.serializers import MemberSerializer

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if not queryset.exists():
            raise Http404("등록된 회원이 없습니다.")

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        self.perform_destroy(self.get_object())
        return Response(status=status.HTTP_200_OK)
    
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except:
            raise Http404("존재하지 않는 회원입니다.")
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)