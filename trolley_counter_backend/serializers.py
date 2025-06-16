from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth.models import User
from rest_framework import serializers


class CurrentUserSerializer(UserDetailsSerializer):
    is_admin = serializers.SerializerMethodField()

    def get_is_admin(request, obj):
        """
        Determine if the current user is an admin
        """
        superusers = User.objects.filter(is_superuser=True)
        if obj in superusers:
            return True
        return False

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            'is_admin',
        )
