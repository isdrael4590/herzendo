from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='provincia_nacimiento',
            field=models.CharField(
                blank=True,
                max_length=50,
                choices=[
                    ('', '—'), ('Azuay', 'Azuay'), ('Bolívar', 'Bolívar'),
                    ('Cañar', 'Cañar'), ('Carchi', 'Carchi'),
                    ('Chimborazo', 'Chimborazo'), ('Cotopaxi', 'Cotopaxi'),
                    ('El Oro', 'El Oro'), ('Esmeraldas', 'Esmeraldas'),
                    ('Galápagos', 'Galápagos'), ('Guayas', 'Guayas'),
                    ('Imbabura', 'Imbabura'), ('Loja', 'Loja'),
                    ('Los Ríos', 'Los Ríos'), ('Manabí', 'Manabí'),
                    ('Morona Santiago', 'Morona Santiago'), ('Napo', 'Napo'),
                    ('Orellana', 'Orellana'), ('Pastaza', 'Pastaza'),
                    ('Pichincha', 'Pichincha'), ('Santa Elena', 'Santa Elena'),
                    ('Santo Domingo de los Tsáchilas', 'Santo Domingo de los Tsáchilas'),
                    ('Sucumbíos', 'Sucumbíos'), ('Tungurahua', 'Tungurahua'),
                    ('Zamora Chinchipe', 'Zamora Chinchipe'),
                ],
            ),
        ),
    ]
