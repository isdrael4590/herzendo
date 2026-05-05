from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0009_igf1_index_decimal'),
    ]

    operations = [
        migrations.AddField(
            model_name='paciente',
            name='cortisol_interp',
            field=models.CharField(
                blank=True,
                max_length=30,
                verbose_name='Interpretación cortisol',
                choices=[
                    ('', '—'),
                    ('normal', 'Normal'),
                    ('elevado', 'Elevado'),
                    ('bajo', 'Bajo'),
                    ('no_det', 'No determinado'),
                ],
            ),
        ),
    ]
