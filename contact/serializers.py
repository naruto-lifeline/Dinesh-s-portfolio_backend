from rest_framework import serializers
from .models import ContactSubmission

class ContactSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactSubmission
        fields = ['id', 'name', 'email', 'message', 'submitted_at', 'is_processed']
        read_only_fields = ['id', 'submitted_at', 'is_processed']