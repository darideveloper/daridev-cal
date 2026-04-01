from rest_framework import serializers
from .models import Event, EventType, Booking, EventAvailability, AvailabilitySlot, BusinessHours

class AvailabilitySlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailabilitySlot
        fields = ["weekday", "start_time", "end_time"]

class EventAvailabilitySerializer(serializers.ModelSerializer):
    slots = AvailabilitySlotSerializer(many=True, read_only=True)
    
    class Meta:
        model = EventAvailability
        fields = ["start_date", "end_date", "slots"]

class EventSerializer(serializers.ModelSerializer):
    availability_rules = EventAvailabilitySerializer(many=True, read_only=True)
    
    class Meta:
        model = Event
        fields = [
            "id", "title", "image", "description", 
            "detailed_description", "price", "duration_minutes", 
            "format_category", "availability_rules"
        ]

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            "id", "event", "client_name", "client_email", 
            "start_time", "end_time", "status"
        ]
        read_only_fields = ["end_time", "status"]

class BusinessHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessHours
        fields = ["weekday", "start_time", "end_time"]
