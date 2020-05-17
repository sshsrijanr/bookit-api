from rest_framework import serializers
from bookit.common.serializers import AttachmentSerializer
from .models import Profile, User


class ProfileSerializer(serializers.ModelSerializer):
    id_card_details = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = "__all__"

    def get_id_card_details(self, instance):
        return AttachmentSerializer(instance.id_card, context=self.context).data


class UserSerializer(serializers.ModelSerializer):
    profile_details = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ['password', 'last_login', 'is_superuser',
                   'is_staff', 'groups', 'user_permissions']

    def get_profile_details(self, instance):
        return ProfileSerializer(instance.profile, context=self.context).data
