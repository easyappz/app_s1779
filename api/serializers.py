from rest_framework import serializers
from api.models import Member, Message


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'username', 'created_at']
        read_only_fields = ['id', 'created_at']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, max_length=128)

    class Meta:
        model = Member
        fields = ['username', 'password']

    def create(self, validated_data):
        member = Member(
            username=validated_data['username']
        )
        member.set_password(validated_data['password'])
        member.save()
        return member


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True, max_length=150)
    password = serializers.CharField(write_only=True, max_length=128)


class MessageSerializer(serializers.ModelSerializer):
    author = MemberSerializer(read_only=True)
    author_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Message
        fields = ['id', 'text', 'author', 'author_id', 'created_at']
        read_only_fields = ['id', 'created_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation
