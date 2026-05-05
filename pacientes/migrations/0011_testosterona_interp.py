from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0010_cortisol_interp'),
    ]

    operations = [
        migrations.AddField(
            model_name='paciente',
            name='testosterona_interp',
            field=models.CharField(
                blank=True,
                max_length=30,
                verbose_name='Interpretación testosterona',
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
