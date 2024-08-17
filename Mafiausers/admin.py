from django.contrib import admin
from .models import *

# Register your models here.
# admin.site.register(MafiaUserModel)


class MafiarModelAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'status']


admin.site.register(MafiaUserModel, MafiarModelAdmin)
admin.site.register(RoomModel)
admin.site.register(PariticipantModel)
admin.site.register(GameInformationModel)