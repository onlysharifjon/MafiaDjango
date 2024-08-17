from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from .models import *
from .serializers import *
from drf_yasg.utils import swagger_auto_schema
import hashlib
import random
from rest_framework.views import APIView
from .serializers import RegisterSRL


class RegisterMafiaUser(APIView):
    serializer_class = RegisterSRL

    @swagger_auto_schema(request_body=RegisterSRL)
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
                    pass
                else:
                    for i in range(4):
                        otp_password += str(random.randint(0, 9))
                    return otp_password

            MafiaUserModel.objects.create(username=username, email=email, otp=otp_password)
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
    @swagger_auto_schema(request_body=VerifySerializer)
    def post(self, request):
        otp = request.data.get('otp')
        b = MafiaUserModel.objects.all().filter(otp=otp).update(status=True)
        if b is not None:
            b = MafiaUserModel.objects.all().filter(otp=otp).update(otp='')
            return Response({'message': 'Register Sucsessfuly'})
        else:
            return Response({'message': 'Password is invalid'})


class Login_API(APIView):
    serializer_class = LoginSerializer

    @swagger_auto_schema(request_body=LoginSerializer)
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
                MafiaUserModel.objects.filter(email=email).update(otp_login=parol)
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
        return Response({'email': 'Sizning emailingizga xabar jo`natildi'})


class VerifyLogin(APIView):
    serializer_class = VerifyLoginSerializer

    @swagger_auto_schema(request_body=VerifyLoginSerializer)
    def post(self, request):
        otp_login = request.data.get('otp_login')
        filtr1 = MafiaUserModel.objects.all().filter(otp_login=otp_login)
        serializer = MafiaModelSerializer(filtr1, many=True)
        if filtr1:
            return Response(serializer.data)
        else:
            return Response({'Xabar': "Parolni xato kiritdingingiz"})


class CreateRoom(APIView):
    def get(self, request):
        room_id = ''
        for i in range(6):
            room_id += str(random.randint(0, 9))
        hash_room_id = hashlib.sha256(room_id.encode()).hexdigest()
        RoomModel.objects.create(room_id=hash_room_id)
        return Response({"Room Successfully Created": hash_room_id})


class JoinRoom(APIView):
    @swagger_auto_schema(request_body=RoomJoinSerializer)
    def post(self, request):
        room_id = request.data.get('room_id')
        user_id = request.data.get('user_id')
        room = RoomModel.objects.get(room_id=room_id)
        user = MafiaUserModel.objects.get(id=user_id)
        room.room_users.add(user)

        return Response({"Status": 'User Joined to clan'})


def randomize(user_ids:list,user_count:int, rood_id):
    if user_count>=4 and user_count<=7:
        roles = ['don','doc'] + ['people']*(user_count-2)
        random.shuffle(user_ids)
        participants = []
        
        for i, user_id in enumerate(user_ids):
            participant = PariticipantModel.objects.create(
                user_id_id = user_id,
                role = roles[i]
            )
            participants.append(participant)
        
        game = GameInformationModel.objects.create(room = rood_id)
        game.participants.set(participants)
        game.save()

        serializer = GameInformationSerializer(game)
        return serializer.data
    




class StartGame(APIView):
    @swagger_auto_schema(request_body=StartGameSerializer)
    def post(self, request):
        room_id = request.data.get('room_id')
        if not room_id:
            return Response({"error": "Room ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            room = RoomModel.objects.get(room_id=room_id)
        except RoomModel.DoesNotExist:
            return Response({"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND)

        user_count = room.room_users.count()
        user_ids = list(room.room_users.values_list('id', flat=True))       
        if user_count< 4:         
            return Response({"status": "Game not started. Not enough players"}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({"status":"Game started!","game:info":randomize(user_ids,user_count,room)}, status=status.HTTP_200_OK)

     
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    