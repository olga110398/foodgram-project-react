from djoser.views import UserViewSet
from rest_framework.filters import SearchFilter
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from .models import CustomUser
from .serializers import ProfileSerializer
from api.pagination import CustomPaginator


class UserViewSet(UserViewSet):
    """Вьюсеты для модели User."""
    queryset = CustomUser.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (AllowAny, IsAuthenticatedOrReadOnly)
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    pagination_class = CustomPaginator

    def get_permissions(self):
        if self.action == 'me':
            self.permission_classes = (IsAuthenticated, )
        return super().get_permissions()
