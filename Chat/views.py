from http.client import HTTPResponse
from multiprocessing import context
from django.shortcuts import render
from App_1.models import Cliente
from .models import Canal, Canal_mensaje, Canal_usuario
from django.http import HttpResponse, Http404, JsonResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model #
from django.contrib.auth.models import User
from .forms import Form_mensajes
from django.views.generic.edit import FormMixin
from django.views.generic import View, DetailView


from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class Inbox(View):
    def get(self, request):

        inbox = Canal.objects.filter(canal_usuario__usuario__in = [request.user.id])
    
        context = {

            "inbox": inbox
        }

        return render(request, 'inbox.html', context)

class Canal_form_mixin(FormMixin):
    form_class = Form_mensajes
    #success_url = './ '

    def get_success_url(self):
        return self.request.path

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied

        form = self.get_form()
        if form.is_valid():
            canal = self.get_object()
            usuario = self.request.user
            mensaje = form.cleaned_data.get("mensaje") 
            canal_obj = Canal_mensaje.objects.create(canal = canal, usuario = usuario, texto = mensaje)

            if request.is_ajax():
                return JsonResponse({

				    'mensaje':canal_obj.texto,
					'username':canal_obj.usuario.username
					}, status=201)

            return super().form_valid(form)

        else:

            if request.is_ajax():
                return JsonResponse({"Error":form.errors}, status=400)

            return super().form_invalid(form)

            


class Canal_detail_view(LoginRequiredMixin, Canal_form_mixin, DetailView):
    template_name = "chat.html"
    queryset = Canal.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        obj = context["object"]
        print(obj)
        # if self.request.user not in obj.usuarios.all():
        #     raise PermissionDenied

        context["si_canal_miembro"] = self.request.user in obj.usuarios.all()
        return context


    def get_queryset(self):
        usuario = self.request.user
        username = usuario.username
        qs = Canal.objects.all().flitrar_por_username(username)
        return qs


def mensajes_privados(request, username, *args, **kwargs):
    if not request.user.is_authenticated:
        return HttpResponse("Prohibido")

    mi_username = request.user.username

    canal, created = Canal.objects.obtener_o_crear_canal_mensaje(mi_username, username)
    if created:
        print("si, se ha creado!")
    
    if canal == None:
        raise Http404

    if username == mi_username:
        Usuarios_Canal = canal.canal_usuario_set.all().values("usuario__username")
        print(Usuarios_Canal)
        mensaje_canal = canal.canal_mensaje_set.all()
        print(mensaje_canal.values("texto"))
        
        mi_canal, _ = Canal.objects.obtener_o_crear_canal_usuario_actual(request.user)
        return render(request, "chat.html", {"canal": mi_canal})

   
    return render(request, "chat.html", {"canal": canal})

class Detail_mensajes(LoginRequiredMixin, Canal_form_mixin,  DetailView): 

    template_name = 'chat.html'

    def get_object(self, *args,**kwargs):
        mi_username = self.request.user.username
        username = self.kwargs.get("username")
        canal, _ = Canal.objects.obtener_o_crear_canal_mensaje(mi_username, username)
        

        if username == mi_username:
            mi_canal, _ = Canal.objects.obtener_o_crear_canal_usuario_actual(self.request.user)
            return mi_canal

        if canal == None:
            raise Http404

        return canal

def usuarios_chatear(request):
    usuarios = User.objects.all()
    return render(request, "usuarios_chatear.html", {"usuarios": usuarios})

