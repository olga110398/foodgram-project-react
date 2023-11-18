from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from djoser.serializers import SetPasswordSerializer, UserCreateSerializer
from rest_framework import serializers

from recipes.models import Subscribe
from .models import CustomUser


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


class CreateUserSerializer(UserCreateSerializer):

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'password')


class ChangePasswordSerializer(SetPasswordSerializer):
    new_password = serializers.CharField()
    current_password = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ('new_password', 'current_password')

    def validate(self, data):
        try:
            validate_password(data['new_password'])
        except django_exceptions.ValidationError as error:
            raise serializers.ValidationError(
                {'new_password': list(error.messages)}
            )
        return super().validate(data)

    def update(self, instance, validated_data):
        if not instance.check_password(validated_data['current_password']):
            raise serializers.ValidationError(
                {'current_password': 'Неправильный пароль.'}
            )
        if (validated_data['current_password']
           == validated_data['new_password']):
            raise serializers.ValidationError(
                {'new_password': 'Новый пароль должен отличаться от текущего.'}
            )
        instance.set_password(validated_data['new_password'])
        instance.save()
        return validated_data
