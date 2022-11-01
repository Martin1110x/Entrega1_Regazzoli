from django.test import TestCase
from .models import Canal_mensaje, Canal_usuario, Canal
from django.contrib.auth import get_user_model
# Create your tests here.

User = get_user_model()

class Canal_test_case(TestCase):
    def setUp(self):
        self.usuario_a = User.objects.create(username='jorgitocode', password='holacomestas')
        self.usuario_b = User.objects.create(username='dosusuario', password='bien')
        self.usuario_c = User.objects.create(username='usuarioc', password='excelente')

    def test_usuario_count(self):
        qs = User.objects.all()
        self.assertEqual(qs.count(), 3)

    def test_cada_usuario_canal(self):
        qs = User.objects.all()
        for usuario in qs:
            canal_obj = Canal.objects.create()
            canal_obj.usuarios.add(usuario)

        canal_qs = Canal.objects.all()
        self.assertEqual(canal_qs.count(), 3)

        canal_qs_1 = canal_qs.solo_uno()
        self.assertEqual(canal_qs_1.count(), canal_qs.count())

    def prueba_dos_usuarios(self):
        canal_obj = Canal.objects.create()
        Canal_usuario.objects.create(usuario = self.usuario_a, canal = canal_obj)
        Canal_usuario.objects.create(usuario = self.usuario_b, canal = canal_obj)

        canal_obj_2 = Canal.objects.create()
        Canal_usuario.objects.create(usuario = self.usuario_c, canal = canal_obj_2)

        qs = Canal.objects.all()
        self.assertEqual(qs.count(), 2)

        solos_dos = qs.solo_dos()
        self.assertEqual(solos_dos.count(), 1)
