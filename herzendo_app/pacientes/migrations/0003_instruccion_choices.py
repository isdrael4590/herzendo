from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0002_provincia_choices'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='nivel_instruccion',
            field=models.CharField(
                blank=True,
                max_length=30,
                verbose_name='Nivel de instrucción',
                choices=[
                    ('', '—'),
                    ('ninguna', 'Ninguna'),
                    ('primaria_completa', 'Primaria Completa'),
                    ('primaria_incompleta', 'Primaria Incompleta'),
                    ('secundaria_completa', 'Secundaria Completa'),
                    ('secundaria_incompleta', 'Secundaria Incompleta'),
                    ('superior_completa', 'Superior Completa'),
                    ('superior_incompleta', 'Superior Incompleta'),
                ],
            ),
        ),
    ]
