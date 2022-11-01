import uuid
from django.db import models
from django.conf import settings
from django.db.models import Count

from django.apps import apps

User = settings.AUTH_USER_MODEL
# Create your models here.

class Model_base(models.Model):
    id = models.UUIDField(default = uuid.uuid4, primary_key = True, db_index = True, editable = False)
    tiempo = models.DateTimeField(auto_now_add = True)
    actualizar = models.DateTimeField(auto_now = True)
    
    class Meta:
        abstract = True

class Canal_mensaje(Model_base):
    canal = models.ForeignKey("Canal", on_delete = models.CASCADE)
    usuario = models.ForeignKey(User, on_delete = models.CASCADE)
    texto = models.TextField()

class Canal_usuario(Model_base):
    canal = models.ForeignKey("Canal", null = True, on_delete = models.SET_NULL)
    usuario = models.ForeignKey(User, on_delete = models.CASCADE)

class Canal_query_set(models.QuerySet):
    def solo_uno(self):
        return self.annotate(num_usuarios = Count("usuarios")).filter(num_usuarios = 1)

    def solo_dos(self):
        return self.annotate(num_usuarios = Count("usuarios")).filter(num_usuarios = 2)

    def flitrar_por_username(self, username):
        return self.filter(canal_usuario__usuario__username = username)


class Canal_manager(models.Manager):

    def get_queryset(self, *args, **kwargs):
        return Canal_query_set(self.model, using = self._db)

    def filtrar_mensajes_por_privado(self, username_a, username_b):
        return self.get_queryset().solo_dos().flitrar_por_username(username_a).flitrar_por_username(username_b)

    def obtener_o_crear_canal_usuario_actual(self, user):
        qs = self.get_queryset().solo_uno().flitrar_por_username(user.username)
        if qs.exists():
            return qs.order_by("tiempo").first, False
        canal_obj = Canal.objects.create()
        Canal_usuario.objects.create(usuario = user, canal = canal_obj)
        return canal_obj, True

    def obtener_o_crear_canal_mensaje(self, username_a, username_b):
        qs = self.filtrar_mensajes_por_privado(username_a, username_b)
        if qs.exists():
            return qs.order_by("tiempo").first(), False 

        User = apps.get_model("auth", model_name = "User")
        usuario_a, usuario_b = None, None
        try:
            usuario_a = User.objects.get(username = username_a)
        except User.DoesNotExist:
            return None, False

        try:
            usuario_b = User.objects.get(username = username_b)
        except User.DoesNotExist:
            return None, False

        if usuario_a == None or usuario_b == None:
            return None, False

        obj_canal = Canal.objects.create()
        canal_usuario_a = Canal_usuario(usuario = usuario_a, canal = obj_canal)
        canal_usuario_b = Canal_usuario(usuario = usuario_b, canal = obj_canal)
        Canal_usuario.objects.bulk_create([canal_usuario_a, canal_usuario_b])
        return obj_canal, True


class Canal(Model_base):
    usuarios = models.ManyToManyField(User, blank = True, through = Canal_usuario)

    objects = Canal_manager()