from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib
import random
from .models import MafiaUserModel
from .models import MafiaUserModel
from .serializers import LoginSerializer

# login qilish uchun api yozishimiz kerak
from rest_framework.views import APIView


class Login_API(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data.get('email')

        try:
            filter = MafiaUserModel.objects.filter(email=email)
            if filter.exists():
                sender_email = "mominovsharif12@gmail.com"
                receiver_email = email
                password = "uorv tkma xoxp jpcr"
                smtp_server = "smtp.gmail.com"
                smtp_port = 587
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
                server.login(sender_email, password)
                parol = random.randint(100000, 999999)

                subject = "Mafia UZ"
                body = f"Sizning tasdiqlash kodingiz{parol}"
                message = MIMEMultipart()

                message["From"] = sender_email
                message["To"] = receiver_email
                message["Subject"] = subject
                message.attach(MIMEText(body, "plain"))

                server.sendmail(sender_email, receiver_email, message.as_string())
                print('Email sent successfully!')
            else:
                return Response({'error': 'Bunday email mavjud emas'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f'Error: {e}')
        # finally:
        #     server.quit()
        return Response({'email': 'Sizning emailingizga xabar jo`natildi'})


# from rest_framework.generics import ListCreateAPIView, GenericAPIView
# from .models import MafiaUserModel
# from .serializers import MafiaModelSerializer, OTPVerifySerializer
# from rest_framework.response import Response
# from rest_framework import status
# import random
# from django.core.mail import send_mail
from .serializers import RegisterSRL


class RegisterMafiaUser(APIView):
    serializer_class = RegisterSRL

    def post(self, request):
        email = request.data.get('email')
        username = request.data.get('username')
        username_filter = MafiaUserModel.objects.all().filter(username=username).first()
        email_filter = MafiaUserModel.objects.all().filter(email=email).first()
        print(username_filter)
        print(email_filter)
        if username_filter is None and email_filter is None:
            import random
            otp_password = ''
            for i in range(4):
                otp_password += str(random.randint(0, 9))
            def checker(otp_password):
                a = MafiaUserModel.objects.all().filter(otp=otp_password).first()
                if a is None:
                    otp
                else:
                    for i in range(4):
                        otp_password += str(random.randint(0, 9))
                    return otp_password

            MafiaUserModel.objects.create(username=username,email=email,otp=otp_password)
            sender_email = "mominovsharif12@gmail.com"
            receiver_email = email
            password = "uorv tkma xoxp jpcr"
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, password)
            parol = random.randint(100000, 999999)

            subject = "Mafia UZ"
            body = f"Sizning tasdiqlash kodingiz: {otp_password}"
            message = MIMEMultipart()

            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))

            server.sendmail(sender_email, receiver_email, message.as_string())
            print('Email sent successfully!')
            return Response({'mmessage': 'Email sent successfully!'})
        else:
            return Response({'error': "Bunday email allaqachon ro`yxatdan o`tgan"})

class VerifyAccount(APIView):
    def post(self,request):
        otp = request.data.get('otp')
        b = MafiaUserModel.objects.all().filter(otp=otp).update(status=True)
        if b is not None:
            b = MafiaUserModel.objects.all().filter(otp=otp).update(otp='')
            return Response({'message':'Register Sucsessfuly'})
        else:
            return Response({'message':'Password is invalid'})

