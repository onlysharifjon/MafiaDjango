from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response

from .serializers import LoginSerializer

# login qilish uchun api yozishimiz kerak
from rest_framework.views import APIView


class Login_API(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data.get('email')
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.application import MIMEApplication
        import smtplib
        import random
        from .models import MafiauserModel

        try:
            filter = MafiauserModel.objects.filter(email=email)
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


from django.shortcuts import render

# Create your views here.
