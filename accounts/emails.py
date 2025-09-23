from django.core.mail  import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import random
from accounts.models import CustomUser
from django.conf import settings

def opt_email(email):
   otp = random.randint(10000,99999)
   user_obj = CustomUser.objects.get(email=email)
   subject = "otp number"
   message = f'your otp is {otp}'
   email_from = settings.EMAIL_HOST
   send_mail(subject,message,email_from,[email])
   user_obj.otp = otp 
   user_obj.save()
   
