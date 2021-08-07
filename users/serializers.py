from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser

        fields = [

            'id', 'name', 'email', 'password',
            'language', 'currency', 'phone_number'
        ]
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()

        return instance


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser

        fields = [

            'name', 'email', 'language',
            'currency', 'phone_number'
        ]
