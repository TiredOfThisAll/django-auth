from rest_framework.serializers import ModelSerializer
from .models import CustomUser

class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "phone_number", "username", "invite_code", "invited_by")