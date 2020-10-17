from django.shortcuts import render
from users.models import Course,Courses,Messages,UserMy,Token
from django.contrib.auth.models import User
from users.serializers import CourseSerializer,CoursesSerializer,MessagesSerializer,UserMySerializer,UserSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import warnings

from django.conf import settings
# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.utils.decorators import method_decorator
from braces.views import CsrfExemptMixin
from django.utils.crypto import get_random_string
from django.db.models import Q


class CoursesView(CsrfExemptMixin,APIView):

    @method_decorator(csrf_exempt)
    def get(self,request,token,format=None):
        usr=get_user_token(token)
        user=UserMy.objects.get(user=usr)
        courses=user.courses.all()
        course_set=Course.objects.filter(pk__in=courses.values('course'))
        serializer=CourseSerializer(course_set,many=True)
        return Response(serializer.data)
    
    @method_decorator(csrf_exempt)
    def post(self,request,token,format=None):
        usr=get_user_token(token)
        user=UserMy.objects.get(user=usr)
        serializer=CourseSerializer(data=request.data)
        if serializer.is_valid() and user.is_professor:
            course=serializer.save()
            courses=Courses.objects.create(course=course,status="professor")
            user.courses.add(courses)
            serializer_1=CoursesSerializer(courses)
            return Response(serializer_1.data,status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)


class UserMyView(CsrfExemptMixin,APIView):

    @method_decorator(csrf_exempt)
    def get(self,request,token,format=None):
        usr=get_user_token(token)
        try:
            user=UserMy.objects.get(user=usr)
            serializer=UserMySerializer(user)
            return Response(serializer.data)
        except:
            return Response()
    
    @method_decorator(csrf_exempt)
    def post(self,request,token,format=None):
        usr=get_user_token(token)
        try:
            user=UserMy.objects.create(user=usr)
            serializer=UserMySerializer(user)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,status.HTTP_206_PARTIAL_CONTENT)
        except:
            return Response(status.HTTP_400_BAD_REQUEST)

      
class UserView(CsrfExemptMixin,APIView):

    @method_decorator(csrf_exempt)
    def get(self,request,token,format=None):
        user=get_user_token(token)
        serializer=UserSerializer(user)
        return Response(serializer.data)
    
    @method_decorator(csrf_exempt)
    def post(self,request,token='',format=None):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            request.data['user']=user.pk
            serializer1=UserMySerializer(data=request.data)
            if serializer1.is_valid():
                serializer1.save()
                response=Response(serializer1.data,status.HTTP_201_CREATED)
                response['Access-Control-Allow-Origin']='*'
                return response
            else:
                return Response(serializer1.errors,status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)


class CourseUserView(CsrfExemptMixin,APIView):
    
    @method_decorator(csrf_exempt)
    def get(self,request,pk,username,token,format=None):
        usr=get_user_token(token)
        user=UserMy.objects.get(user=usr)
        try:
            course_i=Course.objects.get(pk=pk)
            course=user.courses.get(course=course_i)
            serializer=CoursesSerializer(course)
            return Response(serializer.data)
        except:
            return Response()
    
    @method_decorator(csrf_exempt)
    def post(self,request,pk,username,token,format=None):
        usr=User.objects.get(username=username)
        user=UserMy.objects.get(user=usr)
        course_i=Course.objects.get(pk=pk)
        courses,created=Courses.objects.get_or_create(course=course_i,status=request.data['status'])
        print(courses)
        try:
            courses_old = user.courses.get(course=course_i)
            serializer = CoursesSerializer(courses_old)
        except:
            user.courses.get(course=course_i)
            serializer = CoursesSerializer(courses)
            user.courses.add(courses.pk)
        return Response(serializer.data,status.HTTP_201_CREATED)


class LoginView(CsrfExemptMixin,APIView):

    @method_decorator(csrf_exempt)
    def post(self,request,format=None):
        self.user_cache = authenticate(self.request, username=request.data['username'], password=request.data['password'])
        if self.user_cache is not None:
            auth_login(request,self.get_user())
            user=self.get_user()
            user_my=UserMy.objects.get(user=user)
            uuid=request.data['uuid']
            token=Token.objects.create(uuid=uuid)
            user_my.tokens.add(token)
            token_form=uuid+'|'+token.token
            serializer = UserMySerializer(user_my)
            new_dict={'token_form':token_form}
            new_dict.update(serializer.data)
            response=Response(new_dict)
            return response
        else:
            return Response(request.data)

    def get_user(self):
        return self.user_cache


class LogoutView(CsrfExemptMixin,APIView):

    @method_decorator(csrf_exempt)
    def get(self,request,token,format=None):
        user=get_user_token(token)
        user_my=UserMy.objects.get(user=user)
        token_uuid,token_val=token.split('|')
        token_obj=Token.objects.filter(uuid=token_uuid).filter(token=token_val).first()
        user_my.tokens.remove(token_obj)
        token_obj.delete()
        auth_logout(request)
        return Response()


class MessageView(CsrfExemptMixin,APIView):

    @method_decorator(csrf_exempt)
    def get(self,request,pk,token,format=None):
        user=get_user_token(token)
        user_my=UserMy.objects.get(user=user)
        course=Course.objects.get(pk=pk)
        course_stat=user_my.courses.get(course=course)
        if course_stat.status == 'professor':
            messages=Messages.objects.filter(course=course)
        elif course_stat.status == 'TA':
            messages=Messages.objects.filter(course=course).filter(Q(to='student')|Q(to='TA'))
        else:
            messages=Messages.objects.filter(course=course).filter(to='student')
        messages=messages.order_by('-sent')
        serializer=MessagesSerializer(messages,many=True)
        return Response(serializer.data)

    @method_decorator(csrf_exempt)
    def post(self,request,pk,token,format=None):
        user = get_user_token(token)
        user_my = UserMy.objects.get(user=user)
        course = Course.objects.get(pk=pk)
        message=Messages.objects.create(course=course,by=user,to=request.data['to'],message=request.data['message'])
        message.read_by.add(user)
        serializer=MessagesSerializer(message)
        return Response(serializer.data)

def get_user_token(token_in):
    uuid,token=token_in.split('|')
    token_obj=Token.objects.filter(uuid=uuid).filter(token=token).first()
    user_my=token_obj.usermy_set.first()
    user_pk=user_my.user
    return user_pk