from rest_framework import serializers

from reservation.models import Booking
from turf_management.models import Turf

from datetime import datetime

class BookingSerializer(serializers.Serializer):
    id = serializers.CharField(read_only = True)
    name = serializers.CharField()
    phone = serializers.CharField()
    email = serializers.EmailField()
    turf = serializers.IntegerField()
    match_date = serializers.DateField()
    duration = serializers.IntegerField()
    start_time = serializers.TimeField()
    end_time = serializers.TimeField(read_only=True)
    amount = serializers.DecimalField(max_digits=10,decimal_places=2,read_only=True)
    
    def create(self, validated_data):
        return Booking.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        
        for attribute,value in validated_data.items():
            setattr(instance,attribute,value)
        
        return instance
    
    def validate(self, validated_data):
        
        duration = validated_data.get("duration")
        
        if duration not in range(1,5):
            raise serializers.ValidationError("invalid duration: duration should be in range of 1-4")

        turf_id = validated_data.get("turf")
        
        if not Turf.objects.filter(id=turf_id).exists():
            raise serializers.ValidationError("turf does not exists")
        
        match_date = validated_data.get("match_date")
        
        
        if match_date < datetime.today().date():
            
            raise serializers.ValidationError("invalid date")
        
        
        
        
        return validated_data
    