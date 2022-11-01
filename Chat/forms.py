from django import forms 

class Form_mensajes(forms.Form):
    mensaje = forms.CharField(widget=forms.Textarea(attrs= {

        "class": "formulario_ms",
        "placeholder": "Escribe tu mensaje",
        
    }))


