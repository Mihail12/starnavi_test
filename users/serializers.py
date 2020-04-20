from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'email', 'first_name', 'last_name', 'password', 'username', 'guid')
        extra_kwargs = {'password': {'write_only': True}, 'guid': {'read_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
