from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework import authentication
from rest_framework import permissions
from rest_framework.response import Response

from reservation.serializers import BookingSerializer
from reservation.models import Booking

from datetime import datetime,timedelta,time

from turf_management.models import Turf
# Create your views here.

class BookingCreateView(APIView):
    
    authentication_classes = [authentication.BasicAuthentication]
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self,request):
        
        form_data = request.data
        
        serializer_instance = BookingSerializer(data =form_data)
        
        if serializer_instance.is_valid():
            
            cleaned_data = serializer_instance.validated_data
            
            match_date = cleaned_data.get("match_date")
            
            start_time = cleaned_data.get("start_time")
            
            duration = cleaned_data.get("duration")
            
            end_date_time = datetime.combine(match_date,start_time)+timedelta(hours=duration)
            
            end_time = end_date_time.time()
            
            turf_id = cleaned_data.get("turf")
            
            turf_object = Turf.objects.get(id=turf_id)
            
            if start_time > time(18,0):
                amount = turf_object.night_price*duration
            else:
                amount = turf_object.day_price*duration
                
            booking_object = Booking.objects.filter(
                turf = turf_id,
                match_date = match_date,
                start_time__lt = end_time,
                end_time__gt = start_time
                
            )
            
            if booking_object.exists():
                return Response({"message":"slot not available"})
            
            serializer_instance.save(end_time=end_time,amount=amount)
            return Response(serializer_instance.data)
        else:
            return Response(serializer_instance.errors)
    

class BookingRetrieveUpdateDeleteView(APIView):
    
    authentication_classes = [authentication.BasicAuthentication]
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self,request,pk=None):
        
        qs = Booking.objects.get(id=pk)
        
        serializer_instance = BookingSerializer(qs)
        
        return Response(serializer_instance.data)
    
    def put(self,request,pk=None):
        
        form_data = request.data
        
        booking_object = Booking.objects.get(id=pk)
        
        serializer_instance = BookingSerializer(data=form_data,instance=booking_object)
        
        if serializer_instance.is_valid():
            
            serializer_instance.save()
            
            return Response(serializer_instance.data)
        
    def delete(self,request,pk=None):
        
        Booking.objects.filter(id=pk).delete()
        
        return Response({"message":"deleted...."})
    
class BookingSummaryView(APIView):
    def post(self,request):
        form_data = request.data
        
        turf = form_data.get("turf")
        
        match_date = datetime.strptime(form_data.get("match_date"),"%Y-%m-%d")
        
        bookings = Booking.objects.filter(turf=turf,match_date=match_date)
        
        serializer_instance = BookingSerializer(bookings,many=True)
        
        return Response(serializer_instance.data)