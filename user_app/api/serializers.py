
# from django.contrib.auth.models import User
# from rest_framework import serializers

# class RegistrationSerializer(serializers.ModelSerializer):
#     password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password', 'password2']
#         extra_kwargs = {
#             'password': {'write_only': True}
#             }
#         def save(self):
#             password = self.validated_data['password']
#             password2 = self.validated_data['password2']
#             if password != password2:
#                 raise serializers.ValidationError({'error': 'P1 and P2 should be the same'})
#             if User.objects.filter(email=self.validated_data['email']).exists():
#                 raise serializers.ValidationError({'error': 'Email already exists'})
#             account = User(email=self.validated_data['email'], username=self.validated_data['username'])
#             account.set_password(password)
#             account.save()
#             return account



from django.contrib.auth.models import User
from rest_framework import serializers

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')

        if password != password2:
            raise serializers.ValidationError({'error': 'P1 and P2 should be the same'})

        return data

    def create(self, validated_data):
        validated_data.pop('password2', None)  # Remove 'password2' from validated_data
        user = User.objects.create_user(**validated_data)
        return user
