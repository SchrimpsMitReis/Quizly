from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for registering new users.
    Ensures email uniqueness and password confirmation.
    """
    
    confirmed_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirmed_password']
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'email': {
                'required': True
            }
        }

    def validate_confirmed_password(self, value):
        """
        Check if password and confirmed_password match.
        """
        password = self.initial_data.get('password')
        if password and value and password != value:
            raise serializers.ValidationError('Passwords do not match')
        return value

    def validate_email(self, value):
        """
        Ensure the email address is unique.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value

    def save(self):
        """
        Create and store a new user with a hashed password.
        """
        pw = self.validated_data['password']

        account = User(email=self.validated_data['email'], username=self.validated_data['username'])
        account.set_password(pw)
        account.save()
        return account
    

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom login serializer that authenticates users using
    email and password instead of username.
    """
        
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


    def __init__(self, *args, **kwargs):
        """
        Remove the default username field from the serializer.
        """
        super().__init__(*args, **kwargs)
        if "username" in self.fields:
            del self.fields["username"]

    
    def validate(self, attrs):
        """
        Validate user credentials and return JWT tokens if valid.
        """
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Ungültige Email oder Password")
          
        if not user.check_password(password):
            print(password)
            raise serializers.ValidationError("Ungültige Email oder Password")
        
        attrs["username"] = user.username
        data = super().validate(attrs)
        
        return data