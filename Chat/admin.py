from django.contrib import admin
from .models import Canal, Canal_usuario, Canal_mensaje

# Register your models here.

class  Canal_mensaje_inline(admin.TabularInline):
    model = Canal_mensaje
    extra = 1

class Canal_usuario_inline(admin.TabularInline):
    model = Canal_usuario
    extra = 1

class Canal_admin(admin.ModelAdmin):
    inlines = [Canal_mensaje_inline, Canal_usuario_inline]

    class Meta:
        model = Canal

admin.site.register(Canal, Canal_admin)
admin.site.register(Canal_usuario)
admin.site.register(Canal_mensaje)


