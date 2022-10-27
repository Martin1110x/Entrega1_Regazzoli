#from curses import meta
from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.template.defaultfilters import slugify
from ckeditor.fields import RichTextField

# Create your models here.
class Empleado(models.Model):
    usuario = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
    DNI: int = models.IntegerField()
    fecha_de_nacimiento: str = models.DateField(null=True)
    domicilio: str = models.CharField(max_length=40, null=True)
    localidad: str = models.CharField(max_length=40, null=True)
    provincia: str = models.CharField(max_length=40, null=True)

    def __str__(self) -> str:
        return f"Nombre: {self.nombre} - Apellido: {self.apellido} - Email: {self.email} - DNI: {self.DNI}"

class Cliente(models.Model):
    usuario = models.ForeignKey(User, on_delete = models.CASCADE)
    DNI: int = models.IntegerField()
    fecha_de_nacimiento: str = models.DateField(null=True)
    domicilio: str = models.CharField(max_length=40, null=True)
    localidad: str = models.CharField(max_length=40, null=True)
    provincia: str = models.CharField(max_length=40, null=True)
    nivel_del_cliente: str = models.CharField(max_length=40) # basico, gold, platinum, black.
    dinero_en_la_cuenta: int = models.IntegerField()
    tarjeta_de_credito_vencida: bool = models.BooleanField()
    fecha_de_vencimiento_tarjeta: str = models.DateField()
    numero_de_tarjeta: int = models.IntegerField() 
    codigo_de_seguridad_tarjeta: int = models.IntegerField()


    def __str__(self) -> str:
        return f"Nombre: {self.nombre} - Apellido: {self.apellido} - Email: {self.email} - DNI: {self.DNI}"

class Transferencia_bancaria(models.Model):
    monto_en_pesos: int = models.IntegerField()
    fecha_de_transferencia: str = models.DateField()
    nombre_del_remitente: str = models.CharField(max_length=40)
    apellido_del_remitente: str = models.CharField(max_length=40)
    dni_del_remitente: int = models.IntegerField()
    nombre_del_destinatario: str = models.CharField(max_length=40)
    apellido_del_destinatario: str = models.CharField(max_length=40)
    dni_del_destinatario: int = models.IntegerField()
    
    
    def __str__(self) -> str:
        return f"Nombre remitente: {self.nombre_del_remitente} {self.apellido_del_remitente} - Fecha: {self.fecha_de_transferencia}"


class Avatar(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    imagen = models.ImageField(upload_to = "avatares", null = True, blank = True)

###CK EDITOR###

class Blog(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = RichTextField()
    mini_description = models.TextField()
    post_date = models.DateField(default=date.today)
    slug = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.name + " ==> " + str(self.author)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name + "-" + str(self.post_date))
        return super().save(*args, **kwargs)

class BlogComment(models.Model):
    description = models.TextField(help_text="Write your comment")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comment_date = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.blog)


