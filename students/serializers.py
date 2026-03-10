from rest_framework import serializers
from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'email', 'age', 'course', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_age(self, value):
        if value < 16 or value > 100:
            raise serializers.ValidationError("Age must be between 16 and 100.")
        return value

    def validate_email(self, value):
        if Student.objects.filter(email=value).exists():
            if self.instance and self.instance.email != value:
                raise serializers.ValidationError("A student with this email already exists.")
            elif not self.instance:
                raise serializers.ValidationError("A student with this email already exists.")
        return value