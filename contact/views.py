from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ContactSubmission
from .serializers import ContactSubmissionSerializer
import traceback

@api_view(['GET', 'POST'])
def contact_submission(request):
    try:
        if request.method == 'GET':
            return Response({
                'message': '✅ Contact API is working!',
                'instruction': 'Send POST request with: name, email, message',
                'required_fields': ['name', 'email', 'message'],
                'example': {
                    'name': 'John Doe',
                    'email': 'john@example.com',
                    'message': 'Hello, I would like to connect with you!'
                }
            }, status=status.HTTP_200_OK)

        if request.method == 'POST':
            if not request.data:
                return Response(
                    {'error': 'Empty request body. Please send JSON with name, email, message.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = ContactSubmissionSerializer(data=request.data)

            if not serializer.is_valid():
                return Response(
                    {'error': 'Invalid form data.', 'details': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )

            contact = serializer.save()

            try:
                # Send email to portfolio owner
                send_mail(
                    subject=f'📧 New Contact from {contact.name}',
                    message=f"""
Name: {contact.name}
Email: {contact.email}
Message:
{contact.message}

Submitted at: {contact.submitted_at}
""".strip(),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.DEFAULT_FROM_EMAIL],
                    fail_silently=False,
                )

                # Auto-reply to user
                send_mail(
                    subject='Thank you for reaching out! - Abhiram',
                    message=f"""
Hi {contact.name},

Thank you for reaching out through my portfolio website! 
I've received your message and will get back to you within 24 hours.

Best regards,
Abhiram
Email: chabhiram2001@gmail.com
Phone: +91 7095885614
""".strip(),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[contact.email],
                    fail_silently=False,
                )

                contact.is_processed = True
                contact.save()

                return Response(
                    {'message': 'Message sent successfully! Thank you for reaching out.', 'status': 'success'},
                    status=status.HTTP_201_CREATED
                )

            except Exception:
                contact.is_processed = False
                contact.save()
                print("Email sending failed:", traceback.format_exc())
                return Response(
                    {'error': 'Message received but email delivery failed.', 'status': 'warning'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

    except Exception:
        print("Unhandled exception:", traceback.format_exc())
        return Response(
            {'error': 'Internal server error occurred.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
