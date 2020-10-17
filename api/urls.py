from django.contrib import admin
from django.urls import path,include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import ObtainAuthToken
from api.views import (
                        CoursesView,
                        UserMyView,
                        UserView,
                        CourseUserView,
                        LoginView,
                        LogoutView,
                        MessageView,
                    )
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('rest-auth/login/',ObtainAuthToken.as_view()),
    path('auth/login/',csrf_exempt(LoginView.as_view())),
    path('auth/logout/<str:token>/',csrf_exempt(LogoutView.as_view())),
    path('courses/<str:token>/',csrf_exempt(CoursesView.as_view())),
    path('usermy/<str:token>/',csrf_exempt(UserMyView.as_view())),
    path('user/<str:token>/',csrf_exempt(UserView.as_view())),
    path('user/<int:pk>/<str:username>/<str:token>/',csrf_exempt(CourseUserView.as_view())),
    path('messages/<int:pk>/<str:token>/',csrf_exempt(MessageView.as_view())),
]
urlpatterns = format_suffix_patterns(urlpatterns)
