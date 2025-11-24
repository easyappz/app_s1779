from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from .models import Member, Token, Message
from .serializers import (
    MessageSerializer,
    RegisterSerializer,
    LoginSerializer,
    TokenSerializer,
    MemberSerializer
)


class TokenAuthentication(BaseAuthentication):
    """
    Custom token authentication using Token model.
    """
    keyword = 'Token'

    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header:
            return None
        
        parts = auth_header.split()
        
        if len(parts) != 2 or parts[0] != self.keyword:
            return None
        
        token_key = parts[1]
        
        try:
            token = Token.objects.select_related('member').get(key=token_key)
        except Token.DoesNotExist:
            raise AuthenticationFailed('Invalid token')
        
        return (token.member, token)


class RegisterView(APIView):
    """
    Register a new member and return authentication token.
    """
    
    @extend_schema(
        request=RegisterSerializer,
        responses={201: TokenSerializer},
        description="Register a new member"
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            member = serializer.save()
            token = Token.objects.create(member=member)
            token_serializer = TokenSerializer(token)
            return Response(token_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    Login with username and password, return authentication token.
    """
    
    @extend_schema(
        request=LoginSerializer,
        responses={200: TokenSerializer},
        description="Login and get authentication token"
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            try:
                member = Member.objects.get(username=username)
            except Member.DoesNotExist:
                return Response(
                    {"detail": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            if not member.check_password(password):
                return Response(
                    {"detail": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            token, created = Token.objects.get_or_create(member=member)
            if not created:
                # Delete old token and create new one
                token.delete()
                token = Token.objects.create(member=member)
            
            token_serializer = TokenSerializer(token)
            return Response(token_serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    Logout by deleting the authentication token.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        responses={204: None},
        description="Logout and delete authentication token"
    )
    def post(self, request):
        if hasattr(request, 'auth') and request.auth:
            request.auth.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MessageListCreateView(generics.ListCreateAPIView):
    """
    List all messages (public) or create a new message (authenticated).
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    
    def get_authenticators(self):
        if self.request.method == 'POST':
            return [TokenAuthentication()]
        return []
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return []
    
    @extend_schema(
        responses={200: MessageSerializer(many=True)},
        description="Get all messages"
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @extend_schema(
        request=MessageSerializer,
        responses={201: MessageSerializer},
        description="Create a new message"
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrentMemberView(APIView):
    """
    Get current authenticated member information.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        responses={200: MemberSerializer},
        description="Get current member info"
    )
    def get(self, request):
        serializer = MemberSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class HelloView(APIView):
    """
    A simple API endpoint that returns a greeting message.
    """

    @extend_schema(
        responses={200: MessageSerializer}, description="Get a hello world message"
    )
    def get(self, request):
        data = {"message": "Hello!", "timestamp": timezone.now()}
        serializer = MessageSerializer(data)
        return Response(serializer.data)
