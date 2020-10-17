from rest_framework import serializers
from .models import Course,Courses,Messages,UserMy
from django.contrib.auth.models import User


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Course
        fields='__all__'


class CoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Courses
        fields='__all__'


class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Messages
        fields='__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

        
class UserMySerializer(serializers.ModelSerializer):
    class Meta:
        model=UserMy
        fields='__all__'
