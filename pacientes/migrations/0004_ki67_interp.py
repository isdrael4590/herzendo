from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0003_instruccion_choices'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='ki67_interp',
            field=models.CharField(
                blank=True,
                max_length=10,
                verbose_name='Interpretación Ki-67',
                choices=[
                    ('', '—'),
                    ('muy_bajo', 'Muy bajo (< 1 %)'),
                    ('bajo',     'Bajo (1 – 3 %)'),
                    ('alto',     'Alto (> 3 %)'),
                    ('muy_alto', 'Muy alto (> 10 %)'),
                ],
            ),
        ),
    ]
