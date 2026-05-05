from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Crea los grupos de roles si no existen'

    def handle(self, *args, **options):
        for nombre in ['administrador', 'medico', 'visualizador']:
            _, created = Group.objects.get_or_create(name=nombre)
            if created:
                self.stdout.write(f'  Grupo creado: {nombre}')
        self.stdout.write(self.style.SUCCESS('Grupos listos.'))
