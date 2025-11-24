from rest_framework import serializers
from api.models import Member, Message, Token


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


class TokenSerializer(serializers.ModelSerializer):
    member_id = serializers.IntegerField(source='member.id', read_only=True)
    username = serializers.CharField(source='member.username', read_only=True)
    token = serializers.CharField(source='key', read_only=True)

    class Meta:
        model = Token
        fields = ['token', 'member_id', 'username']
        read_only_fields = ['token', 'member_id', 'username']


class MessageSerializer(serializers.ModelSerializer):
    author_id = serializers.IntegerField(source='author.id', read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'text', 'author_id', 'author_username', 'created_at']
        read_only_fields = ['id', 'author_id', 'author_username', 'created_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation
