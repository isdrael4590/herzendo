from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0007_tumor_interp_labels'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='etnia',
            field=models.CharField(
                blank=True,
                max_length=20,
                choices=[
                    ('', '—'),
                    ('mestizo',         'Mestizo'),
                    ('indigena',        'Indígena'),
                    ('afroecuatoriano', 'Afroecuatoriano'),
                    ('blanco',          'Blanco'),
                    ('montubio',        'Montubio'),
                    ('otro',            'Otros'),
                    ('no_dato',         'No dato'),
                ],
            ),
        ),
    ]
