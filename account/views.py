from rest_framework.response import Response
from rest_framework import generics,status
from rest_framework.views import APIView
from account.serializers import SendPasswordResetEmailSerializer, UserChangePasswordSerializer, UserLoginSerializer, UserPasswordResetSerializer, UserProfileSerializer, UserRegistrationSerializer,BookSerializer,OrderBookSerializer,BookDetailSerializer,ReturnBookSerializer
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import *

# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

class UserRegistrationView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    token = get_tokens_for_user(user)
    return Response({'token':token, 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    password = serializer.data.get('password')
    user = authenticate(email=email, password=password)
    if user is not None:
      token = get_tokens_for_user(user)
      return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
    else:
      return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

class UserProfileView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

class UserChangePasswordView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)

class SendPasswordResetEmailView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = SendPasswordResetEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)

class UserPasswordResetView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, uid, token, format=None):
    serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)



class BookList(generics.ListCreateAPIView):
    # permission_classes=[DjangoModelPermissions]
    renderer_classes = [UserRenderer]
    permission_classes=[IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class OrderBook(generics.GenericAPIView):
    renderer_classes = [UserRenderer]
    permission_classes=[IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = OrderBookSerializer

    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data = request.data)
        self.serializer.is_valid(raise_exception=True)
        order = self.serializer.save()
        return Response(status = status.HTTP_200_OK)

class ReturnBook(generics.GenericAPIView):
    renderer_classes = [UserRenderer]
    permission_classes=[IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = ReturnBookSerializer

    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data = request.data)
        self.serializer.is_valid(raise_exception=True)
        order = self.serializer.remove()
        return Response(status = status.HTTP_200_OK)

class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    renderer_classes = [UserRenderer]
    permission_classes=[IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer

class BookOrderList(generics.GenericAPIView):
    # renderer_classes = [UserRenderer]
    permission_classes=[IsAuthenticated]
    def get(self,request):
        return Response(BookOrder.objects.get(customer=request.user.id).books.values())


