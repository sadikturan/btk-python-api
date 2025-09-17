from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email']

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(help_text="Kullanıcı email adresiniz. Örneğin example@example.com")
    password = serializers.CharField(help_text="Kullanıcı şifreniz. Şifreniz en az 7 karakter olmalıdır.")

class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(
        required=True, 
        error_messages={"required":"Ad zorunlu.", "blank": "Ad boş olamaz"})
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id','email','password','password2','first_name','last_name','phone',)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password':'Passwords do not match'})
        return attrs
    
    def validate_phone(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Telefon numarası sadece rakamlardan oluşmalıdır.")
        
        if len(value) < 10:
            raise serializers.ValidationError("Telefon numarası en az 10 haneli olmalıdır.")
        
        return value
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        # Token.objects.create(user=user)
        return user

class UserAdminSerializer(serializers.ModelSerializer):
    role = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "phone", "role"]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["role"] = "admin" if instance.is_superuser else "user"
        return rep

    def update(self, instance, validated_data):
        role = validated_data.pop("role", None)
        instance = super().update(instance, validated_data)

        if role:
            if role == "admin":
                instance.is_superuser = True
                instance.is_staff = True
            elif role == "user":
                instance.is_superuser = False
                instance.is_staff = False
            instance.save()

        return instance