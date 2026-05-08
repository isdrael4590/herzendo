from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0005_tipo_histologico_choices'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='prolactina_interp',
            field=models.CharField(
                blank=True,
                max_length=30,
                verbose_name='Interpretación prolactina',
                choices=[
                    ('', '—'),
                    ('normal',  'Normal'),
                    ('baja',    'Baja'),
                    ('elevada', 'Elevada'),
                    ('no_dato', 'No dato'),
                ],
            ),
        ),
    ]
