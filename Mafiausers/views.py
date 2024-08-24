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
from rest_framework import generics

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


class Boshlash(APIView):
    @swagger_auto_schema(request_body=RoomStartSerializer)
    def post(self, request):
        room_id = request.data.get('room_id')
        print(RoomModel.objects.all().filter(room_id=room_id,is_started=True).exists())
        if RoomModel.objects.all().filter(room_id=room_id,is_started=True).exists():
            return Response({'Message': "Bu o`yin oldin boshlangan"})
        users = RoomModel.objects.all().filter(room_id=room_id).first().room_users.all()
        users_list = []
        for i in users:
            users_list.append(i.id)
            
        rollar = []
        #minimal 5 ta odam bo`lishi kerak
        #5-8 ta odam bo`lsa 2 mafia, 1 doctor, 1 policiya qolgani oddiy odam
        #9-12 ta odam bo`lsa 3 mafia, 1 doctor, 1 policiya qolgani oddiy odam
        #13-16 ta odam bo`lsa 4 mafia, 1 doctor, 1 policiya,1 manyak qolgani oddiy odam
        #17-20 ta odam bo`lsa 5 mafia, 1 doctor, 1 policiya,1 manyak, 1 o`yinchi` qolgani oddiy odam
        if len(users_list) >= 5 and len(users_list) <= 8:
            rollar = ['Mafia',"Mafia","Doctor","Komissar"]
            xalq = len(users_list)-len(rollar)
            for i in range(xalq):
                rollar.append("Oddiy aholi")
        elif len(users_list) >= 9 and len(users_list) <= 12:
            rollar = ['Mafia',"Mafia","Mafia","Doctor","Komissar"]
            xalq = len(users_list)-len(rollar)
            for i in range(xalq):
                rollar.append("Oddiy aholi")
        elif len(users_list) >= 13 and len(users_list) <= 16:
            rollar = ['Mafia',"Mafia","Mafia","Mafia","Doctor","Komissar","Manyak"]
            xalq = len(users_list)-len(rollar)
            for i in range(xalq):
                rollar.append("Oddiy aholi")
        elif len(users_list) >= 17 and len(users_list) <= 25:
            rollar = ["Oyinchi",'Mafia','Mafia',"Mafia","Mafia","Mafia","Doctor","Komissar","Manyak","Manyak"]
            xalq = len(users_list)-len(rollar)
            for i in range(xalq):
                rollar.append("Oddiy aholi")
        else:
            return Response({'Message': "O`yinchilar soni 5 dan kam yoki 25 dan ortiq bo`lmasligi kerak"})
        import random
        random.shuffle(rollar)
        users_dict = {
        }
        for i in range(len(users_list)):
            users_dict[users_list[i]] = rollar[i]
        for i in users_dict:
            user = MafiaUserModel.objects.get(id=i)
            room = RoomModel.objects.all().filter(room_id=room_id).first()
            RoomRole.objects.create(room=room, user=user, role=users_dict[i])
        RoomModel.objects.filter(room_id=room_id).update(is_started=True)
        return Response(users_dict,status=200)
    
class ViewRole(APIView):
    @swagger_auto_schema(request_body=RoleViewSerializer)
    def post(self,request):
        id_user = request.data.get('user_id')
        room_id = request.data.get("room_id")
        user = MafiaUserModel.objects.get(id=id_user)
        room = RoomModel.objects.all().filter(room_id=room_id).first()
        a = RoomRole.objects.filter(room=room,user=user).first()
        
        
        return Response({"Message": f"{user.username} Sizning Rolingiz <<<{str(a)}>>>"})


class AllRoomRole(APIView):
    @swagger_auto_schema(request_body=RoomStartSerializer)
    def post(self,request):
        room_id = request.data.get("room_id")
        room = RoomModel.objects.all().filter(room_id=room_id).first()
        a = RoomRole.objects.filter(room=room)
        mafialar = {

        }
        xalq = {

        }
        for i in a:
            if i.role == "Mafia":
                mafialar[i.user.username] = i.role
            else:
                xalq[i.user.username] = i.role
        all_data = {
            "Mafiyalar": mafialar,
            "Xalq":xalq

        }
        
        

        return Response(all_data)

        

        


        
        




        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    