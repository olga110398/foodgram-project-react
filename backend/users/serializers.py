from rest_framework import serializers
from djoser.serializers import UserCreateSerializer

from recipes.models import Subscribe
from users.models import CustomUser


class ProfileSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Subscribe.objects.filter(follower=user,
                                        following=obj).exists()

class UserCreateSerialize(UserCreateSerializer):

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name',
                  'last_name', 'password')
