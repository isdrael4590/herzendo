from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0011_testosterona_interp'),
    ]

    operations = [
        migrations.AddField(
            model_name='paciente',
            name='prolactina_ref_min',
            field=models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=3,
                                      verbose_name='Prolactina ref. mín'),
        ),
        migrations.AddField(
            model_name='paciente',
            name='prolactina_ref_max',
            field=models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=3,
                                      verbose_name='Prolactina ref. máx'),
        ),
    ]
