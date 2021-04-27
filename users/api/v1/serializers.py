from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'password',
                  'is_staff', 'is_active']

        read_only_fields = ('last_name', 'is_staff', 'is_active')

        extra_kwargs = {'password': {'write_only': True, 'min_length': 6}}
