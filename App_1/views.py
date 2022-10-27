from multiprocessing.connection import Client
from telnetlib import STATUS
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import generic
from django.urls import  reverse_lazy
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from random import choice, randint
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib import messages

from django.contrib.auth.decorators import user_passes_test # @user_passes_test(lambda u: u.is_superuser)
from django.contrib.admin.views.decorators import staff_member_required # @staff_member_required



# Create your views here.
def inicio(request):
    return render(request, "inicio.html")

def cuentas(request):
    return render(request, "cuentas.html")

def centro_de_ayuda(request):
    return render(request, "centro_de_ayuda.html")

def preguntas_frecuentes(request):
    return render(request, "preguntas_frecuentes.html")

def beneficios(request):
    return render(request, "beneficios.html")

def prestamos(request):
    return render(request, "prestamos.html")

def seguros(request):
    return render(request, "seguros.html")

def tarjetas(request):
    return render(request, "tarjetas.html")
    
def sobre_nosotros(request):
    return render(request, "sobre_nosotros.html")

def ingresar_cuenta(request):
    return render(request, "ingresar_cuenta.html")

def post(request):
    return render (request, "post.html")

def post1(request):
    return render (request, "post1.html")

def post2(request):
    return render (request, "post2.html")


@csrf_exempt
def post3(request):
    post = Blog.objects.filter()
    print (post)
    return render (request, "post3.html", {"post":post})

def paginaenconstruccion(request):
    return render(request, "paginaenconstruccion.html")

