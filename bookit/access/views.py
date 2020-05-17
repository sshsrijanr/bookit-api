from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import User, Profile
from .serializers import UserSerializer, ProfileSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.data.get('profile', None):
            profile_data = request.data.get('profile', None)
            serializer = ProfileSerializer(instance=instance.profile, data=profile_data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return super(UserViewSet, self).partial_update(request, *args, **kwargs)

    @action(methods=['GET'], detail=False, url_path='me')
    def me(self, request):
        content = {'request': self.request}
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            Profile.objects.create(user=request.user)
        return Response(self.serializer_class(instance=request.user, context=content).data,
                        status=200)
