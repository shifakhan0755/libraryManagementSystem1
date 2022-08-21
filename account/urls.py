from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from account.views import SendPasswordResetEmailView, UserChangePasswordView, UserLoginView, UserProfileView, UserRegistrationView, UserPasswordResetView
from account import views




urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    path('book/profile/', views.BookList.as_view()),
    # path('orders/', views.BookOrderList.as_view()),
    path('order/', views.OrderBook.as_view()),
    path('store/<int:pk>/', views.BookDetail.as_view()),
    path('return/', views.ReturnBook.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)