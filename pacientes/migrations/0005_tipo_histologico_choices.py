from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0004_ki67_interp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='tipo_histologico',
            field=models.CharField(
                blank=True,
                max_length=30,
                verbose_name='Tipo histológico del tumor',
                choices=[
                    ('', '—'),
                    ('prolactinoma',     'Prolactinoma'),
                    ('somatotropinoma',  'Somatotropinoma'),
                    ('corticotropinoma', 'Corticotropinoma'),
                    ('gonadotropinoma',  'Gonadotropinoma'),
                    ('tirotropinoma',    'Tirotropinoma'),
                    ('carcinoma',        'Carcinoma hipofisario'),
                ],
            ),
        ),
    ]
