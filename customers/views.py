import jwt
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import CustomerSerializer
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Customer
from .tasks import send_confirmation_email_task


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request) -> Response:
    """
    Register a new user
    """
    user = User.objects.create(username=request.data.get('username'), email=request.data.get('email'),
                               password=request.data.get('password'))
    customer = Customer.objects.create(user=user)

    send_confirmation_email_task.delay(customer.user.id)
    # send_confirmation_email_task(customer.user.id)

    return Response({'message': 'User registered successfully. Check your email for confirmation.'})


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def confirm_registration(request) -> Response:
    """
    Confirm user registration using a token.
    """
    token = request.data.get('token', None)

    if not token:
        return Response({'detail': 'Token not provided.'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = payload['user_id']

        user = get_object_or_404(User, id=user_id)
        customer = user.customer

        customer.email_confirmed = True
        customer.save()
        refresh_token = RefreshToken.for_user(user)
        return Response(
            {
                "refresh_token": str(refresh_token),
                "access_token": str(refresh_token.access_token),
                "user_id": user_id,
            }
        )


    except jwt.ExpiredSignatureError:
        return Response({'detail': 'Token has expired.'}, status=status.HTTP_400_BAD_REQUEST)

    except jwt.InvalidTokenError as e:
        return Response({'detail': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def reset_password(request) -> Response:
    """
    Reset user password.
    """
    new_password = request.data.get('new_password')

    user = request.user.customer

    user.user.set_password(new_password)
    user.user.save()
    # send_password_reset_email_task(user.user.id, new_password)
    send_mail(
        'Password Reset Confirmation',
        f'Your password has been successfully reset.New password{new_password} for user {user}',
        None,
        [user.user.email],
        fail_silently=False,
    )
    return Response({'message': 'Password reset successful.'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def reset_email(request) -> Response:
    """
    Reset user email address.
    """
    new_email = request.data.get('new_email')

    user = request.user.customer

    send_mail(
        'Email Reset Confirmation',
        f'Your email has been successfully reset. New email: {new_email} for user: {user}',
        None,
        [user.user.email],
        fail_silently=False,
    )
    user.user.email = new_email
    user.user.save()

    return Response({'message': 'Email reset successful.'})


class CustomerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = (JWTAuthentication,)
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