def crear_empleado(request):
    if request.method == "POST":
        form: object = User_register_form(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            user = form.save()
            _usuario: str = datos["username"]
            _dni: int = datos["DNI"]
            _fecha_de_nacimiento: int = datos["fecha_de_nacimiento"]
            _domicilio: int = datos["domicilio"]
            _localidad: int = datos["localidad"]
            _provincia: int = datos["provincia"] 
            empleado = Empleado(usuario = user, DNI = _dni, fecha_de_nacimiento = _fecha_de_nacimiento, domicilio = _domicilio, localidad = _localidad, provincia = _provincia)
            empleado.save()
            return render(request, "inicio.html", {"mensaje": f"Se registro el usuario {_usuario} exitosamente."})
        else:
            return render(request, "crear_empleado.html", {"mensaje": "Error, datos introducidos erróneos."})
    else:
        form = User_register_form()
        return render(request, "crear_empleado.html", {"formulario": form})

@login_required
def crear_transferencia_bancaria(request):
    remitente = request.user
    datos_bancarios = Cliente.objects.get(usuario = remitente)
    if request.method == "POST":
        formulario: object = Crear_transferencia_bancaria(request.POST)
        if formulario.is_valid():
            informacion: dict = formulario.cleaned_data
            monto_transferencia: int = informacion["monto_en_pesos"]
            if datos_bancarios.dinero_en_la_cuenta - monto_transferencia < 0:
                return render(request, "dinero_en_cuenta.html", {"mensaje": "Usted no posee el dinero en la cuenta necesario para poder hacer la transferencia.", "datos_bancarios": datos_bancarios})
            datos_bancarios.dinero_en_la_cuenta -= monto_transferencia
            Transferencia__bancaria: object = Transferencia_bancaria(monto_en_pesos = monto_transferencia, fecha_de_transferencia = datetime.now().date(), nombre_del_remitente = remitente.username, apellido_del_remitente = remitente.last_name, dni_del_remitente = datos_bancarios.DNI, nombre_del_destinatario = informacion["nombre_del_destinatario"], apellido_del_destinatario = informacion["apellido_del_destinatario"], dni_del_destinatario = informacion["dni_del_destinatario"])
            Transferencia__bancaria.save()
            return render(request, "dinero_en_cuenta.html", {"mensaje": "La transferencia bancaria fue realizada exitosamente!", "datos_bancarios": datos_bancarios})
    else:
        formulario: object = Crear_transferencia_bancaria()
        return render(request, "crear_transferencia_bancaria.html", {"formulario": formulario})

@login_required
def dinero_en_cuenta(request):
    _usuario = request.user
    datos_bancarios = Cliente.objects.get(usuario = _usuario)
    return render(request, "dinero_en_cuenta.html",{"datos_bancarios": datos_bancarios})

@login_required
def agregar_dinero(request):
    _usuario = request.user
    datos_bancarios = Cliente.objects.get(usuario = _usuario)
    if request.method == "POST":
        formulario: object = Agregar_dinero(request.POST)
        if formulario.is_valid():
            informacion: dict = formulario.cleaned_data
            datos_bancarios.dinero_en_la_cuenta += informacion["dinero_agregado"]
            datos_bancarios.save()
            return render(request, "dinero_en_cuenta.html",{"datos_bancarios": datos_bancarios})
        else:
            return render(request, "agregar_dinero.html", {"mensaje": "Introduzca el monto de forma numérica."})
    else:
        formulario = Agregar_dinero()
        return render(request, "agregar_dinero.html", {"formulario": formulario, "datos_bancarios": datos_bancarios})
        
@login_required
def perfil(request):
    _usuario = request.user
    cliente = Cliente.objects.get(usuario = _usuario)
    return render(request, "perfil.html", {"avatar":obtener_avatar(request), "datos": _usuario, "datos_bancarios": cliente}) 
    
@login_required
def eliminar_usuario_confirmar(request):
    return render(request, "eliminar_usuario_confirmar.html")

@login_required
def eliminar_usuario(request):
    _usuario = request.user
    _usuario.delete()
    return render(request, "cuenta_eliminada.html", {"mensaje": "Se eliminó tu cuenta de banco."})

def login_solicitud(request): 
    if request.method == "POST":
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            usuario: str = form.cleaned_data.get("username")
            contrasenia: str = form.cleaned_data.get("password")
            user: object = authenticate(username = usuario, password = contrasenia)
            if user is not None:
                login(request, user)     
                return render(request, "inicio.html", {"mensaje": f"Bienvenido {usuario}"})
            else:
                return render(request, "inicio.html", {"mensaje": "Error, datos incorrectos"})
        else:
            return render(request, "inicio.html", {"mensaje": "Error, datos introducidos erróneos."})
    else:
        form = AuthenticationForm()
        return render(request, "login.html", {"formulario": form})

def register(request):
    if request.method == "POST":
        form: object = User_register_form(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            print(datos)
            print("hola")
            user = form.save()
            print("hola2")
            print(user)
            _usuario: str = form.cleaned_data["username"]
            _dni: int = form.cleaned_data["DNI"]
            _fecha_de_nacimiento: int = form.cleaned_data["fecha_de_nacimiento"]
            _domicilio: int = form.cleaned_data["domicilio"]
            _localidad: int = form.cleaned_data["localidad"]
            _provincia: int = form.cleaned_data["provincia"] 
            login(request, user)
            #Creación datos bancarios
            usu_nivel_del_cliente: str = "Básico" # basico, gold, platinum, black.
            usu_dinero_en_la_cuenta: int = 0
            usu_tarjeta_de_credito_vencida: bool = False
            fecha_de_hoy: str = datetime.now()
            usu_fecha_de_vencimiento_tarjeta: str = fecha_de_hoy + timedelta(days = 1500)
            usu_fecha_de_vencimiento_tarjeta =  usu_fecha_de_vencimiento_tarjeta.date()
            list_usu_numero_de_tarjeta: list = [0] * 16
            list_usu_numero_de_tarjeta[0] = str(4)
            for i in range(1, len(list_usu_numero_de_tarjeta)):
                list_usu_numero_de_tarjeta[i] = str(randint(1,9))
            usu_numero_de_tarjeta: str = "".join(list_usu_numero_de_tarjeta)
            usu_codigo_de_seguridad_tarjeta: int = randint(100,999)
            cliente = Cliente(usuario = user, DNI = _dni, fecha_de_nacimiento = _fecha_de_nacimiento, domicilio = _domicilio, localidad = _localidad, provincia = _provincia, nivel_del_cliente = usu_nivel_del_cliente, dinero_en_la_cuenta = usu_dinero_en_la_cuenta, tarjeta_de_credito_vencida = usu_tarjeta_de_credito_vencida,
            fecha_de_vencimiento_tarjeta = usu_fecha_de_vencimiento_tarjeta, numero_de_tarjeta = usu_numero_de_tarjeta, codigo_de_seguridad_tarjeta = usu_codigo_de_seguridad_tarjeta )
            cliente.save()
            return render(request, "perfil.html", {"mensaje": f"el usuario {_usuario} fue creado exitosamente.", "datos": datos, "user": user,  "datos_bancarios": cliente})
        else:
            return render(request, "inicio.html", {"mensaje": "Error, datos introducidos erróneos."})
    else:
        form = User_register_form()
        return render(request, "register.html", {"formulario": form})

@login_required
def editar_perfil(request):
    _usuario = request.user
    if request.method == "POST":
        form = User_edit_form(request.POST)
        if form.is_valid():
            informacion: dict = form.cleaned_data
            _usuario.username = informacion["username"]
            _usuario.last_name = informacion["last_name"]
            _usuario.email = informacion["email"]
            _usuario.password1 = informacion["password1"]
            _usuario.password2 = informacion["password2"]
            _usuario.save()
            datos_bancarios = Cliente.objects.get(usuario = _usuario)
            datos_bancarios.DNI: int = informacion["DNI"]
            datos_bancarios.fecha_de_nacimiento: int = informacion["fecha_de_nacimiento"]
            datos_bancarios.domicilio: int = informacion["domicilio"]
            datos_bancarios.localidad: int = informacion["localidad"]
            datos_bancarios.provincia: int = informacion["provincia"]
            datos_bancarios.save()
            return render(request, "perfil.html",  {"mensaje": "El perfil fue editado exitosamente.", "avatar":obtener_avatar(request), "datos": _usuario, "datos_bancarios": datos_bancarios})
        else:
            render(request, "editar_perfil.html", {"formulario": form, "usuario": _usuario, "mensaje": "formulario invalido."})
    else:
        form = User_edit_form(instance = _usuario)
        return render(request, "editar_perfil.html", {"formulario": form, "usuario": _usuario, "avatar":obtener_avatar(request)})    

@login_required
def agregar_avatar(request):
    if request.method=='POST':
        formulario=AvatarForm(request.POST, request.FILES)
        if formulario.is_valid():
            avatarViejo=Avatar.objects.filter(user=request.user)
            if(len(avatarViejo)>0):
                avatarViejo[0].delete()
            avatar=Avatar(user=request.user, imagen=formulario.cleaned_data['imagen'])
            avatar.save()
            return render(request, 'inicio.html', {'usuario':request.user, 'mensaje':'AVATAR AGREGADO EXITOSAMENTE', "avatar": avatar.imagen.url})
        else:
            return render(request, 'agregar_avatar.html', {'formulario':formulario, 'mensaje':'FORMULARIO INVALIDO'})
        
    else:
        formulario=AvatarForm()
        return render(request, "agregar_avatar.html", {"formulario":formulario, "usuario":request.user, "avatar": obtener_avatar(request)})


def obtener_avatar(request):
    lista=Avatar.objects.filter(user=request.user)
    if len(lista)!=0:
        imagen=lista[0].imagen.url
    else:
        imagen="/media/avatares/avatarpordefecto.png"
    return imagen


#CKEDITOR

class CreateBlog(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    form_class = CreateBlogForm
    template_name = ("create_blog.html")
    login_url = 'login'
    success_url = "/"
    success_message = "Your blog has been created"

class UpdateBlogView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Blog
    form_class = UpdateBlogForm
    template_name = ("update_blog.html")
    login_url = 'login'
    success_url = "/"
    success_message = "Your blog has been updated"

class DeleteBlogView(LoginRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    model = Blog
    template_name = ("delete_blog.html")
    login_url = 'login'
    success_url = "/"
    success_message = "Your blog has been deleted"


class blog_home(generic.ListView):
    model = Blog
    paginate_by = 10
    template_name = ("blog_home.html")

def blog_detail(request, slug):
    blog = Blog.objects.get(slug=slug)
    all_comments = BlogComment.objects.filter(blog = blog.id)
    all_blogs = Blog.objects.all().order_by('-post_date')[:10]
    
    form = CommentBlogForm()
    if request.method == "POST":
        form = CommentBlogForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your comment on this blog has been posted")
            return redirect("/blog_detail/"+blog.slug)
    else:
        form = CommentBlogForm()
    
    context = {
        'blog':blog,
        'all_blogs': all_blogs,
        'form': form,
        'all_comments': all_comments
    }
    return render(request, ("blog_detail.html"), context)