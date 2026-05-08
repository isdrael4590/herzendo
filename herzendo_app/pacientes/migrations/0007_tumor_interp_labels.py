from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0006_prolactina_interp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='tamano_tumor_interp',
            field=models.CharField(
                blank=True,
                max_length=30,
                verbose_name='Interpretación tamaño tumor',
                choices=[
                    ('', '—'),
                    ('microadenoma', 'Microadenoma (< 10 mm)'),
                    ('macroadenoma', 'Macroadenoma (≥ 10 mm hasta 40 mm)'),
                    ('gigante',      'Adenoma gigante (> 40 mm)'),
                ],
            ),
        ),
    ]
