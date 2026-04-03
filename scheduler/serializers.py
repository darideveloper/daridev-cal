from django.conf import settings
from django.utils.translation import gettext as _
from rest_framework import serializers
from .models import Event, EventType, Booking, EventAvailability, AvailabilitySlot, BusinessHours, EventDateOverride, CompanyProfile

class AvailabilitySlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailabilitySlot
        fields = ["weekday", "start_time", "end_time"]

class EventAvailabilitySerializer(serializers.ModelSerializer):
    slots = AvailabilitySlotSerializer(many=True, read_only=True)
    
    class Meta:
        model = EventAvailability
        fields = ["start_date", "end_date", "slots"]

class EventDateOverrideSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventDateOverride
        fields = ["date", "is_available", "start_time", "end_time"]

class EventSerializer(serializers.ModelSerializer):
    availability_rules = EventAvailabilitySerializer(many=True, read_only=True)
    date_overrides = EventDateOverrideSerializer(many=True, read_only=True)
    event_type_title = serializers.CharField(source="event_type.title", read_only=True)
    
    class Meta:
        model = Event
        fields = [
            "id", "title", "event_type_title", "image", "description", 
            "detailed_description", "price", "duration_minutes", 
            "availability_rules", "date_overrides"
        ]

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # Apply i18n translation to dynamic content
        ret["title"] = _(instance.title)
        if instance.description:
            ret["description"] = _(instance.description)
        if "event_type_title" in ret:
            ret["event_type_title"] = _(instance.event_type.title)
        return ret

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            "id", "event", "client_name", "client_email", "client_phone",
            "start_time", "end_time", "status"
        ]
        read_only_fields = ["end_time", "status"]

class BusinessHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessHours
        fields = ["weekday", "start_time", "end_time"]

class CompanyConfigSerializer(serializers.Serializer):
    brand_color = serializers.CharField()
    logo = serializers.ImageField()
    currency = serializers.CharField()
    contact_email = serializers.EmailField()
    contact_phone = serializers.CharField()
    company_name = serializers.CharField()
    timezone = serializers.CharField()
