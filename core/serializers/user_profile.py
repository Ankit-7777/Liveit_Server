from rest_framework import serializers
from core.models import UserProfile
from rest_framework.validators import ValidationError
from core.utils import Utils
from rest_framework.validators import UniqueValidator
import re
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.password_validation import validate_password
from django.db.models.functions import Lower
from django.utils import timezone
from datetime import date
from rest_framework.exceptions import NotFound

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'id',
            'email',
            'full_name',
            'phone',
            'is_active',
            'is_staff',
            'is_superuser',
            'created_at',
            'updated_at',
            'role'
        ]
        read_only_fields = ['email', 'is_active', 'is_staff', 'is_superuser', 'created_at', 'updated_at']
 
class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password=serializers.CharField(style={'input_type':'password'},write_only='True')
    class Meta:
        model=UserProfile
        fields= '__all__'
        
        extra_kwargs={
            'password':{'write_only':True}
        }
    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"
        if password != confirm_password:
            raise serializers.ValidationError("Password and Confirm Password Must Be Same")
        elif not re.match(pattern, password):
            raise serializers.ValidationError("Password must contain at least eight characters with a digit, an uppercase letter, a lowercase letter, and a special character")
        return attrs
    
    def create(self,validated_data):
        return UserProfile.objects.create_user(**validated_data)

class UserLoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model = UserProfile
        fields = ['email','password']
    
    def validate(self,attrs):
     
        email=attrs.get('email')
        user=UserProfile.objects.filter(email=email)        
        if  not user.exists():
                    raise serializers.ValidationError({'email':'The email is not valid'})
        return attrs

class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("The old password is incorrect.")
        return value

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError("The new password and confirm new passwords do not match.")
        return data

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()

class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields = ['email']
    
    def validate(self, attrs):
        email = attrs.get('email')
        if UserProfile.objects.filter(email = email).exists():
            user = UserProfile.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = 'http://127.0.0.1:3000/reset-password/'+uid+'/'+token
            #Send Email
            body = 'Click Following Link to Reset Your Password' +link
            data = {
                'email_subject': 'Reset Your Password',
                'body':body,
                'to_email':user.email
            }
            Utils.send_email(data)
            return attrs
                
        else:
            raise ValidationError('You are not a Registered User')

class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length = 255, style = {'input_type':'password'}, write_only=True)
    confirm_password = serializers.CharField(max_length = 255, style = {'input_type':'confirm_password'}, write_only=True)
    class Meta:
        fields = ['password', 'confirm_pssword']
    
    def validate(self, attrs):
        try:
            password = attrs.get('password')
            confirm_password = attrs.get('confirm_password')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != confirm_password:
                raise (serializers.ValidationError)("Password and Confirm Password dosen't match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = UserProfile.objects.get(id = id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise ValidationError('Token is not Valid or Expired')
            user.set_password(password)
            user.save()
            return attrs  
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise ValidationError('Token is not Valid or Expired')

class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = UserProfile
        fields = ['full_name', 'email', 'phone', 'role', 'password']

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        
        # Check if the instance exists
        if not instance:
            raise NotFound("User not found")

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
