from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from .models import User
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer=UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


# Create your views here.
class LoginView(APIView):
    def post(self, request):
        email=request.data['email']
        password=request.data['password']
        user=User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        payload={
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()

        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')

        # Δημιουργία απάντησης με το Response από το Django REST Framework

        response = Response({
            'message': 'Login successful'
        })

        # Ορισμός του JWT token στο cookie
        response.set_cookie(
            key='jwt',  # Το όνομα του cookie
            value=token,  # Το περιεχόμενο του JWT token
            httponly=True,  # Για να είναι ασφαλές (δεν μπορεί να προσπελαστεί από JavaScript)
            max_age=datetime.timedelta(minutes=60),  # Η διάρκεια του cookie

        )

        return response

class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Token not found')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Invalid token')


        user=User.objects.filter(id=payload['id']).first()

        serializer = UserSerializer(user)

        return Response(serializer.data)




class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data={
            'message': 'Logout successful'
        }
        return response