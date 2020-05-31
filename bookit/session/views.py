import json
from django.db import transaction
from django.db.models import Sum, Count
from django.db.models.functions import Cast, ExtractMonth, ExtractYear
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from bookit.access.models import Profile, User
from bookit.access.serializers import ProfileSerializer

from .models import Booking, Event, Language, Tags
from .serializers import (BookingSerializer, EventSerializer,
                          EventDetailSerializer, LanguageSerializer,
                          TagsSerializer)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]


class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['number_of_seats', 'languages', 'city']
    search_fields = ['title', 'city']
    ordering_fields = ['views_count', 'cost_per_person', 'start_time']

    def get_serializer_context(self):
        return {"request": self.request}

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EventDetailSerializer
        else:
            return EventSerializer

    def get_queryset(self):
        tags = self.request.query_params.get('tags', None)
        if tags:
            tags = json.loads(tags)
            self.queryset = self.queryset.filter(tags__in=tags)
        is_admin = self.request.query_params.get('is_admin', None)
        if is_admin and json.loads(is_admin) == True:
            return self.queryset
        else:
            return self.queryset.exclude(start_time__lte=timezone.now())


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['event']

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        user_data = request.data.get('user', None)
        if not user_data:
            raise exceptions.ValidationError("user key is required!")
        if not user_data.get('first_name', None):
            raise exceptions.ValidationError(
                "user key does not contains first_name - is required!")
        if not user_data.get('last_name', None):
            raise exceptions.ValidationError(
                "user key does not contains last_name -  is required!")
        if not user_data.get('email', None):
            raise exceptions.ValidationError(
                "user key does not contains email -  is required!")
        if not user_data.get('mobile_number', None):
            raise exceptions.ValidationError(
                "user key does not contains mobile_number -  is required!")
        if not user_data.get('id_card', None):
            raise exceptions.ValidationError(
                "user key does not contains id_card -  is required!")
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
            User.objects.filter(id=user.id).update(
                first_name=user_data['first_name'],
                last_name=user_data['last_name'])
            try:
                profile = user.profile
                profile_data = {
                    "user": str(user.id),
                    "mobile_number": user_data['mobile_number'],
                    "id_card": user_data['id_card']
                }
                serializer = ProfileSerializer(data=profile_data,
                                               instance=profile)
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
            booked_seats = event_obj.booking_set.aggregate(
                booked=Sum('number_of_tickets'))['booked']
            if booked_seats is None:
                booked_seats = 0
            if event_obj.number_of_seats - booked_seats - number_of_tickets < 0:
                raise exceptions.ValidationError('Not enough seats available!')
        return super(BookingViewSet, self).create(request, *args, **kwargs)


@api_view(['GET'])
def booking_type_stats(request):
    results = Booking.objects.values('registration_type').annotate(
        type_count=Count('id')).order_by('registration_type').values(
            'registration_type', 'type_count')
    return Response(results, status=200)


@api_view(['GET'])
def booking_event_stats(request, event):
    event = get_object_or_404(Event, pk=event)
    results = Booking.objects.filter(
        event=event).values('registration_type').annotate(
            type_count=Count('id')).order_by('registration_type').values(
                'registration_type', 'type_count')
    return Response(results, status=200)


@api_view(['GET'])
def monthly_booking_stats(request):
    results = Booking.objects.annotate(
        month=ExtractMonth('event__start_time'),
        year=ExtractYear('event__start_time')).values(
            'month', 'year',
            'registration_type').annotate(type_count=Count('id')).order_by(
                'year', 'month').values('month', 'year', 'registration_type',
                                        'type_count')
    return Response(results, status=200)