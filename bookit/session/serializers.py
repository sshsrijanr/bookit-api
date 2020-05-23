from django.db.models import Sum
from rest_framework import serializers

from bookit.access.serializers import UserSerializer
from bookit.common.serializers import AttachmentSerializer

from .models import Booking, Event, Language, Tags


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    tags_details = TagsSerializer(source='tags', many=True, read_only=True)
    languages_details = LanguageSerializer(source='languages',
                                           many=True,
                                           read_only=True)
    image_details = serializers.SerializerMethodField()
    available_seats = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = '__all__'

    def get_image_details(self, instance):
        context = self.context
        return AttachmentSerializer(instance.image, context=context).data

    def get_available_seats(self, instance):
        booked_seats = instance.booking_set.aggregate(
            booked=Sum('number_of_tickets'))['booked']
        if booked_seats is None:
            booked_seats = 0
        return int(instance.number_of_seats - booked_seats)


class EventDetailSerializer(EventSerializer):
    views_count = serializers.SerializerMethodField()

    def get_views_count(self, obj):
        obj.views_count += 1
        obj.save()
        return obj.views_count


class BookingSerializer(serializers.ModelSerializer):
    event_details = EventSerializer(source='event', read_only=True)
    user_details = UserSerializer(source='user', read_only=True)
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = '__all__'

    def get_total_amount(self, obj):
        return int(obj.number_of_tickets) * int(obj.event.cost_per_person)
