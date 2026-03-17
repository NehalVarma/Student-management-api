from rest_framework import serializers
from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'email', 'age', 'course', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'email': {'validators': []}
        }

    def validate_age(self, value):
        if value < 16 or value > 100:
            raise serializers.ValidationError("Age must be between 16 and 100.")
        return value

    def validate_email(self, value):
        qs = Student.objects.filter(email=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("A student with this email already exists.")
        return value