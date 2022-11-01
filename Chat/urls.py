from uuid import UUID
from django.urls import path, re_path
from .views import *

UUID_CANAL_REGEX = r'canal/(?P<pk>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})'
urlpatterns = [

     path("inbox/", Inbox.as_view(), name = "inbox"),
     path("usuarios_chatear/", usuarios_chatear, name = "usuarios_chatear"),
     #path("<str:username>/", mensajes_privados, name = "mensajes_privados"),
     path("<str:username>/", Detail_mensajes.as_view(), name = "Detail_mensajes"), 
      

     #re_path(r'canal/(?P<pk>[\w-]+)', Canal_detail_view.as_view(), name = "Canal_detail_view"), 
     re_path(UUID_CANAL_REGEX, Canal_detail_view.as_view(), name = "Canal_detail_view"),
     
     
]
