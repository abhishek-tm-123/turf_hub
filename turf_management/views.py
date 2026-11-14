from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework import permissions

from turf_management.models import Turf
from turf_management.serializers import TurfSerializer

# Create your views here.

class TurfListCreateView(APIView):
    
    authentication_classes = [authentication.BasicAuthentication]
    
    permission_classes = [permissions.IsAdminUser]
    def get(self,request):
        qs = Turf.objects.all()
        serializer_instance = TurfSerializer(qs,many=True)
        return Response(serializer_instance.data)
    
    def post(self,request):
        form_data = request.data
        
        serializer_instance = TurfSerializer(data=form_data)
        
        if serializer_instance.is_valid():
            
            # cleaned_data = serializer_instance.validated_data
            
            # Turf.objects.create(**cleaned_data)
            
            serializer_instance.save() # work create() method inside serializer
            
            return Response(serializer_instance.data)
        
        else:
            
            return Response(serializer_instance.errors)
        

class TurfRetrieveUpdateDeleteView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
        
    permission_classes = [permissions.IsAdminUser]
    
    def get(self,request,pk=None):
        qs = Turf.objects.get(id=pk)
        
        serializer_instance = TurfSerializer(qs)
         
        return Response(serializer_instance.data)
    
    def put(self,request,pk=None):
        
        turf_object = Turf.objects.get(id=pk)
        
        form_data = request.data
        
        serializer_instance = TurfSerializer(data=form_data,instance=turf_object)
        
        if serializer_instance.is_valid():
            
            # cleaned_data = serializer_instance.validated_data
            
            # Turf.objects.filter(id=pk).update(**cleaned_data)
            
            serializer_instance.save() # work update() method inside serializer
            
            return Response(serializer_instance.data)
        
        else:
            
            return Response(serializer_instance.errors)
        
    def delete(self,request,pk=None):
        
        Turf.objects.filter(id=pk).delete()
        
        return Response({"message":"turf deleted ...."})