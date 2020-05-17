from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import User, Profile
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    @action(methods=['GET'], detail=False, url_path='me')
    def me(self, request):
        content = {'request': self.request}
        return Response(self.serializer_class(instance=request.user, context=content).data,
                        status=200)
