from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from App_1.models import *
from ckeditor.widgets import CKEditorWidget 

class Crear_usuario(forms.Form):
    nombre: str = forms.CharField(max_length=40)
    apellido: str = forms.CharField(max_length=40)
    email: str = forms.EmailField()
    DNI: int = forms.IntegerField()
    fecha_de_nacimiento: str = forms.DateField()
    domicilio: str = forms.CharField(max_length=40)
    localidad: str = forms.CharField(max_length=40)
    provincia: str = forms.CharField(max_length=40)

class Crear_cliente(forms.Form):
    nivel_del_cliente: str = forms.CharField(max_length=40) # basico, gold, platinum, black.
    dinero_en_la_cuenta: int = forms.IntegerField()
    tarjeta_de_credito_vencida: bool = forms.BooleanField()
    fecha_de_vencimiento_tarjeta: str = forms.DateField()
    numero_de_tarjeta: int = forms.IntegerField()
    codigo_de_seguridad_tarjeta: int = forms.IntegerField()

class Crear_transferencia_bancaria(forms.Form):
    monto_en_pesos: int = forms.IntegerField()
    nombre_del_destinatario: str = forms.CharField(max_length=40)
    apellido_del_destinatario: str = forms.CharField(max_length=40)
    dni_del_destinatario: int = forms.IntegerField()
    

class Agregar_dinero(forms.Form):
    dinero_agregado: int = forms.IntegerField()

class User_register_form(UserCreationForm):
    username: str = forms.CharField(max_length=40)
    last_name: str = forms.CharField(max_length=40)
    DNI: int = forms.IntegerField()
    fecha_de_nacimiento: str = forms.DateField()
    domicilio: str = forms.CharField(max_length=40)
    localidad: str = forms.CharField(max_length=40)
    provincia: str = forms.CharField(max_length=40)
    email: str = forms.EmailField()
    password1 = forms.CharField(label="Ingrese su contraseña", widget = forms.PasswordInput)
    password2 = forms.CharField(label="Vuelva a ingresar su contraseña", widget = forms.PasswordInput)

  
    class Meta:
        model: object = User
        fields: list = ["username", "last_name", "DNI", "fecha_de_nacimiento", "domicilio", "localidad", "provincia", "email", "password1", "password2"]
        #Saca los mensajes de ayuda
        help_texts = {k: "" for k in fields}


class User_edit_form(UserCreationForm):
    username: str = forms.CharField(max_length=40, label= "Modificar nombre")
    last_name: str = forms.CharField(max_length=40, label= "Modificar apellido")
    DNI: int = forms.IntegerField(label = "Modificar DNI")
    fecha_de_nacimiento: str = forms.DateField(label = "Modificar fecha de nacimiento (formato yyyy-mm-dd)")
    domicilio: str = forms.CharField(max_length=40, label = "Modificar domicilio")
    localidad: str = forms.CharField(max_length=40, label = "Modificar localidad")
    provincia: str = forms.CharField(max_length=40, label = "Modificar provincia")
    email: str = forms.EmailField(label="Ingrese su nuevo email")
    password1: str = forms.CharField(label="Ingrese su nueva contraseña", widget = forms.PasswordInput)
    password2: str = forms.CharField(label="Vuelva a ingresar su contraseña", widget = forms.PasswordInput)


    class Meta:
        model: object = User
        fields: list = ["username", "last_name", "DNI", "fecha_de_nacimiento", "domicilio", "localidad", "provincia", "email", "password1", "password2"]
        #Saca los mensajes de ayuda
        help_texts = {k: "" for k in fields}
    
class AvatarForm(forms.Form):
    imagen= forms.ImageField(label="Imagen")


class CreateBlogForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Blog
        exclude = ('post_date', 'slug')
        widgets = {
            'author': forms.TextInput(attrs={'value': '', 'id':'author', 'type':'hidden'}),
            'mini_description': forms.Textarea(attrs={'class': 'form-control'})
        }
        

class UpdateBlogForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Blog
        exclude = ('post_date', 'slug')
        widgets = {
            'author': forms.TextInput(attrs={'value': '', 'id':'author', 'type':'hidden'}),
            'mini_description': forms.Textarea(attrs={'class': 'form-control'})
        }
        

class CommentBlogForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = "__all__"
        
        widgets = {
            'author': forms.TextInput(attrs={'value': '', 'id':'author', 'type':'hidden'}),
            'blog': forms.TextInput(attrs={'value': '', 'id':'blog', 'type':'hidden'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }