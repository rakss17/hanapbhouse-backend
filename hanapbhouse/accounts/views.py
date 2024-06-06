from django.shortcuts import redirect
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from .models import User
from rest_framework.response import Response

def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()


        subject = 'Your account has been activated'
        message = f'Your account has been activated.'

        from_email = settings.EMAIL_HOST_USER
        to_email = user.email

        send_mail(subject, message, from_email, [to_email])
        messages.success(request, 'Your account has been activated.')
        
        return redirect(f'https://gmail.com')
    else:
        messages.error(request, 'Activation link is invalid or has expired.')
        return Response({'message': "Expired"}, status=404)
        # return redirect(f'{settings.FRONTEND_URL}/#/NotFound')
