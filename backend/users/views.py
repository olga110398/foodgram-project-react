from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import CustomUser
from .serializers import (ChangePasswordSerializer, CreateUserSerializer,
                          ProfileSerializer)
from api.pagination import CustomPaginator


class UserViewSet(ModelViewSet):
    """Вьюсеты для модели User."""
    queryset = CustomUser.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (AllowAny, )
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    pagination_class = CustomPaginator

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ProfileSerializer
        return CreateUserSerializer

    @action(
        methods=['get', ],
        detail=False,
        url_path='me',
        permission_classes=[IsAuthenticated]
    )
    def my_profile(self, request):
        user = request.user
        serializer = ProfileSerializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=['post', ],
        detail=False,
        url_path='set_password',
        permission_classes=[IsAuthenticated],
    )
    def set_password(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'status': 'Пароль успешно изменен!'},
                            status=status.HTTP_204_NO_CONTENT)
        if user.is_anonymous:
            return Response({'detail':
                             'Учетные данные не были предоставлены.'},
                            status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
