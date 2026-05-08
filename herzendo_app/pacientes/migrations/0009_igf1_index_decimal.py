from django.db import migrations, models


def limpiar_index_igf1(apps, schema_editor):
    # Borrar valores de texto anteriores (si/no) antes de cambiar a DecimalField
    schema_editor.execute("UPDATE pacientes_paciente SET igf1_index_elevado = NULL")


class Migration(migrations.Migration):
    atomic = False  # MySQL no permite DDL+DML en la misma transacción

    dependencies = [
        ('pacientes', '0008_etnia_choices'),
    ]

    operations = [
        migrations.RunPython(limpiar_index_igf1, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='paciente',
            name='igf1_index_elevado',
            field=models.DecimalField(
                blank=True,
                null=True,
                max_digits=10,
                decimal_places=3,
                verbose_name='INDEX IGF-1 (ref_max ÷ IGF-1)',
            ),
        ),
    ]
