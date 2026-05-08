from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0012_prolactina_refs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='hipogonadismo_fem',
            field=models.CharField(
                blank=True, max_length=30,
                verbose_name='Hipogonadismo femenino',
                choices=[('', '—'), ('si', 'Sí'), ('no', 'No'), ('na', 'No aplica')],
            ),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='hipogonadismo_masc',
            field=models.CharField(
                blank=True, max_length=30,
                verbose_name='Hipogonadismo masculino',
                choices=[('', '—'), ('si', 'Sí'), ('no', 'No'), ('na', 'No aplica')],
            ),
        ),
    ]
