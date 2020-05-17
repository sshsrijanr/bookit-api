from django.db import transaction
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, exceptions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from bookit.access.models import User, Profile
from bookit.access.serializers import ProfileSerializer
from .models import Language, Event, Booking
from .serializers import LanguageSerializer, EventSerializer, BookingSerializer


class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {"request": self.request}


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        user_data = request.data.get('user', None)
        if not user_data:
            raise exceptions.ValidationError("user key is required!")
        if not user_data.get('first_name', None):
            raise exceptions.ValidationError("user key does not contains first_name - is required!")
        if not user_data.get('last_name', None):
            raise exceptions.ValidationError("user key does not contains last_name -  is required!")
        if not user_data.get('email', None):
            raise exceptions.ValidationError("user key does not contains email -  is required!")
        if not user_data.get('mobile_number', None):
            raise exceptions.ValidationError("user key does not contains mobile_number -  is required!")
        if not user_data.get('id_card', None):
            raise exceptions.ValidationError("user key does not contains id_card -  is required!")
        res = User.objects.filter(email=user_data['email']).exists()

        if not res:
            user = User.objects.create(username=user_data['email'],
                                       first_name=user_data['first_name'],
                                       last_name=user_data['last_name'],
                                       email=user_data['email'])
            profile_data = {
                "user": str(user.id),
                "mobile_number": user_data['mobile_number'],
                "id_card": user_data['id_card']
            }
            serializer = ProfileSerializer(data=profile_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            user = User.objects.filter(email=user_data['email']).first()
            User.objects.filter(id=user.id).update(first_name=user_data['first_name'],
                                                   last_name=user_data['last_name'])
            try:
                profile = user.profile
                profile_data = {
                    "user": str(user.id),
                    "mobile_number": user_data['mobile_number'],
                    "id_card": user_data['id_card']
                }
                serializer = ProfileSerializer(data=profile_data, instance=profile)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            except Profile.DoesNotExist:
                profile_data = {
                    "user": str(user.id),
                    "mobile_number": user_data['mobile_number'],
                    "id_card": user_data['id_card']
                }
                serializer = ProfileSerializer(data=profile_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
        request.data['user'] = str(user.id)
        reg_type = request.data.get('registration_type', None)
        if not reg_type:
            raise exceptions.ValidationError('registration_type is required')
        if reg_type == 'self':
            request.data['number_of_tickets'] = 1
        number_of_tickets = request.data.get('number_of_tickets', None)
        event = request.data.get('event', None)
        event_obj = get_object_or_404(Event, pk=event)
        if number_of_tickets:
            booked_seats = event_obj.booking_set.aggregate(booked=Sum('number_of_tickets'))['booked']
            if event_obj.number_of_seats - booked_seats - number_of_tickets < 0:
                raise exceptions.ValidationError('Not enough seats available!')
        return super(BookingViewSet, self).create(request, *args, **kwargs)
