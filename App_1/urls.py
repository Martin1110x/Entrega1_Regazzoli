from re import template
from django.urls import path, include
from App_1.views import *
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path("", inicio, name = "inicio"),
    path("cuentas/", cuentas, name = "cuentas"),
    path("centro_de_ayuda/", centro_de_ayuda, name = "centro_de_ayuda"),
    path("preguntas_frecuentes/", preguntas_frecuentes, name = "preguntas_frecuentes"),
    path("beneficios/", beneficios, name = "beneficios"),
    path("prestamos/", prestamos, name = "prestamos"),
    path("seguros/", seguros, name = "seguros"),
    path("tarjetas/", tarjetas, name = "tarjetas"),
    path("sobre_nosotros/", sobre_nosotros, name = "sobre_nosotros"),
    path("post/", post, name = "post"),
    path("post1/", post1, name = "post1"),
    path("post2/", post2, name = "post2"),
    path("post3/", post3, name = "post3"),
    path("paginaenconstruccion/", paginaenconstruccion, name = "paginaenconstruccion"),
    
    path("ingresar_cuenta/", ingresar_cuenta, name = "ingresar_cuenta"),
    path("perfil/", perfil, name = "perfil"),
    path("crear_empleado/", crear_empleado, name = "crear_empleado"), 
    path("crear_transferencia_bancaria/", crear_transferencia_bancaria, name = "crear_transferencia_bancaria"), 
    path("dinero_en_cuenta/", dinero_en_cuenta, name = "dinero_en_cuenta"), 
    path("agregar_dinero/", agregar_dinero, name = "agregar_dinero"), 
    
    #ABM funciones
    path("eliminar_usuario_confirmar/", eliminar_usuario_confirmar, name = "eliminar_usuario_confirmar"),
    path("eliminar_usuario",eliminar_usuario,name ="eliminar_usuario"),
    #login, register, logout, avatar
    path("login/", login_solicitud, name = "login"),
    path("register/", register, name = "register"),
    path("logout/", LogoutView.as_view(template_name = "logout.html"), name = "logout"),
    path("editar_perfil/", editar_perfil, name = "editar_perfil"),
    path("agregar_avatar/", agregar_avatar, name = "agregar_avatar"),
    #path('chat/', include ('chats.urls'), name='chat'),

    #CKEDITOR
    path('Create_Blog/', CreateBlog.as_view(), name="CreateBlog"),

    path('update_blog/<int:pk>/', UpdateBlogView.as_view(), name="UpdateBlogView"),

    path('delete_blog/<int:pk>/', DeleteBlogView.as_view(), name="DeleteBlogView"),

    path('blog_detail/<str:slug>', blog_detail, name="blog_detail"),

    path('blog_home/', blog_home.as_view(), name="blog_list"),
    

    
]



