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
        username_filter = MafiaUserModel.objects.all().filter(username=username)
        email_filter = MafiaUserModel.objects.all().filter(email=email)
        if username_filter is None and email_filter is None:
            import random
            otp_password = ''
            for i in range(4):
                otp_password += random.randint(0, 9)
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

# class MafiaUserCreateView(ListCreateAPIView):
#     queryset = MafiaUserModel.objects.all()
#     serializer_class = MafiaModelSerializer
#
#     def create(self, request, *args, **kwargs):
#         email = request.data.get("email")
#
#         if MafiaUserModel.objects.filter(email=email).exists():
#             Response({"Email is already registrated"}, status=status.HTTP_400_BAD_REQUEST)
#
#         otp = random.randint(1000, 9999)
#
#         send_mail(
#             "Verification Code",
#             f"Your verification code is: {otp} ",
#             'TalabaUz <setting.EMAIL_HOST_USER>',
#             [email],
#             fail_silently=False,
#         )
#         mutable_data = request.data.copy()
#
#         mutable_data['otp'] = otp
#
#         serializer = self.get_serializer(data=mutable_data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#
#         return Response("Otp sended successfully", status=status.HTTP_200_OK)
#
#
# class OTPVerificationView(GenericAPIView):
#     serializer_class = OTPVerifySerializer
#
#     def post(self, request, *args, **kwargs):
#         email = request.data.get('email')
#         otp = request.data.get('otp')
#
#         try:
#             user = MafiaUserModel.objects.get(email=email)
#         except MafiaUserModel.DoesNotExist:
#             return Response("User not found.", status=status.HTTP_404_NOT_FOUND)
#
#         if not user.otp == otp:
#             return Response({'error': 'Provided code is wrong'}, status=status.HTTP_400_BAD_REQUEST)
#
#         user.status = True
#         user.otp = ""
#         user.save()
#         return Response("Your email verified successfully!", status=status.HTTP_200_OK)
