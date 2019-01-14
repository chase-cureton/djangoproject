from django.contrib.auth import update_session_auth_hash

from rest_framework import serializers

from authentication.models import Account


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Account
        fields = ('id', 'email', 'username', 'created_at', 'updated_at',
                  'first_name', 'last_name', 'tagline', 'password',
                  'confirm_password',
                 )
        read_only_fields = ('created_at', 'updated_at',)

        def create(self, validated_data):
            return Account.object.create(**validated_data)

        def update(self, instance, validated_data):
            instance.username = validated_data.get('username', instance.username)
            instance.tagline = validated_data.get('tagline', instance.tagline)

            instance.save()

            password = validated_data.get('password', None)
            confirm_password = validated_data.get('confirm_password', None)

            if password and confirm_password == confirm_password:
                instance.set_password(password)
                instance.save()

            # When a user's password is updated, their session auth hash must be explicitly updated.
            # If this is not done, the user will not be authenticated on their next request and will have to log in again
            # tutorial says: self.context (gives error)
            update_session_auth_hash(instance.context.get('request'), instance)

            return instance